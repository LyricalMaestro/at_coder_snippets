import os
import pathlib
import sys
from fractions import Fraction
from random import Random

import pytest

src_path = pathlib.Path(os.path.dirname(__file__)).parent.joinpath("src")
sys.path.append(str(src_path))

from rational_sort import sort_rationals


class TestSortRationals:
    def test_empty_and_single_element(self):
        assert sort_rationals([], 1) == []
        assert sort_rationals([(3, 2)], 3) == [(3, 2)]

    def test_sorts_by_first_two_values_and_preserves_remaining_values(self):
        values = [(3, 1, "third", "fourth"), (2, 1, "extra"), (5, 1, "last")]
        assert sort_rationals(values, 5) == [
            (5, 1, "last"),
            (3, 1, "third", "fourth"),
            (2, 1, "extra"),
        ]

    def test_orders_fractions_signs_and_infinities_stably(self):
        values = [
            (0, 1),
            (2, 1),
            (-3, 1),
            (3, -1),
            (1, 0),
            (-1, 0),
            (2, -1),
            (4, 2),
            (0, -1),
        ]
        expected = [
            (0, -1),
            (2, -1),
            (-3, 1),
            (3, -1),
            (1, 0),
            (-1, 0),
            (2, 1),
            (4, 2),
            (0, 1),
        ]

        # 分母が0の値は符号付き無限大として扱い、同値の有限小数は入力順を保つ。
        result = sort_rationals(values, 4)
        assert result == expected
        assert values[0] == (0, 1)

    @pytest.mark.parametrize("max_value", [10**9, 10**18])
    def test_distinguishes_close_fractions_at_supported_bounds(self, max_value):
        values = [(max_value - 1, 1), (max_value, 1)]
        assert sort_rationals(values, max_value) == [
            (max_value, 1),
            (max_value - 1, 1),
        ]

    def test_matches_fraction_order_with_large_signed_coefficients(self):
        max_value = 10**18
        values = [
            (max_value, max_value - 1),
            (-max_value + 1, max_value),
            (max_value - 1, max_value),
            (-max_value, max_value - 1),
            (max_value, -max_value + 1),
            (max_value, max_value - 1),
        ]
        expected = sorted(
            values,
            key=lambda pair: Fraction(pair[1], pair[0]),
        )
        assert sort_rationals(values, max_value) == expected

    def test_randomized_results_match_fraction(self):
        random = Random(20261025)
        max_value = 10**9
        values = [
            (random.choice((-1, 1)) * random.randint(1, max_value),
             random.randint(-max_value, max_value))
            for _ in range(1000)
        ]
        expected = sorted(values, key=lambda pair: Fraction(pair[1], pair[0]))
        assert sort_rationals(values, max_value) == expected

    @pytest.mark.parametrize(
        ("values", "max_value"),
        [([], 0), ([(1, 2)], 1), ([(2, 1)], 1)],
    )
    def test_rejects_coefficients_outside_declared_bound(self, values, max_value):
        with pytest.raises(ValueError):
            sort_rationals(values, max_value)
