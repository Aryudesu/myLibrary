from collections import deque


def slidingMinMax(A: list[int], k: int):
    min_q = deque()
    max_q = deque()

    for r, x in enumerate(A):
        while min_q and A[min_q[-1]] >= x:
            min_q.pop()
        min_q.append(r)

        while max_q and A[max_q[-1]] <= x:
            max_q.pop()
        max_q.append(r)

        l = r - k + 1

        while min_q and min_q[0] < l:
            min_q.popleft()
        while max_q and max_q[0] < l:
            max_q.popleft()

        if l >= 0:
            yield A[min_q[0]], A[max_q[0]]


