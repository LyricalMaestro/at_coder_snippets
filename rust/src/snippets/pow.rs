/// Computes `base.pow(exponent) % modulus` using binary exponentiation.
///
/// `modulus` must be positive.
///
/// Source: https://github.com/LyricalMaestro/at_coder_snippets
pub fn pow_mod(mut base: u64, mut exponent: u64, modulus: u64) -> u64 {
    assert!(modulus > 0);
    base %= modulus;

    let mut result = 1 % modulus;
    while exponent > 0 {
        if exponent & 1 == 1 {
            result = ((result as u128 * base as u128) % modulus as u128) as u64;
        }
        base = ((base as u128 * base as u128) % modulus as u128) as u64;
        exponent >>= 1;
    }
    result
}
