use at_coder_snippets::snippets::binary_index_tree::BinaryIndexTree;
use at_coder_snippets::snippets::combination::CombinationCalculator;
use at_coder_snippets::snippets::pow::pow_mod;

#[test]
fn fenwick_tree_supports_updates_and_prefix_bounds() {
    let mut tree = BinaryIndexTree::new(7);
    for (index, value) in [(3, 3), (5, 2)] {
        tree.add(index, value);
    }

    assert_eq!(tree.sum(0), 0);
    assert_eq!(tree.sum(4), 3);
    assert_eq!(tree.sum(7), 5);
    assert_eq!(tree.least_upper_bound(4), Some(5));
    assert_eq!(tree.least_upper_bound(6), None);
    assert_eq!(tree.greatest_lower_bound(3), Some(4));
    assert_eq!(tree.greatest_lower_bound(-1), None);

    tree.add(3, -3);
    assert_eq!(tree.sum(7), 2);
}

#[test]
fn combination_calculator_handles_valid_and_invalid_ranges() {
    let calculator = CombinationCalculator::new(10, 1_000_000_007);
    assert_eq!(calculator.calc_combination(5, 2), 10);
    assert_eq!(calculator.calc_combination(8, 0), 1);
    assert_eq!(calculator.calc_combination(4, 5), 0);
    assert_eq!(calculator.calc_permutation(5, 2), 20);
    assert_eq!(calculator.calc_permutation(4, 5), 0);
}

#[test]
fn modular_power_handles_large_values_and_zero_exponent() {
    assert_eq!(pow_mod(2, 10, 1_000), 24);
    assert_eq!(pow_mod(u64::MAX, 0, 7), 1);
    assert_eq!(pow_mod(123, 10, 1), 0);
}
