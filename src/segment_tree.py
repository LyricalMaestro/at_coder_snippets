
class LazySegmentTree:
    """
    非再帰版遅延セグメント木。
    更新は「加法」、取得は「最大値」のもの限定。
    取得のところの都合で取得演算子は可換になっている必要がある。
    """

    def __init__(self, init_array):
        n = 1
        while n < len(init_array):
            n *= 2
        
        self.size = n
        self.array = [0] * (2 * self.size)
        self.lazy_array = [0 for _ in range(2 * self.size)]
        for i, a in enumerate(init_array):
            self.array[self.size + i] = a
        
        end_index = self.size
        start_index = end_index // 2
        while start_index >= 1:
            for i in range(start_index, end_index):
                self.array[i] = max(self.array[2 * i], self.array[2 * i + 1])
            end_index = start_index
            start_index = end_index // 2
    
    def _propagates(self, *ids):
        for i in reversed(ids):
            self._propagate(i)

    def _propagate(self, i):
        v = self.lazy_array[i]
        if v == 0:
            return
        
        if i < self.size:
            self.lazy_array[2 * i] += v
            self.lazy_array[2 * i + 1] += v
            self.array[2 * i] += v
            self.array[2 * i + 1] += v
        self.lazy_array[i] = 0

    def _get_target_index(self, l, r):
        L = l + self.size; R = r + self.size
        lm = (L // (L & -L)) >> 1
        rm = (R // (R & -R)) >> 1
        while 0 < L and L < R:
            if R <= rm:
                yield R
            if L <= lm:
                yield L
            L >>= 1; R >>= 1
        while L > 0:
            yield L
            L >>= 1

    def add(self, l, r, x):
        # 2. 区間[l, r)のdata, lazyの値を更新
        L = self.size + l; R = self.size + r
        *ids, = self._get_target_index(l, r)
        self._propagates(*ids)
        while L < R:
            if R & 1:
                R -= 1
                self.lazy_array[R] += x
                self.array[R] += x
            if L & 1:
                self.lazy_array[L] += x
                self.array[L] += x
                L += 1
            L >>= 1; R >>= 1

        # 3. 伝搬させた区間について、ボトムアップにdataの値を伝搬する
        for i in ids:
            if i < self.size:
                self.array[i] = max(self.array[2 * i], self.array[2 * i +  1])

    def get_max(self, l, r):
        # 1. トップダウンにlazyの値を伝搬
        self._propagates(*self._get_target_index(l, r))
        L = self.size + l; R = self.size + r

        # 2. 区間[l, r)の最大値を求める
        s = 0
        while L < R:
            if R & 1:
                R -= 1
                s = max(s, self.array[R])
            if L & 1:
                s = max(s, self.array[L])
                L += 1
            L >>= 1; R >>= 1
        return s


class SegmentTree:
    """
    非再帰版セグメント木。
    更新は「加法」、取得は「最大値」のもの限定。
    """

    def __init__(self, init_array):
        n = 1
        while n < len(init_array):
            n *= 2
        
        self.size = n
        self.array = [0] * (2 * self.size)
        for i, a in enumerate(init_array):
            self.array[self.size + i] = a
        
        end_index = self.size
        start_index = end_index // 2
        while start_index >= 1:
            for i in range(start_index, end_index):
                self.array[i] = max(self.array[2 * i], self.array[2 * i + 1])
            end_index = start_index
            start_index = end_index // 2

    def add(self, x, a):
        index = self.size + x
        self.array[index] += a
        while index > 1:
            index //= 2
            self.array[index] = max(self.array[2 * index], self.array[2 * index + 1])

    def get_max(self, l, r):
        L = self.size + l; R = self.size + r

        # 2. 区間[l, r)の最大値を求める
        s = 0
        while L < R:
            if R & 1:
                R -= 1
                s = max(s, self.array[R])
            if L & 1:
                s = max(s, self.array[L])
                L += 1
            L >>= 1; R >>= 1
        return s

# -------------------------------------

from typing import Callable, Generic, Iterable, TypeVar

S = TypeVar("S")   # ノード情報
F = TypeVar("F")   # 遅延作用


class SegmentTreeBeats(Generic[S, F]):
    """
    汎用 Segment Tree Beats（非再帰版）。区間はすべて半開区間 [l, r)。

    通常の LazySegmentTree は、区間の集約情報だけで常に一括更新できる
    作用を扱う。Beats はこの条件を緩め、mapping が一括更新できる場合は
    遅延し、できない場合は子へ降りて更新し、親の情報を再計算する。

    深く降りる追加コストを抑えるには、更新によって区間内の値の種類などの
    「複雑さ」が減り、同じ理由で何度も降り続けない性質を利用する。
    例えば chmax は小さい値をまとめて引き上げ、chmin は大きい値を
    まとめて引き下げる。最大値と最小値の差が縮むのはその直感的な例。
    このクラス自体は複雑さを測定せず、mapping の成否だけで降下を判断する。

    応用時に用意する関数（具体的な実装は利用側で渡す）:

    op(array, left, right) -> None:
        3 引数はすべて S のインスタンス（添字ではない）。
        left と right の区間情報を、この順で結合して更新先 array に書き込む。
        戻り値は使わず、left と right は変更しない。
        更新先は入力とは別のインスタンスを渡す。
        結合結果は結合則を満たす必要がある。可換性は不要。

    e() -> S:
        空区間の情報（op の単位元）を新しいインスタンスで返す。
        空区間と x を左右どちらの順で結合しても、結果は x と同じ情報になる。
        op が更新するフィールドは、他のノードと共有しない。

    query_op(left, right) -> S:
        左右の区間情報を、この順で結合した新しい S を返す。
        入力は変更せず、結果のフィールドも入力と共有しない。
        結合結果は op と同じ情報になり、結合則を満たす。可換性は不要。
        query_op(query_op(a, b), c) と query_op(a, query_op(b, c)) は同じ情報。

    mapping(f, x) -> bool:
        区間情報 x だけで一括更新できれば、x のフィールドを書き換えて True。
        更新不要の場合も True。新しいノードは生成しない。
        情報不足なら x を変更せず False を返して子への降下を求める。
        作用 f は変更しない（複数ノードへの適用と遅延伝搬で共有するため）。
        葉と空区間では必ず成功し、空区間の情報は変えない。

    is_noop(f, x) -> bool（省略可能）:
        区間 x のどの要素にも f による変化がないと保証できれば True。
        True なら部分被覆でも探索を打ち切り、mapping と遅延作用の保存も省く。
        集約値が変わらないだけでは不十分で、各要素が変わらないことが必要。
        f と x は変更しない。不明なら False。省略時はこの判定を行わない。
        x はそのノードまでの遅延作用を反映済みの情報で判定する。

    composition(new_op, base_op) -> None:
        base_op の後に new_op を作用させる合成を、base_op に直接書き込む。
        更新後の base_op == new_op ∘ 更新前の base_op（作用の意味として）。
        new_op は変更しない。戻り値は使わない。
        base_op はノード専用の可変オブジェクトで、new_op とは別のものを渡す。
        new_op 内の可変フィールドをそのまま共有せず、値をコピーして書き込む。

    id_() -> F:
        どの要素も変えない恒等作用を、新しい可変オブジェクトで返す。
        各ノードが独立して書き換えられるよう、可変フィールドも共有しない。
        mapping(id_(), x) は x を変更せず True を返す。
        composition(f, base_op) は、base_op が恒等作用なら f と同じ作用を書き込む。
        composition(id_(), base_op) は base_op の作用を変えない。

    この実装では、親で受理した作用（合成した作用も含む）は、後で子へ
    伝搬するときにも必ず mapping が成功する設計を要求する。
    「apply 時に一括更新できず降りる」ことと、この伝搬時の条件は別。
    """

    def __init__(
        self,
        v: Iterable[S],
        op: Callable[[S, S, S], None],
        e: Callable[[], S],
        mapping: Callable[[F, S], bool],
        composition: Callable[[F, F], None],
        id_: Callable[[], F],
        query_op: Callable[[S, S], S],
        is_noop: Callable[[F, S], bool] | None = None,
    ):
        """
        __init__(v, op, e, mapping, composition, id_, query_op, is_noop=None):
            葉の情報 v と応用側の関数から木を構築する。構築時間は O(n)。
            v の各要素は生の値ではなく、mapping と op が扱う S を渡す。
            v の各要素は互いに独立したインスタンスを渡す。
            葉はコピーせず保持するため、更新すると v の要素も書き換わる。
        """
        v = list(v)

        self._n = len(v)
        self._op = op
        self._query_op = query_op
        self._e = e
        self._mapping = mapping
        self._is_noop = is_noop
        self._composition = composition
        self._id = id_

        size = 1
        log = 0
        while size < self._n:
            size <<= 1
            log += 1

        self._size = size
        self._log = log

        self._d = [e() for _ in range(2 * size)]

        # lazy は内部ノードのみ必要だが、
        # 実装を単純にするため size 個確保
        self._lz = [id_() for _ in range(size)]
        self._has_lz = [False] * size

        for i, x in enumerate(v):
            self._d[size + i] = x

        for k in range(size - 1, 0, -1):
            self._update(k)

    # ============================================================
    # 基本操作
    # ============================================================

    def _update(self, k: int) -> None:
        """
        _update(k) -> None:
            更新済みの左右の子を op で結合し、親 k の集約情報を再計算する。
            親 k の未伝搬の作用は、事前に push しておく。
        """
        self._op(
            self._d[k],
            self._d[k << 1],
            self._d[k << 1 | 1],
        )

    def _all_apply(self, k: int, f: F) -> bool:
        """
        _all_apply(k, f) -> bool:
            ノード k の集約情報だけで一括更新を試みる。
            更新不要なら何も変更せず True。それ以外は成功時に情報と遅延作用を更新する。
            情報不足なら木を変更せず False を返す。子への降下は呼び出し側が行う。
        """

        # 既存の lazy は保持したまま、今回の不要な作用だけを省く。
        if self._is_noop is not None and self._is_noop(f, self._d[k]):
            return True

        if not self._mapping(f, self._d[k]):
            return False

        if k < self._size:
            # 未保存なら base は恒等作用。初回も合成して、呼び出し元の f や
            # 伝搬元の親の作用と、このノードの可変な遅延作用を共有しない。
            self._composition(f, self._lz[k])
            self._has_lz[k] = True

        return True

    def _push(self, k: int) -> None:
        """
        _push(k) -> None:
            親 k に保存した作用を左右の子へ伝搬し、親の遅延作用を消す。
            親の集約情報はすでに更新済みなので変更しない。
            子で一括適用できなければ、応用側の契約違反として RuntimeError。
        """
        if not self._has_lz[k]:
            return

        f = self._lz[k]

        # 親で受理済みの lazy は、
        # 子でも受理可能であることを要求する。
        ok_left = self._all_apply(k << 1, f)
        ok_right = self._all_apply(k << 1 | 1, f)

        if not ok_left or not ok_right:
            raise RuntimeError(
                "Invalid SegmentTreeBeats mapping: "
                "an accepted lazy operation could not be pushed "
                "to its children."
            )

        self._lz[k] = self._id()
        self._has_lz[k] = False

    # ============================================================
    # Point
    # ============================================================

    def get(self, p: int) -> S:
        """
        get(p) -> S:
            根から葉まで遅延作用を伝搬し、位置 p の最新の情報を返す。
            0 <= p < n を満たさなければ IndexError。
            戻り値は木のノードへの参照。後の更新で内容が変わるので、直接変更しない。
        """
        if not (0 <= p < self._n):
            raise IndexError

        k = 1
        l = 0
        r = self._size

        while r - l > 1:
            self._push(k)

            m = (l + r) >> 1

            if p < m:
                k <<= 1
                r = m
            else:
                k = k << 1 | 1
                l = m

        return self._d[k]

    # ============================================================
    # Range Apply
    # ============================================================

    def apply(self, l: int, r: int, f: F) -> None:
        """
        apply(l, r, f) -> None:
            [l, r) の各要素に f を作用させる。空区間では何もしない。
            is_noop が True のノードでは、部分被覆でも探索を打ち切る。
            完全に覆うノードでも mapping が失敗すれば子へ降りて更新する。
            葉でも失敗する mapping は契約違反として RuntimeError。
            0 <= l <= r <= n を満たさなければ IndexError。
        """

        if not (0 <= l <= r <= self._n):
            raise IndexError

        if l == r:
            return

        # state
        #
        # 0:
        #   ノードに入る
        #
        # 1:
        #   子の処理終了後。pullする。
        #
        # (k, node_l, node_r, state)

        stack = [(1, 0, self._size, 0)]

        while stack:
            k, nl, nr, state = stack.pop()

            if state == 1:
                self._update(k)
                continue

            # スタックには対象区間と重なるノードだけが入る。
            # 完全被覆
            if l <= nl and nr <= r:

                if self._all_apply(k, f):
                    continue

                # 区間全体が対象でも、集約情報だけでは更新できない。
                # 子へ降りて更新することで、応用側が想定する複雑さの解消を進める。
                # 葉には情報不足がないため、必ず成功する必要がある。
                if nr - nl == 1:
                    raise RuntimeError(
                        "mapping() failed on a leaf."
                    )

            # 完全被覆時は _all_apply で判定済み。部分被覆でも、ノード全体が
            # 変化しないなら子へ降りる必要はない。
            elif self._is_noop is not None and self._is_noop(f, self._d[k]):
                continue

            # 部分被覆 or Beats
            self._push(k)

            m = (nl + nr) >> 1

            # 子処理の後で親を再構築
            stack.append(
                (k, nl, nr, 1)
            )

            # 親は対象区間と重なるので、中央 m との比較だけで子の重なりを判定。
            # 右を先に積み、処理順は左→右にする。
            if m < r:
                stack.append((k << 1 | 1, m, nr, 0))
            if l < m:
                stack.append((k << 1, nl, m, 0))

    # ============================================================
    # Range Query
    # ============================================================

    def prod(self, l: int, r: int) -> S:
        """
        prod(l, r) -> S:
            [l, r) の最新の情報を左から右へ query_op で結合して返す。
            部分的に参照するノードでは、子へ降りる前に遅延作用を伝搬する。
            空区間では e()。0 <= l <= r <= n を満たさなければ IndexError。
        """

        if not (0 <= l <= r <= self._n):
            raise IndexError

        if l == r:
            return self._e()

        result = self._e()

        stack = [(1, 0, self._size)]

        while stack:
            k, nl, nr = stack.pop()

            # スタックには対象区間と重なるノードだけが入る。
            if l <= nl and nr <= r:
                result = self._query_op(result, self._d[k])
                continue

            self._push(k)

            m = (nl + nr) >> 1

            # 重なる子だけを積む。query_op が非可換でも左→右に結合するため、
            # 右を先に積む。
            if m < r:
                stack.append((k << 1 | 1, m, nr))
            if l < m:
                stack.append((k << 1, nl, m))

        return result

    def all_prod(self) -> S:
        """
        all_prod() -> S:
            全区間 [0, n) の最新の集約情報を O(1) で返す。空の木では e()。
            根の情報は常に更新済みなので、遅延作用の伝搬は不要。
            戻り値は根への参照。後の更新で内容が変わるので、直接変更しない。
        """
        return self._d[1]
