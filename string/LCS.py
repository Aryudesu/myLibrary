from typing import Sequence, TypeVar

T = TypeVar("T")


def myers_distance(a: Sequence[T], b: Sequence[T]) -> int:
    """
    Myers の O(ND) アルゴリズムで、挿入＋削除のみの編集距離を求める。

    Parameters
    ----------
    a, b : 任意のシーケンス（str, list, tuple など）

    Returns
    -------
    d : int
        a を b に変換するのに必要な insert + delete の最小回数。
        （置換は insert+delete 2回としてカウントされる）
    """
    n, m = len(a), len(b)
    max_d = n + m

    # v[k] = 対角線 k 上で到達できる最大の x
    # 論文では配列 V[-MAX..MAX] だが、Python では dict でやる
    v = {1: 0}

    for d in range(max_d + 1):
        # d 回の編集（非対角辺）を使うパスを全部試す
        for k in range(-d, d + 1, 2):
            # どっちから来たか？
            #   k-1 → 右（delete）
            #   k+1 → 下（insert）
            if k == -d or (k != d and v.get(k - 1, 0) < v.get(k + 1, 0)):
                # 下から来る（insert）
                x = v.get(k + 1, 0)
            else:
                # 右から来る（delete）
                x = v.get(k - 1, 0) + 1

            y = x - k

            # snake：一致する限り対角線を貪欲に伸ばす
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1

            v[k] = x

            # 終点 (n, m) に到達したらそれが最小 d
            if x >= n and y >= m:
                return d

    # ここまで行くことは理論上ないが、お守りで
    return max_d


def lcs_length(a: Sequence[T], b: Sequence[T]) -> int:
    """
    Myers の距離から LCS の長さを求めるユーティリティ関数。
    """
    d = myers_distance(a, b)
    return (len(a) + len(b) - d) // 2



S = input()
T = input()
d = myers_distance(S, T)
L = lcs_length(S, T)
print("D =", d)   # 最小挿入＋削除回数
print("LCS length =", L)
