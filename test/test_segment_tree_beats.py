"""区間 chmax / chmin と区間和を、最小値・最大値で判定する応用例。

説明を簡潔にするため、一括更新は「変化なし」か「全要素が同じ値になる」
場合だけ受理する。第二最小値・第二最大値を保持する最適化は行わない。
"""

from dataclasses import dataclass
from pathlib import Path
import random
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from segment_tree import SegmentTreeBeats


@dataclass
class Node:
    total: int = 0
    size: int = 0
    minimum: float = float("inf")
    maximum: float = -float("inf")


def leaf(value):
    """leaf(value) -> Node: 一要素の和・長さ・最小値・最大値を作る。"""
    return Node(value, 1, value, value)


def op(array, left, right):
    """
    op(array, left, right) -> None:
        3 引数とも Node。左右の区間を結合し、更新先 array のフィールドに書き込む。
        left と right は変更せず、戻り値も返さない。
    """
    array.total = left.total + right.total
    array.size = left.size + right.size
    array.minimum = min(left.minimum, right.minimum)
    array.maximum = max(left.maximum, right.maximum)


def query_op(left, right):
    """
    query_op(left, right) -> Node:
        左右の情報を結合した新しい Node を返す。入力は変更しない。
        更新用 op と同じ和・長さ・最小値・最大値を計算する。
    """
    return Node(left.total + right.total, left.size + right.size,
                min(left.minimum, right.minimum), max(left.maximum, right.maximum))


def e():
    """e() -> Node: 長さと和が 0 の空区間を、独立したインスタンスで返す。"""
    return Node()


def id_():
    """id_() -> F: 制限のない上下限を、独立した可変リストで返す。"""
    return [-float("inf"), float("inf")]


def clamp(f, value):
    """clamp((lower, upper), value) -> 数値: 値を [lower, upper] に収める。"""
    lower, upper = f
    return min(max(value, lower), upper)


def mapping(f, x):
    """
    mapping(f, x) -> bool:
        chmax は (下限, inf)、chmin は (-inf, 上限) で表す。
        全要素が変化しないか同じ値になるなら、区間和も一括更新できる。
        成功時は x を直接更新して True、情報不足なら変更せず False を返す。
        葉・空区間・受理済み作用の子への伝搬は必ず成功する。
    """
    if x.size == 0:
        return True
    low = clamp(f, x.minimum)
    high = clamp(f, x.maximum)
    if low == high:
        x.total = low * x.size
        x.minimum = low
        x.maximum = high
        return True
    if (low, high) == (x.minimum, x.maximum):
        return True
    return False


def composition(new_op, base_op):
    """
    composition(new_op, base_op) -> None:
        base_op の後に new_op を作用させる合成を、base_op に書き込む。
        古い上下限を新しい区間へ収めると、合成後の上下限になる。
        new_op は変更しない。chmax と chmin の順序は交換できない。
    """
    base_op[0] = clamp(new_op, base_op[0])
    base_op[1] = clamp(new_op, base_op[1])


def is_noop(f, x):
    """
    is_noop(f, x) -> bool:
        空区間、または全要素が作用の上下限内なら、どの要素も変わらない。
        ノードを変更せず、探索と遅延作用の保存を省けるか判定する。
    """
    return x.size == 0 or (f[0] <= x.minimum and x.maximum <= f[1])


def make_tree(values, mapper=mapping, is_noop=None):
    return SegmentTreeBeats(map(leaf, values), op, e, mapper, composition, id_,
                            query_op, is_noop=is_noop)


def expected(values):
    if not values:
        return e()
    return Node(sum(values), len(values), min(values), max(values))


@pytest.mark.parametrize("f, result", [
    ((5, float("inf")), [5, 5, 7, 9]),
    ((-float("inf"), 5), [1, 3, 5, 5]),
])
def test_failed_bulk_update_descends(f, result):
    failures = []

    def tracked_mapping(action, node):
        updated = mapping(action, node)
        if not updated:
            failures.append(node)
        return updated

    tree = make_tree([1, 3, 7, 9], tracked_mapping)
    tree.apply(0, 4, f)
    assert failures  # 完全被覆でも一括更新できず、子へ降りるケース。
    assert tree.all_prod() == expected(result)
    assert [tree.get(i).total for i in range(4)] == result


