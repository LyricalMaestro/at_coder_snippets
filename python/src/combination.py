
class CombinationCalculator:
    """
    modを考慮したPermutation, Combinationを計算するためのクラス
    """    
    def __init__(self, size, mod):
        self.mod = mod
        self.factorial = [0] * (size + 1)
        self.factorial[0] = 1
        for i in range(1, size + 1):
            self.factorial[i] = (i * self.factorial[i - 1]) % self.mod
        
        self.inv_factorial = [0] * (size + 1)
        self.inv_factorial[size] = pow(self.factorial[size], self.mod - 2, self.mod)

        for i in reversed(range(size)):
            self.inv_factorial[i] = ((i + 1) * self.inv_factorial[i + 1]) % self.mod

    def calc_combination(self, n, r):
        if n < 0 or n < r or r < 0:
            return 0

        if r == 0 or n == r:
            return 1
        
        ans = self.inv_factorial[n - r] * self.inv_factorial[r]
        ans %= self.mod
        ans *= self.factorial[n]
        ans %= self.mod
        return ans
    
    def calc_permutation(self, n, r):
        if n < 0 or n < r:
            return 0

        ans = self.inv_factorial[n - r]
        ans *= self.factorial[n]
        ans %= self.mod
        return ans
        