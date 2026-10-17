# Manacherアルゴリズムの実装
# https://klee.hatenablog.jp/entry/2020/06/18/210754 を参考にした
# 線形時間で回文部分文字列の個数を列挙するアルゴリズム

from typing import List

class ManacherResult:

    def __init__(self, rad_odd_length: List[int], rad_even_length: List[int]):
        self._rad_odd_length = rad_odd_length
        self._rad_even_length = rad_even_length

    def get_max_palindrome_length(self):
        # 奇数長の最大長は 2r - 1, 偶数長の最大長は 2r
        max_odd_rad = max(self._rad_odd_length, default=0)
        max_even_rad = max(self._rad_even_length, default=0)
        odd_len = 2 * max_odd_rad - 1 if max_odd_rad > 0 else 0
        even_len = 2 * max_even_rad
        return max(odd_len, even_len)

    def get_palindrome_count(self):
        return sum(self._rad_odd_length) + sum(self._rad_even_length)


class Manacher:
    """Manacherアルゴリズム

    Aの間と両端に区切り文字を挟んだ列に対して奇数長Manacherを適用することで、
    奇数長・偶数長両方の回文の半径を線形時間で求める。
    """

    def __init__(self, seperator = "#"):
        self._seperator = seperator

    def solve(self, A) -> ManacherResult:
        # 奇数長回文の計算
        rad_odd_length = self._manacher_odd_length(A)

        # 偶数長回文の計算:
        n = len(A)
        # Aの間と両端に区切り文字を挟んだ列 (長さ 2n + 1) を作る
        # B[2i] が区切り、B[2i + 1] が A[i] に対応する
        B = [self._seperator] * (2 * n + 1)
        for i in range(n):
            B[2 * i + 1] = A[i]

        rad = self._manacher_odd_length(B)

        # B[2c] (区切り位置) を中心とする回文が Aでの偶数長回文に対応する。
        # B上の半径 r (区切り位置では常に奇数) は A に射影すると r - 1 文字 (偶数) になる
        # ので、Aでの半径は (r - 1) // 2
        rad_even_length = [(rad[2 * c] - 1) // 2 for c in range(n + 1)]

        return ManacherResult(rad_odd_length, rad_even_length)

    @staticmethod
    def _manacher_odd_length(A) -> List[int]:
        n = len(A)

        rad = [0] * n
        # (c - r, c + r)という開区間
        c = 0
        r = 0
        while c < n:

            # どんどん右に伸ばしていく
            while 0 <= c - r and c + r < n and A[c - r] == A[c + r]:
                r += 1
            rad[c] = r

            # c ~ c + rないについてc - r までの結果を使い回す
            k = 1
            while 0 <= c - k and k + rad[c - k] < r:
                rad[c + k] = rad[c - k]
                k += 1

            # 計算が終わった分だけ前進する
            c += k
            r -= k

        return rad
