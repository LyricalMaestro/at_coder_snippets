
"""
[x^M] P(x) / Q(x) を高速に計算するためのアルゴリズム Q(0) != 0 となることが大前提。
L = max(deg(P), deg(Q))としたときに
O(LlogL * logM) で解くことができる

使用するときにはntt.pyのNTTを設定すること
"""

MOD = 998244353

class Bostan_Mori:

    def __init__(self, ntt):
        self.ntt = ntt

    def solve(self, target_deg: int, poly_p, poly_q):
        if target_deg == 0:
            return (poly_p[0] * pow(poly_q[0], MOD - 2, MOD)) % MOD

        neq_poly_q = []
        for i in range(len(poly_q)):
            if i % 2 == 0:
                neq_poly_q.append(poly_q[i])
            else:
                neq_poly_q.append((- poly_q[i]) % MOD)
        
        poly = self.ntt.convolution(poly_p, neq_poly_q)
        poly2 = self.ntt.convolution(poly_q, neq_poly_q)
        
        if target_deg % 2 == 0:
            new_poly_p = []
            i = 0
            while i < len(poly):
                new_poly_p.append(poly[i])
                i += 2
            if len(new_poly_p) == 0:
                new_poly_p.append(0)

            new_poly_q = []
            i = 0
            while i < len(poly2):
                new_poly_q.append(poly2[i])
                i += 2
            
            return self.solve(target_deg // 2, new_poly_p, new_poly_q)
        else:
            new_poly_p = []
            i = 1
            while i < len(poly):
                new_poly_p.append(poly[i])
                i += 2
            if len(new_poly_p) == 0:
                new_poly_p.append(0)

            new_poly_q = []
            i = 0
            while i < len(poly2):
                new_poly_q.append(poly2[i])
                i += 2
            
            return self.solve((target_deg - 1) // 2, new_poly_p, new_poly_q)
