def calc_prime(N):
    """素数表作成"""
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


def yakusu(N, primes):
    """Nの約数の個数計算"""
    tmp = N
    idx = 0
    result = 1
    count = 0
    while tmp > 1:
        p = primes[idx]
        if tmp % p == 0:
            count = 0
            while True:
                if tmp % p != 0:
                    break
                count += 1
                tmp //= p
            result = result * (count + 1)
        elif p * p > tmp:
            result = result * 2
            break
        idx += 1
    return result


primes = calc_prime(200000)
N = int(input())
print(yakusu(N, primes))
