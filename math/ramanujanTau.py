def calc_pascal_triangle(num):
    dp = [1]
    for i in range(num):
        new_dp = [1] + [dp[j] + dp[j + 1] for j in range(len(dp) - 1)] + [1]
        dp = new_dp
    return dp


def calc(num):
    ta = calc_pascal_triangle(24)
    lta = len(ta)
    dp = {0: 1}  # 初期状態
    for n in range(1, num + 1):
        new_dp = {}
        for d, dp_value in dp.items():
            sgn = 1
            for idx in range(lta):
                key = d + n * idx
                if key > num:  # 範囲外になったら終了
                    break
                new_dp[key] = new_dp.get(key, 0) + sgn * dp_value * ta[idx]
                sgn = -sgn
        dp = new_dp  # 更新
    # 結果リストを生成
    return [dp.get(i, 0) for i in range(num + 1)]


def inputNum():
    print("InputNum > ", end="")
    return int(input())


# 入力値に応じた結果を計算し、ファイルに保存
result = calc(inputNum())
with open("Result.txt", mode="w") as f:
    for r in result:
        f.write(str(r) + "\n")
