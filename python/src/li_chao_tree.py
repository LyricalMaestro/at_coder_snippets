class LiChaoTree:
    """
    Li Chao Tree（李超線分木）。
    あらかじめ与えたx座標の列に対し、
    直線（線分）y = a * x + b を追加しながら、
    各xにおける最小値を高速に求めるデータ構造。

    座標圧縮は行わない。x_array にはリーフに対応するx座標を
    昇順で並べて渡し、l / r / x はその添字（インデックス）で指定する。
    （x_array = [0, 1, ..., n-1] のように渡せば添字 == x座標となる）

    - 直線追加（区間全体）: O(log N)
    - 線分追加（区間 [l, r)）: O(log^2 N)
    - 最小値クエリ          : O(log N)

    参考: https://smijake3.hatenablog.com/entry/2018/06/16/144548
    """

    INF = float("inf")

    def __init__(self, x_array):
        """
        ベースとなるxの範囲を初期化する。
        x_array は各リーフに対応するx座標（昇順）。
        """
        self.xs = list(x_array)
        n = len(self.xs)

        size = 1
        while size < n:
            size *= 2
        self.size = size

        # リーフ数を2べきに揃えるため、末尾を最大値で埋める
        self.xs += [self.xs[-1]] * (size - n)

        # 各ノードが保持する直線 (a, b)。None は「直線なし（= +∞）」を表す。
        # 1-indexed: ルート=1, 子=2k/2k+1, リーフ=size+i（i番目の座標）
        self.lines = [None] * (2 * size)

    @staticmethod
    def _f(line, x):
        a, b = line
        return a * x + b

    def add_line(self, l, r, a, b):
        """
        半開区間 [l, r)（リーフ添字）に対して
        線分 y = a * x + b を追加する。
        区間全体に追加したい場合は add_line(0, len(x_array), a, b)。
        """
        if l < r:
            self._add_segment((a, b), l, r, 1, 0, self.size)

    def _add_segment(self, line, seg_l, seg_r, k, node_l, node_r):
        """
        線分追加：添字区間 [seg_l, seg_r) に line を追加する。
        ノード k は添字区間 [node_l, node_r) を担当する。
        """
        if seg_r <= node_l or node_r <= seg_l:
            return
        if seg_l <= node_l and node_r <= seg_r:
            # ノード区間がすっぽり含まれる → そのノードに直線として追加
            self._add_line(line, k, node_l, node_r)
            return
        mid = (node_l + node_r) // 2
        self._add_segment(line, seg_l, seg_r, 2 * k, node_l, mid)
        self._add_segment(line, seg_l, seg_r, 2 * k + 1, mid, node_r)

    def _add_line(self, line, k, l, r):
        """
        ノード k（担当区間 [l, r)）以下に対して直線 line を追加する。
        各ノードでは「区間の中点でより小さい方」を残し、
        負けた直線を勝敗が入れ替わる側の子へ降ろしていく。
        """
        while True:
            cur = self.lines[k]
            if cur is None:
                self.lines[k] = line
                return

            m = (l + r) // 2
            left = self._f(line, self.xs[l]) < self._f(cur, self.xs[l])
            mid = self._f(line, self.xs[m]) < self._f(cur, self.xs[m])
            right = self._f(line, self.xs[r - 1]) < self._f(cur, self.xs[r - 1])

            if left and right:
                # 区間全体で line が小さい → 置き換えて終了
                self.lines[k] = line
                return
            if not left and not right:
                # 区間全体で既存が優位 → 何もしない
                return

            if mid:
                # 中点では line が小さい → ノードを line にして、負けたcurを降ろす
                self.lines[k], line = line, cur

            # 端点と中点で勝敗が異なる側へ降りる
            if left != mid:
                k = 2 * k
                r = m
            else:
                k = 2 * k + 1
                l = m

    def calc_min_value(self, x):
        """
        添字 x のリーフ（座標 x_array[x]）における最小値を計算する。
        """
        xv = self.xs[x]
        k = self.size + x
        s = self.INF
        while k >= 1:
            line = self.lines[k]
            if line is not None:
                v = self._f(line, xv)
                if v < s:
                    s = v
            k //= 2
        return s

