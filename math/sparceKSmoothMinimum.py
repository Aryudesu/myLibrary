def kSmoothMinimum(arr: list[int], K: int) -> list[int]:
    """各要素を加算のみを行い前後の差をK以下にした場合の最適解"""
    N = len(arr)
    L = [0] * N
    L[0] = arr[0]
    for i in range(1, N):
        L[i] = max(arr[i], L[i-1] - K)
    r = arr[-1]
    B = [0] * N
    B[-1] = max(L[-1], r)
    for i in range(N-2, -1, -1):
        r = max(arr[i], r - K)
        B[i] = max(L[i], r)
    return B

# AWC0005C
N, K = map(int, input().split())
A = list(map(int, input().split()))
B = kSmoothMinimum(A, K)
print(sum(B[i] - A[i] for i in range(N)))
