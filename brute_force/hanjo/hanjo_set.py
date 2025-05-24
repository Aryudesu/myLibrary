def calc_hanjo(H: int, W: int, h: int, w: int, A: int, B: int, memo: set):
    if h == H:
        return 1
    next_w = w + 1
    next_h = h
    if next_w >= W:
        next_w = 0
        next_h += 1
    now = (h, w)
    res = 0
    # 1x1を入れる場合
    if not now in memo and B > 0:
        memo.add(now)
        res += calc_hanjo(H, W, next_h, next_w, A, B - 1, memo)
        memo.discard(now)
    # 1x2を入れる場合
    if w + 1 < W and A > 0:
        next = (h, w + 1)
        if not next in memo and not now in memo:
            memo.add(now)
            memo.add(next)
            res += calc_hanjo(H, W, next_h, next_w, A - 1, B, memo)
            memo.discard(now)
            memo.discard(next)
    # 2x1を入れる場合
    if h + 1 < H and A > 0:
        next = (h + 1, w)
        if not next in memo and not now in memo:
            memo.add(now)
            memo.add(next)
            res += calc_hanjo(H, W, next_h, next_w, A - 1, B, memo)
            memo.discard(now)
            memo.discard(next)
    if now in memo:
        res += calc_hanjo(H, W, next_h, next_w, A, B, memo)
    return res


# == Example ABC196D
H, W, A, B = [int(l) for l in input().split()]
print(calc_hanjo(H, W, 0, 0, A, B, set()))
