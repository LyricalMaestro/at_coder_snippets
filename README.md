
# AtCoder Snippets

AtCoderなどの競技プログラミングで使うアルゴリズム・データ構造のスニペット集です。
言語ごとにプロジェクトを分けています。

## Python

Pythonのソースとテストは [`python/`](./python/) にあります。

```sh
cd python
uv sync
uv run pytest
```

## Rust

RustのCargo crateとスニペットは [`rust/`](./rust/) にあります。

```sh
cargo test --manifest-path rust/Cargo.toml
```

現在のRustスニペット:

- `binary_index_tree`: 1-indexed Fenwick Tree
- `combination`: 素数moduloでの順列・組み合わせ
- `pow`: modular exponentiation

## AtCoderの生成AIルール

ABC・ARC・AGCの開催中は生成AIの利用が原則禁止です。開催前に生成AIを用いて作成したコードをコンテストで使う場合は、開催前にコードを第三者が確認できる形で公開し、提出コードに参照URLを記載する必要があります。

このリポジトリのRustスニペットをコンテストで使う場合も、事前にリポジトリを公開し、コピーしたコードの提出に次のURLを含めてください。

```text
https://github.com/LyricalMaestro/at_coder_snippets
```

公開と参照URLの条件を満たすまでは、開催中のABC・ARC・AGCでは使用しないでください。詳細は[AtCoderの生成AIルール](https://info.atcoder.jp/entry/llm-rules-ja)を確認してください。
