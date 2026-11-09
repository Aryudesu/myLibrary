# math

## mod/inverse_mod

modについての逆数の計算を行う基本的関数

## mod/modQ

有理数modについてのクラス
基本的な四則演算と整数冪については実装．

## prime/divisor

約数の計算を行うもの

## prime/erats

エラトステネスの篩

## prime/osa_k

osa_k法

## prime/prime

素数表を元に色々操作をするためのもの

## ./matrix

行列

## ./ex_euclid

拡張ユークリッドの互除法

## ./ramanujan_tau

ラマヌジャンのタウ関数

## ./XorBasis

非負整数の部分集合 XOR を管理する線形基底クラス。

- `add(x)`: 要素を追加（線形独立なら True）
- `can_make(x)`: XOR 値 `x` を作れるか判定
- `max_xor(x=0)` / `min_xor(x=0)`: `x XOR y` の最大・最小値
- `rank` / `count_distinct()`: ランクと異なる XOR 値の個数
- `count_ways(x)`: XOR が `x` になる元の要素の部分集合数
- `enumerate_xors()`: 異なる XOR 値を全列挙（数値順とは限らない）
- `merge(other)`: 2 つの基底を結合（新しいインスタンスを返す）

`add`・`can_make` などは O(bit_width)、全列挙は O(2^rank)。
`count_ways` は線形従属な元の要素数も含めて数える。
