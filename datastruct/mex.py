import heapq


class Mex:
    """非負整数の多重集合の mex を管理する。

    max_limit は mex の探索候補数（0 ～ max_limit - 1）。
    mex がその範囲を超える場合は ValueError を送出する。
    """

    def __init__(self, max_limit=2 * (10**5) + 5):
        if max_limit <= 0:
            raise ValueError("max_limit must be positive")
        self.max_limit = max_limit
        self.num_count = {}
        # 昇順リストはそのまま min-heap の条件を満たす。O(max_limit) で初期化。
        self.mex_heap = list(range(max_limit))

    def add(self, num):
        self.num_count[num] = self.num_count.get(num, 0) + 1

    def discard(self, num):
        """存在しない値を削除しても何もしない。"""
        count = self.num_count.get(num, 0)
        if count == 0:
            return
        if count == 1:
            del self.num_count[num]
            if 0 <= num < self.max_limit:
                heapq.heappush(self.mex_heap, num)
        else:
            self.num_count[num] = count - 1

    def change(self, a, b):
        self.discard(a)
        self.add(b)

    def get_mex(self):
        heap = self.mex_heap
        counts = self.num_count
        while heap and counts.get(heap[0], 0) > 0:
            heapq.heappop(heap)
        if not heap:
            raise ValueError("mex is outside the configured max_limit")
        return heap[0]


if __name__ == "__main__":
    # Example: ABC194E
    
    N, M = [int(l) for l in input().split()]
    A = [int(l) for l in input().split()]
    mex = Mex(15 * (10**5) + 5)
    for i in range(M):
        mex.add(A[i])
    result = mex.get_mex()
    for i in range(1, N - M + 1):
        mex.discard(A[i - 1])
        mex.add(A[i + M - 1])
        result = min(result, mex.get_mex())
    print(result)
