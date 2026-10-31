import os
import pathlib
import sys
import unittest
from itertools import accumulate, product
from random import Random
from typing import List

src_path = pathlib.Path(os.path.dirname(__file__)).parent.joinpath("src")
sys.path.append(str(src_path))

from binary_index_tree import BinaryIndexTree


class TestBinaryIndexTreeLeastUpperBound(unittest.TestCase):

    def _make_bit_object(
        self, size: int, input_data: List[int]
    ) -> BinaryIndexTree:
        bit = BinaryIndexTree(size)
        for a in input_data:
            bit.add(a, 1)
        return bit

    def test_find_set_value(self):
        """
        引数に「すでに設定し値に対するsum」を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=10, input_data=[5, 3, 7, 10, 8, 4]
        )
        lub = bit.least_upper_bound(value=3)
        assert 5 == lub

    def test_find_unset_value(self):
        """
        引数に「すでに設定し値に対するsum」以外を設定した場合のテスト
        ・1以上 bit.sum(bit.size) 以下
        """
        bit = self._make_bit_object(
            size=15, input_data=[5, 13, 7, 10, 2, 4, 11]
        )
        lub = bit.least_upper_bound(value=4)
        assert 7 == lub

    def test_find_max_value(self):
        """
        引数にbit.sum(bit.size)を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=15, input_data=[5, 15, 7, 10, 2, 4, 11]
        )
        lub = bit.least_upper_bound(value=7)
        assert 15 == lub
    
    def test_over_max_value(self):
        """
        引数にbit.sum(bit.size) 以上の値を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=15, input_data=[5, 15, 7, 10, 2, 4, 11]
        )
        lub = bit.least_upper_bound(value=16)
        assert -1 == lub

    def test_zero_value(self):
        """
        引数に0を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=15, input_data=[5, 15, 7, 10, 2, 4, 11]
        )
        lub = bit.least_upper_bound(value=0)
        assert 0 == lub

    def test_under_minimum_value(self):
        """
        引数に-1以下の値を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=15, input_data=[5, 15, 7, 10, 2, 4, 11]
        )
        lub = bit.least_upper_bound(value=-8)
        assert 0 == lub

    def test_set_duplicated_value(self):
        """
        引数に「一気に2以上sumの値が上がった場所」におさまる値を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=10, input_data=[2, 3, 6, 6, 7, 8, 8, 6, 10]
        )
        lub = bit.least_upper_bound(value=4)
        assert 6 == lub

    def test_random(self):
        """
        ランダムなデータセットに対して、ランダムな引数を設定した場合のテスト
        """
        bit = self._make_bit_object(
            size=30, 
            input_data=[18, 14, 10, 8, 1, 1, 8, 15, 26, 9, 11, 10, 5, 15]
        )
        lub = bit.least_upper_bound(value=12)
        assert 15 == lub

    def test_huge_target(self):
        """
        答えがindexの大きいものであるもののテスト
        """
        bit = self._make_bit_object(
            size=3000, input_data=[1720, 2998, 2999]
        )
        lub = bit.least_upper_bound(value=2)
        assert 2998 == lub


class TestBinaryIndexTree(unittest.TestCase):
    def _make_bit(self, values):
        bit = BinaryIndexTree(len(values))
        for index, value in enumerate(values, start=1):
            bit.add(index, value)
        return bit

    def _assert_matches_array(self, bit, values):
        # 探索は各要素が非負（累積和が単調非減少）の場合に検証する。
        prefixes = list(accumulate(values, initial=0))
        self.assertEqual(
            [bit.sum(i) for i in range(len(values) + 1)], prefixes
        )
        for target in range(-1, prefixes[-1] + 2):
            expected_lub = next(
                (i for i, total in enumerate(prefixes) if total >= target), -1
            )
            expected_glb = max(
                (i for i, total in enumerate(prefixes) if total <= target),
                default=-1,
            )
            with self.subTest(target=target):
                self.assertEqual(bit.least_upper_bound(target), expected_lub)
                self.assertEqual(bit.greatest_lower_bound(target), expected_glb)

    def test_bounds_with_zero_plateaus_and_gaps(self):
        """同じ累積和の左端・右端と、重みの間にある値を区別する。"""
        bit = self._make_bit([0, 0, 3, 0, 2, 0, 0])
        cases = [
            (-1, 0, -1),
            (0, 0, 2),
            (1, 3, 2),
            (2, 3, 2),
            (3, 3, 4),
            (4, 5, 4),
            (5, 5, 7),
            (6, -1, 7),
        ]
        for target, lub, glb in cases:
            with self.subTest(target=target):
                self.assertEqual(bit.least_upper_bound(target), lub)
                self.assertEqual(bit.greatest_lower_bound(target), glb)

    def test_empty_and_all_zero_trees(self):
        for size in (0, 1, 2, 7, 8, 9):
            with self.subTest(size=size):
                self._assert_matches_array(BinaryIndexTree(size), [0] * size)

    def test_single_element(self):
        self._assert_matches_array(self._make_bit([4]), [4])

    def test_sizes_around_powers_of_two(self):
        """探索開始のビット幅と、先頭・末尾の境界を検証する。"""
        for size in (2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33):
            for position in (0, size - 1):
                values = [0] * size
                values[position] = 3
                with self.subTest(size=size, position=position):
                    self._assert_matches_array(self._make_bit(values), values)

    def test_add_and_sum_with_signed_values(self):
        """sum は負の要素を含む場合も、各更新後に全区間で確認する。"""
        values = [0] * 5
        bit = BinaryIndexTree(len(values))
        for index, delta in ((1, 5), (5, 7), (3, -4), (1, -8), (5, 0), (3, 9)):
            bit.add(index, delta)
            values[index - 1] += delta
            with self.subTest(index=index, delta=delta):
                for end in range(len(values) + 1):
                    self.assertEqual(bit.sum(end), sum(values[:end]))

    def test_bounds_after_repeated_additions_and_removals(self):
        values = [0] * 8
        bit = BinaryIndexTree(len(values))
        updates = ((8, 4), (1, 2), (4, 3), (4, 2), (8, -4), (4, -5), (1, -2))
        for index, delta in updates:
            bit.add(index, delta)
            values[index - 1] += delta
            with self.subTest(index=index, delta=delta):
                self._assert_matches_array(bit, values)

    def test_exhaustive_small_arrays(self):
        """小さい配列の全組み合わせを線形探索の結果と比較する。"""
        for size in range(6):
            for values in product(range(3), repeat=size):
                with self.subTest(values=values):
                    self._assert_matches_array(self._make_bit(values), values)

    def test_random_updates_against_array(self):
        """固定シードで再現可能な更新列を検証する。削除後も要素は非負。"""
        random = Random(20260917)
        for size in (1, 7, 8, 9, 31, 32, 33):
            bit = BinaryIndexTree(size)
            values = [0] * size
            for step in range(50):
                index = random.randrange(size)
                delta = random.randint(-values[index], 5)
                values[index] += delta
                bit.add(index + 1, delta)
                with self.subTest(size=size, step=step, index=index, delta=delta):
                    self._assert_matches_array(bit, values)


if __name__ == "__main__":
    unittest.main()
