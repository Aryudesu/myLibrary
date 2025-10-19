def p_adic_fraction(m: int, n: int, p: int, l: int) -> list[int]:
    """
    m/n を p進数で l桁（p進展開の下位からl桁）まで求める
    """
    result = []
    x = 0
    mod = 1
    for _ in range(l):
        mod *= p
        # n * x ≡ m (mod mod) を解く
        for a in range(p):
            cand = x + a * (mod // p)
            if (n * cand - m) % mod == 0:
                x = cand
                result.append(a)
                break
    return result

print(p_adic_fraction(1, 3, 5, 10))
