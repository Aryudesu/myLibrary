from itertools import permutations
from typing import Tuple

def isOk(nums: Tuple[int], N: int, K: int)-> bool:
    tNums = list(nums)
    data = dict()
    for i in range(N):
        data[tNums[i]] = i
    count = 0
    for i in range(N):
        idx = data[i]
        if i == idx:
            continue
        n = tNums[i]
        tNums[i] = i
        tNums[idx] = n
        data[n] = idx
        count += 1
    return count <= K
