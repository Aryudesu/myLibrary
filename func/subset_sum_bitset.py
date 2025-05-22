def subset_sum(A: list[int], target: int) -> bool:
    """Bitを用いた部分和問題"""
    mask = (1 << (target + 1)) - 1
    bits = 1
    for a in A:
        bits |= bits << a
        if (bits >> target) & 1:
            return True
        bits &= mask
    return (bits >> target) & 1


N, S = [int(l) for l in input().split()]
A = [int(l) for l in input().split()]
print("Yes" if subset_sum(A, S) else "No")
