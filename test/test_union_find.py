import os
import pathlib
import sys
from typing import List

src_path = pathlib.Path(os.path.dirname(__file__)).parent.joinpath("src")
sys.path.append(str(src_path))

from union_find import RollbackUnionFind

class TestRollbackUnionFind:
    """
    RollbackUnionFindクラスのテスト
    """

    def test_constructor(self):
        """
        コンストラクタのテスト
        """
        uf = RollbackUnionFind(10)
        assert [i for i in range(10)] == uf.root
        assert [1] * 10 == uf.size

    def test_merge_diff_root1(self):
        """
        mergeメソッドのテスト(異なるルートでサイズが同じ時)
        """
        uf = RollbackUnionFind(10)

        actual = uf.merge(1, 2)

        assert actual is True
        assert [0, 1, 1, 3, 4, 5, 6, 7, 8, 9] == uf.root
        assert [1, 2, 1, 1, 1, 1, 1, 1, 1, 1] == uf.size
        assert 1 == uf.get_root(1)
        assert 1 == uf.get_root(2)

    def test_merge_diff_root2(self):
        """
        mergeメソッドのテスト(異なるルートでサイズが異なる場合。左>右)
        """
        uf = RollbackUnionFind(10)
        uf.merge(1, 2)

        actual = uf.merge(1, 3)

        assert actual is True
        assert [0, 1, 1, 1, 4, 5, 6, 7, 8, 9] == uf.root
        assert [1, 3, 1, 1, 1, 1, 1, 1, 1, 1] == uf.size
        assert 1 == uf.get_root(1)
        assert 1 == uf.get_root(3)

    def test_merge_diff_root2(self):
        """
        mergeメソッドのテスト(異なるルートでサイズが異なる場合。右>左)
        """
        uf = RollbackUnionFind(10)
        uf.merge(1, 2)

        actual = uf.merge(3, 1)

        assert actual is True
        assert [0, 1, 1, 1, 4, 5, 6, 7, 8, 9] == uf.root
        assert [1, 3, 1, 1, 1, 1, 1, 1, 1, 1] == uf.size
        assert 1 == uf.get_root(1)
        assert 1 == uf.get_root(3)

    def test_merge_same_root(self):
        """
        mergeメソッドのテスト(同じルートの場合)
        """
        uf = RollbackUnionFind(10)
        uf.merge(1, 2)
        uf.merge(3, 1)

        actual = uf.merge(3, 2)

        assert actual is False
        assert [0, 1, 1, 1, 4, 5, 6, 7, 8, 9] == uf.root
        assert [1, 3, 1, 1, 1, 1, 1, 1, 1, 1] == uf.size
        assert 1 == uf.get_root(2)
        assert 1 == uf.get_root(3)

    def test_merge(self):
        """
        mergeメソッドのテスト。複数回mergeして森を構築。
        """
        uf = RollbackUnionFind(10)

        uf.merge(1, 2)
        uf.merge(3, 4)
        uf.merge(4, 5)
        uf.merge(6, 5)
        uf.merge(1, 8)
        uf.merge(2, 6)

        assert [0, 3, 1, 3, 3, 3, 3, 7, 1, 9] == uf.root
        assert [1, 3, 1, 7, 1, 1, 1, 1, 1, 1] == uf.size

    def test_rollback_with_history(self):
        """
        rollbackメソッドのテスト。一つ前に戻るテスト。
        """
        uf = RollbackUnionFind(10)
        uf.merge(1, 2)
        uf.merge(3, 4)
        uf.merge(4, 5)
        uf.merge(6, 5)
        uf.merge(1, 8)
        uf.merge(2, 6)

        uf.rollback()

        assert [0, 1, 1, 3, 3, 3, 3, 7, 1, 9] == uf.root
        assert [1, 3, 1, 4, 1, 1, 1, 1, 1, 1] == uf.size
        assert 1 == uf.get_root(2)
        assert 3 == uf.get_root(6)

    def test_rollback_no_history(self):
        """
        rollbackメソッドのテスト。mergeが一度も成功していない時のテスト
        """        
        uf = RollbackUnionFind(10)

        uf.rollback()

        assert [i for i in range(10)] == uf.root
        assert [1] * 10 == uf.size

    def test_rollback_and_merge(self):
        """
        rollback成功後 -> mergeの流れで正しくデータが作れるかのテスト。
        """

        uf = RollbackUnionFind(10)
        uf.merge(1, 2)
        uf.merge(3, 4)
        uf.merge(4, 5)
        uf.merge(6, 5)
        uf.merge(1, 8)
        uf.merge(2, 6)
        uf.rollback()

        actual = uf.merge(2, 7)

        assert actual is True
        assert [0, 1, 1, 3, 3, 3, 3, 1, 1, 9] == uf.root
        assert [1, 4, 1, 4, 1, 1, 1, 1, 1, 1] == uf.size
        assert 1 == uf.get_root(2)
        assert 1 == uf.get_root(7)