@pytest.mark.parametrize("first, second, result", [
    ((10, float("inf")), (-float("inf"), 3), 3),
    ((-float("inf"), 3), (10, float("inf")), 10),
])
def test_composed_lazy_is_pushed_in_order(first, second, result):
    tree = make_tree([1, 2, 3, 4, 5, 6, 7, 8])
    tree.apply(0, 8, first)
    tree.apply(0, 8, second)
    assert tree.all_prod() == expected([result] * 8)
    assert tree.prod(1, 7) == expected([result] * 6)
    assert [tree.get(i).total for i in range(8)] == [result] * 8


@pytest.mark.parametrize("skip_noop", [False, True])
@pytest.mark.parametrize("n", [0, 1, 2, 7, 8, 17])
def test_random_updates_against_list(n, skip_noop):
    rng = random.Random(20260921 + n)
    values = [rng.randrange(-20, 21) for _ in range(n)]
    tree = make_tree(values, is_noop=is_noop if skip_noop else None)
    for step in range(200):
        l, r = sorted([rng.randrange(n + 1), rng.randrange(n + 1)])
        bound = rng.randrange(-30, 31)
        f = (bound, float("inf")) if step % 2 else (-float("inf"), bound)
        tree.apply(l, r, f)
        values[l:r] = [clamp(f, v) for v in values[l:r]]
        assert tree.all_prod() == expected(values)
        ql, qr = sorted([rng.randrange(n + 1), rng.randrange(n + 1)])
        assert tree.prod(ql, qr) == expected(values[ql:qr])
        if n and step % 11 == 0:
            assert [tree.get(i).total for i in range(n)] == values
    for l in range(n + 1):
        for r in range(l, n + 1):
            assert tree.prod(l, r) == expected(values[l:r])


def test_identity_noop_and_empty_range():
    tree = make_tree([-5, -5, 0, 8, 8])
    before = expected([-5, -5, 0, 8, 8])
    for f in [id_(), (-10, float("inf")), (-float("inf"), 10)]:
        tree.apply(0, 5, f)
        assert tree.all_prod() == before
    tree.apply(2, 2, (100, float("inf")))
    assert tree.all_prod() == before
    assert tree.prod(2, 2) == e()


def test_invalid_indices():
    tree = make_tree([1, 2, 3])
    for p in [-1, 3]:
        with pytest.raises(IndexError):
            tree.get(p)
    for l, r in [(-1, 2), (0, 4), (2, 1)]:
        with pytest.raises(IndexError):
            tree.prod(l, r)
        with pytest.raises(IndexError):
            tree.apply(l, r, id_())


def test_mapping_must_accept_leaves():
    tree = make_tree([1], lambda f, x: False)
    with pytest.raises(RuntimeError, match="failed on a leaf"):
        tree.apply(0, 1, id_())


def test_accepted_mapping_must_push_to_children():
    def invalid_mapping(f, x):
        return x.size > 1

    tree = make_tree([1, 2], invalid_mapping)
    tree.apply(0, 2, id_())
    with pytest.raises(RuntimeError, match="could not be pushed"):
        tree.get(0)


def test_mutating_op_preserves_input_nodes_and_query_order():
    # 文字列の結合で左右の順序も確認する。更新先だけを変更する op を使う。
    @dataclass
    class TextNode:
        text: str = ""

    def merge(target, left, right):
        assert target is not left and target is not right
        target.text = left.text + right.text

    leaves = [TextNode(c) for c in "abcde"]
    tree = SegmentTreeBeats(leaves, merge, TextNode,
                            lambda f, x: True, lambda new, old: None, lambda: None,
                            lambda left, right: TextNode(left.text + right.text))
    whole = tree.all_prod().text
    first = tree.prod(1, 4)
    assert first.text == "bcd"
    assert tree.prod(2, 5).text == "cde"
    assert first.text == "bcd"
    assert tree.all_prod().text == whole == "abcde"
    assert [node.text for node in leaves] == list("abcde")


