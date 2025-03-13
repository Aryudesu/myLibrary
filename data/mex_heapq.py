import heapq


class Mex:
    def __init__(self, max_limit=2 * (10**5) + 5):
        self.num_count = dict()
        self.mex_heap = []
        heapq.heapify(self.mex_heap)
        for i in range(max_limit):
            heapq.heappush(self.mex_heap, i)

    def add(self, num):
        if num in self.num_count:
            self.num_count[num] += 1
        else:
            self.num_count[num] = 1

    def discard(self, num):
        if num in self.num_count:
            self.num_count[num] -= 1
            if self.num_count[num] == 0:
                heapq.heappush(self.mex_heap, num)

    def change(self, a, b):
        self.discard(a)
        self.add(b)

    def get_mex(self):
        while self.num_count.get(self.mex_heap[0], 0) > 0:
            heapq.heappop(self.mex_heap)
        return self.mex_heap[0]
