def eratosthenes(N):
    """エラトステネスの篩"""
    result = [True] * (N + 1)
    primes = [2]
    for i in range(3, N + 1, 2):
        if not result[i]:
            continue
        primes.append(i)
        idx = 3
        while idx * i <= N:
            result[idx * i] = False
            idx += 2
    return primes


N = 1000
result = eratosthenes(N)
print(result)
