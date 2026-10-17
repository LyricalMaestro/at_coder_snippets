# 数論変換パートは
# https://qiita.com/AngrySadEight/items/0dfde26060daaf6a2fda
# と
# https://qiita.com/izu_nori/items/1c5cdef0500ffa0276f5
# を参考にしました

MOD = 998244353


class NTT:

    def __init__(self):
        self._root = self._make_root()
        self._invroot = self._make_invroot(self._root)

    def _reverse_bits(self, n):
        n = (n >> 16) | (n << 16)
        n = ((n & 0xff00ff00) >> 8) | ((n & 0x00ff00ff) << 8)
        n = ((n & 0xf0f0f0f0) >> 4) | ((n & 0x0f0f0f0f) << 4)
        n = ((n & 0xcccccccc) >> 2) | ((n & 0x33333333) << 2)
        n = ((n & 0xaaaaaaaa) >> 1) | ((n & 0x55555555) << 1)
        return n

    def _make_root(self):
        # 3はMODの原始根, 119乗するとconvolusion, NTT における「基底」の条件を満たす
        r = pow(3, 119, MOD)
        return [pow(r, 2 ** i, MOD) for i in range(23, -1, -1)]
    
    def _make_invroot(self, root):
        invroot = []
        for i in range(len(root)):
            invroot.append(pow(root[i], MOD - 2, MOD))
        return invroot
    
    def _ntt(self, poly, root, rev, max_l):
        n = len(poly)
        k = (n - 1).bit_length()
        step = (max_l) >> k

        for i, j in enumerate(rev[::step]):
            if i < j:
                poly[i], poly[j] = poly[j], poly[i]

        r = 1
        for w in root[1:(k + 1)]:
            for l in range(0, n, r * 2):
                wi = 1
                for i in range(r):
                    a = (poly[l + i + r] * wi) % MOD
                    a += poly[l + i]
                    a %= MOD

                    b = (-poly[l + i + r] * wi) % MOD
                    b += poly[l + i]
                    b %= MOD

                    poly[l + i] = a
                    poly[l + i + r] = b
                    wi *= w
                    wi %= MOD
            r <<= 1


    def convolution(self, poly_l, poly_r):
        # 多項式を畳み込んだ時の次数よりも大きい2の冪の長さを求める
        # (NTTの特性上2の冪乗に乗せるため)
        len_ans = len(poly_l) + len(poly_r) - 1
        if (min(len(poly_l), len(poly_r)) <= 40):
            return self._combolution_light(poly_l, poly_r)

        # 2の冪の長さを求める
        n = 1
        max_depth = 0
        while n <= len_ans:
            n *= 2
            max_depth += 1
        rev = [self._reverse_bits(i) >> (32- max_depth) for i in range(n)]
        
        new_poly_l = [0] * n
        for i in range(len(poly_l)):
            new_poly_l[i] = poly_l[i]
        new_poly_r = [0] * n
        for i in range(len(poly_r)):
            new_poly_r[i] = poly_r[i]

        # 数論変換
        self._ntt(new_poly_l, self._root, rev, n)
        self._ntt(new_poly_r, self._root, rev, n)

        # 畳み込みは各iを代入した値の積で求められる
        d_ans = [0] * n
        for i in range(n):
            d_ans[i] = (new_poly_l[i] * new_poly_r[i]) % MOD

        # 逆数論変換
        self._ntt(d_ans, self._invroot, rev, n)

        # 最後の定数分割る処理
        inv_n = pow(n, MOD - 2, MOD)
        poly_ans = [0] * len_ans
        for i in range(len_ans):
            poly_ans[i] = (d_ans[i] * inv_n) % MOD
        return poly_ans

    def _combolution_light(self, poly_l, poly_r):
        poly_ans = [0] * (len(poly_l) + len(poly_r) - 1)
        for i in range(len(poly_l)):
            for j in range(len(poly_r)):
                poly_ans[i + j] += (poly_l[i] * poly_r[j]) % MOD
                poly_ans[i + j] %= MOD
        return poly_ans
    