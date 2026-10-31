use super::pow::pow_mod;

/// Factorial-based permutation and combination calculator.
///
/// `modulus` must be prime and greater than `max_n`.
///
/// Source: https://github.com/LyricalMaestro/at_coder_snippets
pub struct CombinationCalculator {
    max_n: usize,
    modulus: u64,
    factorial: Vec<u64>,
    inverse_factorial: Vec<u64>,
}

impl CombinationCalculator {
    pub fn new(max_n: usize, modulus: u64) -> Self {
        assert!(modulus >= 2);
        assert!((max_n as u128) < modulus as u128);

        let mut factorial = vec![1; max_n + 1];
        for n in 1..=max_n {
            factorial[n] = (factorial[n - 1] as u128 * n as u128 % modulus as u128) as u64;
        }

        let mut inverse_factorial = vec![1; max_n + 1];
        inverse_factorial[max_n] = pow_mod(factorial[max_n], modulus - 2, modulus);
        for n in (0..max_n).rev() {
            inverse_factorial[n] =
                (inverse_factorial[n + 1] as u128 * (n + 1) as u128 % modulus as u128) as u64;
        }

        Self {
            max_n,
            modulus,
            factorial,
            inverse_factorial,
        }
    }

    pub fn calc_combination(&self, n: usize, r: usize) -> u64 {
        assert!(n <= self.max_n);
        if r > n {
            return 0;
        }

        let result = self.factorial[n] as u128 * self.inverse_factorial[r] as u128
            % self.modulus as u128
            * self.inverse_factorial[n - r] as u128
            % self.modulus as u128;
        result as u64
    }

    pub fn calc_permutation(&self, n: usize, r: usize) -> u64 {
        assert!(n <= self.max_n);
        if r > n {
            return 0;
        }

        (self.factorial[n] as u128 * self.inverse_factorial[n - r] as u128 % self.modulus as u128)
            as u64
    }
}
