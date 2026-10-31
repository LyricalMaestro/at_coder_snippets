class BinaryIndexTree:
    """
    フェニック木(Binary Indexed Tree / Fenwick Tree)
    """

    def __init__(self, size):
        self.size = size
        self.array = [0] * (size + 1)

    def add(self, x, a):
        index = x
        while index <= self.size:
            self.array[index] += a
            index += index & (-index)

    def sum(self, x):
        index = x
        ans = 0
        while index > 0:
            ans += self.array[index]
            index -= index & (-index)
        return ans

    def least_upper_bound(self, value):
        """
        sum(i) >= value を満たす最小の index i を返す。

        すなわち

            min { i | sum(i) >= value }

        を求める。

        条件を満たす index が存在しない場合は -1 を返す。
        """

        if self.sum(self.size) < value:
            return -1
        elif value <= 0:
            return 0

        m = 1
        while (m << 1) <= self.size:
            m <<= 1

        k = 0
        k_sum = 0

        while m > 0:
            k0 = k + m
            if k0 <= self.size:
                if k_sum + self.array[k0] < value:
                    k_sum += self.array[k0]
                    k = k0
            m >>= 1

        return k + 1

    def greatest_lower_bound(self, value):
        """
        sum(i) <= value を満たす最大の index i を返す。

        すなわち

            max { i | sum(i) <= value }

        を求める。

        index 0 について sum(0) = 0 と考える。

        value < 0 の場合は条件を満たす index が存在しないため
        -1 を返す。
        """

        if value < 0:
            return -1

        m = 1
        while (m << 1) <= self.size:
            m <<= 1

        k = 0
        k_sum = 0

        while m > 0:
            k0 = k + m
            if k0 <= self.size:
                if k_sum + self.array[k0] <= value:
                    k_sum += self.array[k0]
                    k = k0
            m >>= 1

        return k