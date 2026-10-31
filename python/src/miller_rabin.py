import random
from typing import Sequence


class MillerRabin:
    """
    ミラー・ラビン素数判定法。

    確定的判定(デフォルト)と確率的判定を切り替えられる。

        mr = MillerRabin()                     # 確定的(n < 2^64)
        mr.is_prime(1000000007)                # -> True

        mr = MillerRabin(probabilistic=True)   # 確率的(上限なし)
        mr.is_prime((1 << 89) - 1)             # -> True

    probabilistic=False の場合は固定底集合により n < 2^64 を誤りなく判定する。
        この範囲を超える入力に対しては保証がないため例外を送出する。
    probabilistic=True の場合はランダムなk個の底で確率的に判定する。
        合成数を素数と誤る確率は高々 4^(-k)。上限なく任意の整数に使える。
    """

    # n の大きさごとに「その範囲の奇数合成数を必ず見破る」ことが確認されている
    # 固定底集合。(閾値, 底集合) を閾値の昇順に並べる。
    # n が閾値未満なら、その底集合で確定判定できる。小さい n ほど底が少なく速い。
    # 出典: https://drken1215.hatenablog.com/entry/2023/05/23/233000
    _DETERMINISTIC_TABLE = (
        (4759123141, (2, 7, 61)),
        (1 << 64, (2, 325, 9375, 28178, 450775, 9780504, 1795265022)),
    )

    def __init__(self, probabilistic: bool = False, k: int = 40):
        """
        probabilistic: Trueなら確率的判定、Falseなら確定的判定(デフォルト)。
        k: 確率的判定で用いる底の個数。
        """
        self.probabilistic = probabilistic
        self.k = k

    def is_prime(self, n: int) -> bool:
        """
        nが素数かどうかを判定する。
        """
        if n < 2:
            return False
        # 2, 3 は基底ケース。底集合に必ず 2 が含まれるため試し割りは不要だが、
        # 確率的判定の底選択 randrange(2, n-1) が n<4 で範囲エラーになるのを防ぐ。
        if n < 4:
            return True

        # n - 1 = 2^s * d (dは奇数)
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for a in self._select_bases(n):
            if not self._witness(n, a, d, s):
                return False

        return True

    def _select_bases(self, n: int) -> Sequence[int]:
        """
        判定に用いる底の集合を返す。
        確率的判定ならランダムなk個、確定的判定ならnの大きさに応じた固定底集合。
        """
        if self.probabilistic:
            return [random.randrange(2, n - 1) for _ in range(self.k)]

        if n >= 1 << 64:
            raise ValueError(
                "確定的判定は n < 2^64 のみ対応しています。"
                "より大きい入力には probabilistic=True を指定してください。"
            )

        # n の大きさに応じた最小の底集合を選ぶ
        for threshold, bases in self._DETERMINISTIC_TABLE:
            if n < threshold:
                return bases

    @staticmethod
    def _witness(n: int, a: int, d: int, s: int) -> bool:
        """
        底aによるミラー・ラビンのテストを1回実行する。

        n - 1 = 2^s * d (dは奇数) と分解済みであること。
        返り値がTrueなら「この底では合成数と見破れなかった」(nは素数かもしれない)、
        Falseなら「この底でnは合成数と断定できた」(aはnのwitness)。
        """
        a %= n
        # aがnの倍数の時はこの底では何も判定できないので通過扱いにする
        if a == 0:
            return True

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True

        # x を s-1 回まで平方し、途中で -1 (= n - 1) に到達するか調べる
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                return True

        return False
