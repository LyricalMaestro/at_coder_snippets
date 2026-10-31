
from typing import List, Callable, TypeVar

T = TypeVar('T')

class SparseTable:

    def __init__(self, array: List[T], func: Callable[[T, T], T]):
        self.n = len(array)
        self.func = func
        self.k = self.n.bit_length() - 1
        self.table = [[None for _ in range(self.n)] for _ in range(self.k + 1)]
        
        for i in range(self.n):
            self.table[0][i] = array[i]
        
        for k in range(1, self.k + 1):
            for i in range(self.n - (1 << k) + 1):
                self.table[k][i] = self.func(self.table[k - 1][i], self.table[k - 1][i + (1 << (k - 1))])

    def query(self, l: int, r: int) -> T:
        j = (r - l + 1).bit_length() - 1
        return self.func(self.table[j][l], self.table[j][r - (1 << j) + 1])
