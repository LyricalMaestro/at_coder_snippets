/// 1-indexed Fenwick Tree for integer sums.
///
/// `least_upper_bound` and `greatest_lower_bound` require all point values to
/// be non-negative so that prefix sums are monotonic.
///
/// Source: https://github.com/LyricalMaestro/at_coder_snippets
pub struct BinaryIndexTree {
    size: usize,
    tree: Vec<i64>,
}

impl BinaryIndexTree {
    pub fn new(size: usize) -> Self {
        Self {
            size,
            tree: vec![0; size + 1],
        }
    }

    pub fn add(&mut self, index: usize, delta: i64) {
        assert!((1..=self.size).contains(&index));
        let mut i = index;
        while i <= self.size {
            self.tree[i] += delta;
            i += i & i.wrapping_neg();
        }
    }

    /// Returns the sum of indices `1..=index`. `sum(0)` is zero.
    pub fn sum(&self, index: usize) -> i64 {
        assert!(index <= self.size);
        let mut i = index;
        let mut result = 0;
        while i > 0 {
            result += self.tree[i];
            i -= i & i.wrapping_neg();
        }
        result
    }

    /// Returns the smallest index whose prefix sum is at least `value`.
    ///
    /// Returns `0` when `value <= 0`, and `None` when no index satisfies it.
    pub fn least_upper_bound(&self, value: i64) -> Option<usize> {
        if self.sum(self.size) < value {
            return None;
        }
        if value <= 0 {
            return Some(0);
        }

        let mut bit = 1;
        while bit <= self.size / 2 {
            bit <<= 1;
        }

        let mut index = 0;
        let mut prefix = 0;
        while bit > 0 {
            let next = index + bit;
            if next <= self.size && prefix + self.tree[next] < value {
                prefix += self.tree[next];
                index = next;
            }
            bit >>= 1;
        }
        Some(index + 1)
    }

    /// Returns the largest index whose prefix sum is at most `value`.
    ///
    /// Index zero has a prefix sum of zero. Returns `None` when `value < 0`.
    pub fn greatest_lower_bound(&self, value: i64) -> Option<usize> {
        if value < 0 {
            return None;
        }

        let mut bit = 1;
        while bit <= self.size / 2 {
            bit <<= 1;
        }

        let mut index = 0;
        let mut prefix = 0;
        while bit > 0 {
            let next = index + bit;
            if next <= self.size && prefix + self.tree[next] <= value {
                prefix += self.tree[next];
                index = next;
            }
            bit >>= 1;
        }
        Some(index)
    }
}
