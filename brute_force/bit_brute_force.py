from itertools import product


def bit_brute_force(A: list):
    """Bit全探索を行います"""
    for bits in product([0, 1], repeat=len(A)):
        data = [x for bit, x in zip(bits, A) if bit]
        # TODO 後処理を書く（必要なければ空）
        print(data)
    # TODO 結果を返却する
    return None


bit_brute_force([3, 1, 4, 1, 5])
