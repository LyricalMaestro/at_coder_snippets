import os
import pathlib
import sys
from typing import List

src_path = pathlib.Path(os.path.dirname(__file__)).parent.joinpath("src")
sys.path.append(str(src_path))

from manacher import Manacher, ManacherResult


class TestManacher:
    """
    Manacherクラスのテスト
    """

    def test_odd_length_string(self):
        """
        奇数長文字列 ("abaca")
        rad_odd  = [1, 2, 1, 2, 1]      → 最長奇数長: "aba" or "aca" (長さ 3), sum=7
        rad_even = [0, 0, 0, 0, 0, 0]   → 偶数長回文なし, sum=0
        回文: 'a','b','aba','a','aca','c','a' (計7個)
        """
        manacher = Manacher()
        result: ManacherResult = manacher.solve("abaca")

        assert result.get_max_palindrome_length() == 3
        assert result.get_palindrome_count() == 7

    def test_even_length_string(self):
        """
        偶数長文字列 ("abaaba")
        rad_odd  = [1, 2, 1, 1, 2, 1]      → sum=8
        rad_even = [0, 0, 0, 3, 0, 0, 0]   → 最長偶数長: "abaaba" (長さ 6), sum=3
        回文: 'a','b','aba','a','a','aba','b','a','aa','baab','abaaba' (計11個)
        """
        manacher = Manacher()
        result: ManacherResult = manacher.solve("abaaba")

        assert result.get_max_palindrome_length() == 6
        assert result.get_palindrome_count() == 11

    def test_length_1_string(self):
        """
        長さ1の文字列 ("a")
        rad_odd  = [1]    → 最長: "a" (長さ 1)
        rad_even = [0, 0]
        回文: 'a' (計1個)
        """
        manacher = Manacher()
        result: ManacherResult = manacher.solve("a")

        assert result.get_max_palindrome_length() == 1
        assert result.get_palindrome_count() == 1

    def test_length_2_palindrome_string(self):
        """
        長さ2の回文文字列 ("zz")
        rad_odd  = [1, 1]    → sum=2
        rad_even = [0, 1, 0] → 最長: "zz" (長さ 2), sum=1
        回文: 'z','z','zz' (計3個)
        """
        manacher = Manacher()
        result: ManacherResult = manacher.solve("zz")

        assert result.get_max_palindrome_length() == 2
        assert result.get_palindrome_count() == 3

    def test_length_2_non_palindrome_string(self):
        """
        長さ2の非回文文字列 ("ac")
        rad_odd  = [1, 1]    → 最長: "a" or "c" (長さ 1)
        rad_even = [0, 0, 0]
        回文: 'a','c' (計2個)
        """
        manacher = Manacher()
        result: ManacherResult = manacher.solve("ac")

        assert result.get_max_palindrome_length() == 1
        assert result.get_palindrome_count() == 2

    def test_all_same_characters_string(self):
        """
        全文字が同じ文字列 ("aaaa")
        rad_odd  = [1, 2, 2, 1]    → 最長奇数長: "aaa" (長さ 3), sum=6
        rad_even = [0, 1, 2, 1, 0] → 最長偶数長: "aaaa" (長さ 4), sum=4
        回文: a,a,a,a,aa,aa,aa,aaa,aaa,aaaa (計10個)
        """
        manacher = Manacher()
        result: ManacherResult = manacher.solve("aaaa")

        assert result.get_max_palindrome_length() == 4
        assert result.get_palindrome_count() == 10

    def test_non_negative_int_sequence_odd_palindrome(self):
        """
        非負整数列 (奇数長回文を含む, [1, 2, 1])
        区切り文字を -1 に指定
        rad_odd  = [1, 2, 1]    → 最長: [1,2,1] (長さ 3), sum=4
        rad_even = [0, 0, 0, 0]
        回文: [1],[2],[1],[1,2,1] (計4個)
        """
        manacher = Manacher(seperator=-1)
        result: ManacherResult = manacher.solve([1, 2, 1])

        assert result.get_max_palindrome_length() == 3
        assert result.get_palindrome_count() == 4

    def test_non_negative_int_sequence_even_palindrome(self):
        """
        非負整数列 (偶数長回文を含む, [1, 2, 2, 1])
        区切り文字を -1 に指定
        rad_odd  = [1, 1, 1, 1]       → sum=4
        rad_even = [0, 0, 2, 0, 0]    → 最長: [1,2,2,1] (長さ 4), sum=2
        回文: [1],[2],[2],[1],[2,2],[1,2,2,1] (計6個)
        """
        manacher = Manacher(seperator=-1)
        result: ManacherResult = manacher.solve([1, 2, 2, 1])

        assert result.get_max_palindrome_length() == 4
        assert result.get_palindrome_count() == 6

    def test_non_negative_int_sequence_length_1(self):
        """
        長さ1の非負整数列 ([5])
        """
        manacher = Manacher(seperator=-1)
        result: ManacherResult = manacher.solve([5])

        assert result.get_max_palindrome_length() == 1
        assert result.get_palindrome_count() == 1

    def test_non_negative_int_sequence_length_2_palindrome(self):
        """
        長さ2で回文の非負整数列 ([7, 7])
        """
        manacher = Manacher(seperator=-1)
        result: ManacherResult = manacher.solve([7, 7])

        assert result.get_max_palindrome_length() == 2
        assert result.get_palindrome_count() == 3

    def test_non_negative_int_sequence_length_2_non_palindrome(self):
        """
        長さ2で非回文の非負整数列 ([0, 100])
        """
        manacher = Manacher(seperator=-1)
        result: ManacherResult = manacher.solve([0, 100])

        assert result.get_max_palindrome_length() == 1
        assert result.get_palindrome_count() == 2
