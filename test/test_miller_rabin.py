import os
import pathlib
import sys

import pytest

src_path = pathlib.Path(os.path.dirname(__file__)).parent.joinpath("src")
sys.path.append(str(src_path))

from miller_rabin import MillerRabin


def _sieve_primes(limit: int) -> set:
    """
    エラトステネスの篩で limit 未満の素数集合を作る(テストの正解データ用)
    """
    is_composite = [False] * limit
    primes = set()
    for i in range(2, limit):
        if not is_composite[i]:
            primes.add(i)
            for j in range(i * i, limit, i):
                is_composite[j] = True
    return primes


class TestMillerRabinDeterministic:
    """
    確定的判定(デフォルト)のテスト
    """

    def test_small_non_primes(self):
        """
        2未満や0, 1は素数ではない
        """
        mr = MillerRabin()
        assert mr.is_prime(0) is False
        assert mr.is_prime(1) is False
        assert mr.is_prime(-7) is False

    def test_small_primes(self):
        """
        小さい素数を正しく素数と判定する(基底ケース2,3を含む)
        """
        mr = MillerRabin()
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            assert mr.is_prime(p) is True

    def test_against_sieve(self):
        """
        10000未満の全整数について篩の結果と一致するか総当たりで確認する
        """
        mr = MillerRabin()
        limit = 10000
        primes = _sieve_primes(limit)
        for n in range(limit):
            assert mr.is_prime(n) is (n in primes)

    def test_carmichael_numbers(self):
        """
        カーマイケル数(フェルマー判定をだます合成数)を合成数と判定できる
        """
        mr = MillerRabin()
        for n in (561, 1105, 1729, 2465, 2821, 6601, 8911):
            assert mr.is_prime(n) is False

    def test_strong_pseudoprimes_base2(self):
        """
        底2の強擬素数(底2だけでは通ってしまう合成数)を合成数と判定できる
        """
        mr = MillerRabin()
        for n in (2047, 3277, 4033, 4681, 8321):
            assert mr.is_prime(n) is False

    def test_large_primes(self):
        """
        大きい既知の素数を素数と判定する
        """
        mr = MillerRabin()
        large_primes = [
            1000000007,
            1000000009,
            998244353,
            2147483647,      # 2^31 - 1 (メルセンヌ素数)
            9223372036854775783,  # 2^63 未満の素数
            18446744073709551557,  # 2^64 未満の最大の素数
        ]
        for p in large_primes:
            assert mr.is_prime(p) is True

    def test_large_composites(self):
        """
        大きい合成数を合成数と判定する
        """
        mr = MillerRabin()
        assert mr.is_prime(1000000007 * 1000000009) is False
        assert mr.is_prime(998244353 * 998244353) is False
        assert mr.is_prime((1 << 61) - 2) is False  # 偶数
        assert mr.is_prime(9223372036854775807) is False  # 2^63 - 1 は合成数

    def test_base_set_boundary(self):
        """
        底集合が {2,7,61} から7底集合へ切り替わる境界 4759123141 付近を確認する。
        4759123141 は {2,7,61} を通過してしまう最小の合成数なので、
        切り替え後の7底集合で合成数と判定できなければならない。
        """
        mr = MillerRabin()
        assert mr.is_prime(4759123141) is False  # {2,7,61} の最小共通強擬素数(合成数)
        assert mr.is_prime(4759123151) is True   # 直後の素数(7底集合側)
        # {2,7,61} で確定判定できる範囲側の既知の強擬素数も合成数と判定できる
        assert mr.is_prime(3215031751) is False  # 底 {2,3,5,7} の最小共通強擬素数

    def test_out_of_range_raises(self):
        """
        確定的判定は 2^64 以上ではエラーを送出する
        """
        mr = MillerRabin()
        # 試し割りしないので、2^64 より大きい素数でも範囲チェックに到達する
        with pytest.raises(ValueError):
            mr.is_prime(18446744073709551629)


class TestMillerRabinProbabilistic:
    """
    確率的判定のテスト
    """

    def test_against_sieve(self):
        """
        確率的判定でも小さい範囲では篩と一致する
        """
        mr = MillerRabin(probabilistic=True)
        limit = 3000
        primes = _sieve_primes(limit)
        for n in range(limit):
            assert mr.is_prime(n) is (n in primes)

    def test_carmichael_numbers(self):
        """
        確率的判定でもカーマイケル数を合成数と判定できる
        """
        mr = MillerRabin(probabilistic=True)
        for n in (561, 1105, 1729, 2465, 2821, 6601, 8911):
            assert mr.is_prime(n) is False

    def test_large_prime_no_upper_bound(self):
        """
        確率的判定は上限なく大きい素数にも使える
        """
        mr = MillerRabin(probabilistic=True)
        # 2^89 - 1 はメルセンヌ素数
        assert mr.is_prime((1 << 89) - 1) is True

    def test_large_composite_no_upper_bound(self):
        """
        確率的判定は 2^64 を超える合成数も合成数と判定する
        """
        mr = MillerRabin(probabilistic=True)
        p = (1 << 61) - 1  # メルセンヌ素数
        q = (1 << 89) - 1  # メルセンヌ素数
        assert mr.is_prime(p * q) is False
