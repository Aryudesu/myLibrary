from collections import deque

def sliding_max(arr, K):
    dq = deque()
    result = []

    for i in range(len(arr)):
        # 区間外を削除
        while dq and dq[0] <= i - K:
            dq.popleft()
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
        # 最大値取得
        if i >= K - 1:
            result.append(arr[dq[0]])
    return result
