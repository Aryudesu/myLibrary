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

N = 1000
result = eratosthenes(N)
print(result)
