class primeCalc:
    def __init__(self, n: int = 10**6):
        """初期化（素数表作成）"""
        result = [True] * (n + 1)
        self.primes = [2]
        for i in range(3, n + 1, 2):
            if not result[i]:
                continue
            self.primes.append(i)
            idx = 3
            while idx * i <= n:
                result[idx * i] = False
                idx += 2

    def primes(self):
        return self.primes

    def soinsu(self, n: int):
        """Nの素因数分解"""
        tmp = n
        idx = 0
        result = []
        while tmp > 1:
            p = self.primes[idx]
            if tmp % p == 0:
                while True:
                    if tmp % p != 0:
                        break
                    result.append(p)
                    tmp //= p
            elif p * p > tmp:
                result.append(tmp)
                return result
            idx += 1
        return result
    
    def soinsu2(self, n: int):
        """Nの素因数分解．"""
        tmp = n
        idx = 0
        result = []
        while tmp > 1:
            p = self.primes[idx]
            if tmp % p == 0:
                count = 0
                while True:
                    if tmp % p != 0:
                        result.append((p, count))
                        break
                    count += 1
                    tmp //= p
            elif p * p > tmp:
                result.append((tmp, 1))
                return result
            idx += 1
        return result

    def yakusu(self, n: int):
        """Nの約数の個数計算"""
        tmp = n
        idx = 0
        result = 1
        count = 0
        while tmp > 1:
            p = self.primes[idx]
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


pc = primeCalc(10**7)
print(*pc.soinsu2(int(input())))
