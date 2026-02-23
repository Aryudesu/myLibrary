from math import isqrt

def eratosthenes(N: int)->list[int]:
    """エラトステネスの篩"""
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    primes = [2] if N >= 2 else []
    for i in range(3, N + 1, 2):
        if not is_prime[i]:
            continue
        primes.append(i)
        if i * i > N:
            continue
        for j in range(i * i, N + 1, 2 * i):
            is_prime[j] = False
    return primes

def intervalErats(L: int, R: int):
    """区間篩"""
    basePrimes = eratosthenes(isqrt(R) + 1)
    N = (R - L + 1)
    isPrime = [True] * N
    if L == 1:
        isPrime[0] = False
    for p in basePrimes:
        start = ((L + p - 1) // p) * p
        for x in range(start, R + 1, p):
            if x == p:
                continue
            isPrime[x-L] = False
    return [L + i for i in range(N) if isPrime[i]]

L, R = map(int, input().split())
res = intervalErats(L, R)
print(len(res))