# ------------------------------------------------------------

class LiChaoTree:
    """
    Li Chao Tree（李超線分木）。
    あらかじめ与えたx座標の列に対し、
    直線（線分）y = a * x + b を追加しながら、
    各xにおける最大値を高速に求めるデータ構造。

    座標圧縮は行わない。x_array にはリーフに対応するx座標を
    昇順で並べて渡し、l / r / x はその添字（インデックス）で指定する。
    （x_array = [0, 1, ..., n-1] のように渡せば添字 == x座標となる）

    - 直線追加（区間全体）: O(log N)
    - 線分追加（区間 [l, r)）: O(log^2 N)
    - 最大値クエリ          : O(log N)

    参考: https://smijake3.hatenablog.com/entry/2018/06/16/144548
    """

    NEG_INF = -float("inf")

    def __init__(self, x_array):
        """
        ベースとなるxの範囲を初期化する。
        x_array は各リーフに対応するx座標（昇順）。
        """
        self.xs = list(x_array)
        n = len(self.xs)

        size = 1
        while size < n:
            size *= 2
        self.size = size

        # リーフ数を2べきに揃えるため、末尾を最大値で埋める
        self.xs += [self.xs[-1]] * (size - n)

        # 各ノードが保持する直線 (a, b)。None は「直線なし（= -∞）」を表す。
        # 1-indexed: ルート=1, 子=2k/2k+1, リーフ=size+i（i番目の座標）
        self.lines = [None] * (2 * size)

    @staticmethod
    def _f(line, x):
        a, b = line
        return a * x + b

    def add_line(self, l, r, a, b):
        """
        半開区間 [l, r)（リーフ添字）に対して
        線分 y = a * x + b を追加する。
        区間全体に追加したい場合は add_line(0, len(x_array), a, b)。
        """
        if l < r:
            self._add_segment((a, b), l, r, 1, 0, self.size)

    def _add_segment(self, line, seg_l, seg_r, k, node_l, node_r):
        """
        線分追加：添字区間 [seg_l, seg_r) に line を追加する。
        ノード k は添字区間 [node_l, node_r) を担当する。
        """
        if seg_r <= node_l or node_r <= seg_l:
            return
        if seg_l <= node_l and node_r <= seg_r:
            # ノード区間がすっぽり含まれる → そのノードに直線として追加
            self._add_line(line, k, node_l, node_r)
            return
        mid = (node_l + node_r) // 2
        self._add_segment(line, seg_l, seg_r, 2 * k, node_l, mid)
        self._add_segment(line, seg_l, seg_r, 2 * k + 1, mid, node_r)

    def _add_line(self, line, k, l, r):
        """
        ノード k（担当区間 [l, r)）以下に対して直線 line を追加する。
        各ノードでは「区間の中点でより大きい方」を残し、
        負けた直線を勝敗が入れ替わる側の子へ降ろしていく。
        """
        while True:
            cur = self.lines[k]
            if cur is None:
                self.lines[k] = line
                return

            m = (l + r) // 2
            left = self._f(line, self.xs[l]) > self._f(cur, self.xs[l])
            mid = self._f(line, self.xs[m]) > self._f(cur, self.xs[m])
            right = self._f(line, self.xs[r - 1]) > self._f(cur, self.xs[r - 1])

            if left and right:
                # 区間全体で line が大きい → 置き換えて終了
                self.lines[k] = line
                return
            if not left and not right:
                # 区間全体で既存が優位 → 何もしない
                return

            if mid:
                # 中点では line が大きい → ノードを line にして、負けたcurを降ろす
                self.lines[k], line = line, cur

            # 端点と中点で勝敗が異なる側へ降りる
            if left != mid:
                k = 2 * k
                r = m
            else:
                k = 2 * k + 1
                l = m

    def calc_max_value(self, x):
        """
        添字 x のリーフ（座標 x_array[x]）における最大値を計算する。
        """
        xv = self.xs[x]
        k = self.size + x
        s = self.NEG_INF
        while k >= 1:
            line = self.lines[k]
            if line is not None:
                v = self._f(line, xv)
                if v > s:
                    s = v
            k //= 2
        return s
