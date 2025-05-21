def subset_sum_set(A: list, target: int):
    """setを用いた部分和問題"""
    if target == 0:
        return True
    A = [a for a in A if a <= target]
    A.sort()
    total_remaining = sum(A)
    if total_remaining < target:
        return False
    dp = set()
    for a in A:
        if a == target:
            return True
        total_remaining -= a
        next_dp = {a}
        for x in dp:
            s = a + x
            if s == target:
                return True
            # 残り全てM超過になる場合 or 残り全部足しても届かない場合
            if s > target or s + total_remaining < target:
                continue
            next_dp.add(s)
            next_dp.add(x)
        dp = next_dp
    return target in dp


N, S = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
print("Yes" if subset_sum_set(A, S) else "No")
