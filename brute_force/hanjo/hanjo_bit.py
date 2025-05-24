def calc_hanjo(H: int, W: int, idx: int, A: int, B: int, used: int):
    if idx == H * W:
        return 1
    h, w = divmod(idx, W)
    res = 0
    # 1x1を置く場合
    if not ((1 << idx) & used) and B > 0:
        res += calc_hanjo(H, W, idx + 1, A, B - 1, used | (1 << idx))
    # 1x2を置く場合
    if w + 1 < W and not (used >> (idx + 1)) & 1 and not (used >> idx) & 1 and A > 0:
        res += calc_hanjo(H, W, idx + 1, A - 1, B, used | (1 << idx) | (1 << idx + 1))
    # 2x1を置く場合
    if h + 1 < H and not (used >> (idx + W)) & 1 and not (used >> idx) & 1 and A > 0:
        res += calc_hanjo(H, W, idx + 1, A - 1, B, used | (1 << idx) | (1 << idx + W))
    # 既に入っていて置けない場合
    if (used >> idx) & 1:
        res += calc_hanjo(H, W, idx + 1, A, B, used)
    return res


# == Example ABC196D
H, W, A, B = [int(l) for l in input().split()]
print(calc_hanjo(H, W, 0, A, B, 0))