def test_updates_reuse_nodes_without_constructing_new_ones(monkeypatch):
    values = [1, 3, 7, 9, -2, 6, 8]
    tree = make_tree(values)
    nodes = list(tree._d)
    snapshot = tree.prod(0, len(values))

    def forbidden_init(*args, **kwargs):
        raise AssertionError("更新中に Node を生成している")

    with monkeypatch.context() as patch:
        patch.setattr(Node, "__init__", forbidden_init)
        # 降下、一括更新、遅延作用の合成・伝搬、親の再計算をすべて通す。
        for l, r, f in [(0, 7, (5, float("inf"))),
                        (0, 4, (12, float("inf"))),
                        (0, 4, (-float("inf"), 2)),
                        (1, 6, (-float("inf"), 4))]:
            tree.apply(l, r, f)
            values[l:r] = [clamp(f, v) for v in values[l:r]]
        assert [tree.get(i).total for i in range(7)] == values
        assert all(old is new for old, new in zip(nodes, tree._d))
    assert tree.all_prod() == expected(values)
    assert snapshot == expected([1, 3, 7, 9, -2, 6, 8])


def test_failed_mapping_does_not_modify_node():
    node = expected([1, 3, 7, 9])
    assert mapping((5, float("inf")), node) is False
    assert node == expected([1, 3, 7, 9])


@pytest.mark.parametrize("l, r", [(0, 8), (1, 7)])
def test_noop_stops_before_mapping_or_descent(l, r, monkeypatch):
    tree = make_tree(range(8), is_noop=is_noop)

    def forbidden(*args):
        raise AssertionError("更新不要なら mapping・push・親の再計算は不要")

    monkeypatch.setattr(tree, "_mapping", forbidden)
    monkeypatch.setattr(tree, "_push", forbidden)
    monkeypatch.setattr(tree, "_update", forbidden)
    tree.apply(l, r, (-10, float("inf")))
    assert not any(tree._has_lz)
    assert tree.all_prod() == expected(list(range(8)))


def test_noop_keeps_existing_lazy_and_skips_unchanged_child(monkeypatch):
    tree = make_tree([5, 5, 1, 1], is_noop=is_noop)
    tree.apply(0, 4, (5, float("inf")))
    saved_lazy = tree._lz[1].copy()
    tree.apply(1, 3, (4, float("inf")))
    tree.apply(0, 4, (4, float("inf")))
    assert tree._has_lz[1] and tree._lz[1] == saved_lazy

    calls = []

    def tracked_mapping(f, node):
        calls.append(node)
        return mapping(f, node)

    monkeypatch.setattr(tree, "_mapping", tracked_mapping)
    # 左の子は最初から 5。右の子だけ mapping され、左に lazy は保存されない。
    assert tree.prod(0, 2) == expected([5, 5])
    assert len(calls) == 1 and calls[0] is tree._d[3]
    assert not tree._has_lz[2]
    assert [tree.get(i).total for i in range(4)] == [5] * 4
    tree.apply(1, 3, (-float("inf"), 2))
    assert tree.all_prod() == expected([5, 2, 2, 5])


def test_composition_mutates_base_and_preserves_new_op():
    base = id_()
    original = base
    new_op = [10, float("inf")]
    assert composition(new_op, base) is None
    assert base is original and base == new_op
    composition([-float("inf"), 3], base)
    assert base is original and base == [3, 3]
    assert new_op == [10, float("inf")]


def test_lazy_actions_are_independent_and_input_can_be_reused():
    tree = make_tree([0] * 8)
    assert len({id(f) for f in tree._lz}) == len(tree._lz)
    root_base = tree._lz[1]
    action = [5, float("inf")]
    tree.apply(0, 8, action)
    tree.apply(0, 8, [7, float("inf")])
    assert tree._lz[1] is root_base  # 合成で既存の base を書き換える。
    assert action == [5, float("inf")]
    action[0] = 100  # 呼び出し元の作用を書き換えても、保存済みの作用に影響しない。
    tree.apply(0, 4, [-float("inf"), 2])
    assert tree._lz[2] is not tree._lz[3]
    assert tree.prod(0, 4) == expected([2] * 4)
    assert tree.prod(4, 8) == expected([7] * 4)
    # 伝搬後の親に再度作用を保存し、古い作用が混ざらないことも確認する。
    tree.apply(0, 8, [-float("inf"), 4])
    assert [tree.get(i).total for i in range(8)] == [2] * 4 + [4] * 4
