def calcAbsDiffSum(arr: list[int]) -> int:
    # 全組み合わせでの差分の絶対値の総和を計算します
    data = arr[:]
    data.sort()
    res = 0
    left_sum = 0
    for i, x in enumerate(data):
        res += x * i - left_sum
        left_sum += x
    return res

N = int(input())
X = []
Y = []
for n in range(N):
    x, y = map(int, input().split())
    X.append(x)
    Y.append(y)
print(calcAbsDiffSum(X) + calcAbsDiffSum(Y))

