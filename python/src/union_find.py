
class UnionFind:
    """
    UnionFindの基本的な処理を実装したクラス
    """

    def __init__(self, size):
        self.root = [i for i in range(size)]
        self.size = [1] * size

    def get_root(self, v):
        if v == self.root[v]:
            return v
        else:
            old_root = self.root[v]
            new_root = self.get_root(old_root)
            self.root[v] = new_root
            return new_root

    def merge(self, u, v):
        root_u = self.get_root(u)
        root_v = self.get_root(v)
        if root_u == root_v:
            return False

        if self.size[root_u] >= self.size[root_v]:
            self.size[root_u] += self.size[root_v]
            self.root[root_v] = root_u
            self.root[v] = root_u
        else:
            self.size[root_v] += self.size[root_u]
            self.root[root_u] = root_v
            self.root[u] = root_v
        return True
    
# ----------------------------------------------------------------------

from collections import deque

class RollbackUnionFind:
    """
    rollback機能をつけたUnionFindの基本的な処理を実装したクラス
    この実装でのrollbackは、mergeしたときのみできる
    一回のrollbackメソッドで戻る状態は一つ前の状態のみ
    """

    def __init__(self, size):
        self.root = [i for i in range(size)]
        self.size = [1] * size
        self.history = deque()

    def get_root(self, v):
        if v == self.root[v]:
            return v
        else:
            # undoを加味する場合、経路圧縮込みだと大変なので実装簡易化のために経路圧縮はしない
            return self.get_root(self.root[v])

    def merge(self, u, v):
        root_u = self.get_root(u)
        root_v = self.get_root(v)
        if root_u == root_v:
            return False

        self.history.append((root_u, self.root[root_u], self.size[root_u]))
        self.history.append((root_v, self.root[root_v], self.size[root_v]))
        if self.size[root_u] >= self.size[root_v]:
            self.size[root_u] += self.size[root_v]
            self.root[root_v] = root_u
        else:
            self.size[root_v] += self.size[root_u]
            self.root[root_u] = root_v
        return True
    
    def rollback(self):
        if len(self.history) > 0:
            self._undo()

    def _undo(self):
        u, root_u, size_u = self.history.pop()
        self.root[u] = root_u
        self.size[root_u] = size_u
        v, root_v, size_v = self.history.pop()
        self.root[v] = root_v
        self.size[root_v] = size_v
