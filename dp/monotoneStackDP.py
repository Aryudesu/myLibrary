class MonotoneStackDP:
    def __init__(self, INF: int = 10**10):
        self.INF = INF
    
    def waterTankTimes(self, H: list[int]):
        N = len(H)
        data = [(self.INF, 0)]
        dp = [0] * (N + 1)
        result = [0] * N
        for i in range(1, N + 1):
            h = H[i-1]
            while data[-1][0] < h:
                data.pop()
            prev = data[-1][1]
            dp[i] = dp[prev] + h * (i - prev)
            data.append((h, i))
            result[i-1] = dp[i] + 1
        return result


