from typing import Optional

def calc_gcd(A, B):
    """
    正の整数A, Bの最大公約数を計算する
    """
    a = max(A, B)
    b = min(A, B)
    while a % b > 0:
        c = a % b
        a = b
        b = c
    return b

def ext_euclide(X, Y):
    """
    拡張ユークリッド互除法を実行する。
    a * X + b * Y = 1 を満たすa, bを取得する
    X, Yの満たすべき前提として
    ・gcd(X, Y) = 1
    ・X > Y
    ・X > 0, Y > 0
    """
    if Y == 1:
        return 0, 1

    a, b = ext_euclide(Y, X % Y)
    return b, a - b * (X // Y)


class ChaineseRemainderTheorem:
    def __init__(self, X: int, Y: int):
        self.gcd = calc_gcd(X, Y)
        a, b = ext_euclide(X // self.gcd, Y // self.gcd)
        self.a = a
        self.b = b
        
        x = X // self.gcd
        y = Y // self.gcd
        self.lcm = x * y * self.gcd


    def solve(self, p: int, q: int) -> Optional[int]:
        """
        m = p (mod X)
        m = q (mod Y)
        となるmを求める
        """    
        if (p - q) % self.gcd > 0:
            return None

        s = (q - p) // self.gcd
        m = p + s * self.a * self.X
        m = m % self.lcm
        return m
