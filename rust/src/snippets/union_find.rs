// Source: https://github.com/LyricalMaestro/at_coder_rust/blob/main/src/snippets/union_find.rs

pub struct UnionFind {
    root: Vec<usize>,
    size: Vec<usize>,
}

impl UnionFind {
    pub fn new(n: usize) -> Self {
        Self {
            root: (0..n).collect(),
            size: vec![1; n],
        }
    }
}

pub struct RollbackUnionFind {
    root: Vec<usize>,
    size: Vec<usize>,
    history: Vec<(usize, usize, usize)>,
}

impl RollbackUnionFind {
    pub fn new(n: usize) -> Self {
        Self {
            root: (0..n).collect(),
            size: vec![1; n],
            history: Vec::new(),
        }
    }

    pub fn get_root(&self, v: usize) -> usize {
        if v == self.root[v] {
            v
        } else {
            self.get_root(self.root[v])
        }
    }

    pub fn merge(&mut self, u: usize, v: usize) -> bool {
        let root_u = self.get_root(u);
        let root_v = self.get_root(v);
        if root_u == root_v {
            return false;
        }

        self.history
            .push((root_u, self.root[root_u], self.size[root_u]));
        self.history
            .push((root_v, self.root[root_v], self.size[root_v]));

        if self.size[root_u] >= self.size[root_v] {
            self.size[root_u] += self.size[root_v];
            self.root[root_v] = root_u;
        } else {
            self.size[root_v] += self.size[root_u];
            self.root[root_u] = root_v;
        }
        true
    }

    pub fn rollback(&mut self) {
        if let Some((v, root_v, size_v)) = self.history.pop() {
            self.root[v] = root_v;
            self.size[root_v] = size_v;

            let (u, root_u, size_u) = self.history.pop().expect("incomplete merge history");
            self.root[u] = root_u;
            self.size[root_u] = size_u;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{RollbackUnionFind, UnionFind};

    #[test]
    fn union_find_merges_components_and_rejects_repeated_merges() {
        let mut uf = UnionFind::new(5);
        assert!(uf.merge(1, 2));
        assert!(uf.merge(3, 1));
        assert!(!uf.merge(2, 3));
        assert_eq!(uf.get_root(1), uf.get_root(2));
        assert_eq!(uf.get_root(2), uf.get_root(3));
        assert_ne!(uf.get_root(0), uf.get_root(1));
    }

    #[test]
    fn rollback_union_find_constructor_matches_python() {
        let uf = RollbackUnionFind::new(10);
        assert_eq!(uf.root, (0..10).collect::<Vec<_>>());
        assert_eq!(uf.size, vec![1; 10]);
    }

    #[test]
    fn rollback_union_find_merges_equal_sized_components() {
        let mut uf = RollbackUnionFind::new(10);
        assert!(uf.merge(1, 2));
        assert_eq!(uf.root, vec![0, 1, 1, 3, 4, 5, 6, 7, 8, 9]);
        assert_eq!(uf.size, vec![1, 2, 1, 1, 1, 1, 1, 1, 1, 1]);
        assert_eq!(uf.get_root(1), 1);
        assert_eq!(uf.get_root(2), 1);
    }

    #[test]
    fn rollback_union_find_merges_components_of_different_sizes() {
        let mut uf = RollbackUnionFind::new(10);
        uf.merge(1, 2);
        assert!(uf.merge(1, 3));
        assert_eq!(uf.root, vec![0, 1, 1, 1, 4, 5, 6, 7, 8, 9]);
        assert_eq!(uf.size, vec![1, 3, 1, 1, 1, 1, 1, 1, 1, 1]);

        let mut uf = RollbackUnionFind::new(10);
        uf.merge(1, 2);
        assert!(uf.merge(3, 1));
        assert_eq!(uf.root, vec![0, 1, 1, 1, 4, 5, 6, 7, 8, 9]);
        assert_eq!(uf.size, vec![1, 3, 1, 1, 1, 1, 1, 1, 1, 1]);
        assert_eq!(uf.get_root(1), 1);
        assert_eq!(uf.get_root(3), 1);
    }

    fn make_merged_rollback_union_find() -> RollbackUnionFind {
        let mut uf = RollbackUnionFind::new(10);
        uf.merge(1, 2);
        uf.merge(3, 4);
        uf.merge(4, 5);
        uf.merge(6, 5);
        uf.merge(1, 8);
        uf.merge(2, 6);
        uf
    }

    #[test]
    fn rollback_union_find_rejects_merges_with_the_same_root() {
        let mut uf = RollbackUnionFind::new(10);
        uf.merge(1, 2);
        uf.merge(3, 1);
        assert!(!uf.merge(3, 2));
        assert_eq!(uf.root, vec![0, 1, 1, 1, 4, 5, 6, 7, 8, 9]);
        assert_eq!(uf.size, vec![1, 3, 1, 1, 1, 1, 1, 1, 1, 1]);
        assert_eq!(uf.get_root(2), 1);
        assert_eq!(uf.get_root(3), 1);
    }

    #[test]
    fn rollback_union_find_builds_the_same_forest_as_python() {
        let uf = make_merged_rollback_union_find();
        assert_eq!(uf.root, vec![0, 3, 1, 3, 3, 3, 3, 7, 1, 9]);
        assert_eq!(uf.size, vec![1, 3, 1, 7, 1, 1, 1, 1, 1, 1]);
    }

    #[test]
    fn rollback_union_find_reverts_one_successful_merge() {
        let mut uf = make_merged_rollback_union_find();
        uf.rollback();
        assert_eq!(uf.root, vec![0, 1, 1, 3, 3, 3, 3, 7, 1, 9]);
        assert_eq!(uf.size, vec![1, 3, 1, 4, 1, 1, 1, 1, 1, 1]);
        assert_eq!(uf.get_root(2), 1);
        assert_eq!(uf.get_root(6), 3);
    }

    #[test]
    fn rollback_union_find_ignores_rollback_without_history() {
        let mut uf = RollbackUnionFind::new(10);
        uf.rollback();
        assert_eq!(uf.root, (0..10).collect::<Vec<_>>());
        assert_eq!(uf.size, vec![1; 10]);
    }

    #[test]
    fn rollback_union_find_can_merge_after_rollback() {
        let mut uf = make_merged_rollback_union_find();
        uf.rollback();
        assert!(uf.merge(2, 7));
        assert_eq!(uf.root, vec![0, 1, 1, 3, 3, 3, 3, 1, 1, 9]);
        assert_eq!(uf.size, vec![1, 4, 1, 4, 1, 1, 1, 1, 1, 1]);
        assert_eq!(uf.get_root(2), 1);
        assert_eq!(uf.get_root(7), 1);
    }
}

impl UnionFind {
    pub fn get_root(&mut self, v: usize) -> usize {
        if v == self.root[v] {
            v
        } else {
            self.root[v] = self.get_root(self.root[v]);
            self.root[v]
        }
    }

    pub fn merge(&mut self, u: usize, v: usize) -> bool {
        let root_u = self.get_root(u);
        let root_v = self.get_root(v);
        if root_u == root_v {
            return false;
        }

        if self.size[root_u] >= self.size[root_v] {
            self.size[root_u] += self.size[root_v];
            self.root[root_v] = root_u;
        } else {
            self.size[root_v] += self.size[root_u];
            self.root[root_u] = root_v;
        }
        true
    }
}
