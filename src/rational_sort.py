def sort_rationals(coef_list, MAX_ABS_VALUE):
    """
    各要素の先頭2項を (分母, 分子) とみなし、有理数の値で昇順に並べる。

    Farey列の性質から、分母の絶対値が MAX_ABS_VALUE 以下である
    異なる有理数どうしの差には、1 / MAX_ABS_VALUE**2 以上という下限がある。
    そのため、分子に MAX_ABS_VALUE**2 + 1 を掛けて整数キーを作ることで、
    有理数の大小関係を正確に保ったままソートできる。
    浮動小数点数への変換は行わないため、丸め誤差も生じない。

    分母と分子の絶対値は、どちらも MAX_ABS_VALUE 以下である必要がある。
    分母が 0 の場合は、分子の符号に応じて負または正の無限大として扱う。
    """
    if MAX_ABS_VALUE < 1:
        raise ValueError("MAX_ABS_VALUE must be at least 1")

    scale = MAX_ABS_VALUE * MAX_ABS_VALUE + 1
    infinity_key = MAX_ABS_VALUE * scale + 1

    def key(coef):
        denominator, numerator = coef[0], coef[1]
        if abs(denominator) > MAX_ABS_VALUE or abs(numerator) > MAX_ABS_VALUE:
            raise ValueError("coefficient exceeds MAX_ABS_VALUE")

        if denominator == 0:
            return infinity_key if numerator > 0 else -infinity_key
        if denominator < 0:
            denominator = -denominator
            numerator = -numerator
        return numerator * scale // denominator

    result = list(coef_list)
    result.sort(key=key)
    return result
