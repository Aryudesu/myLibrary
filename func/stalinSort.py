from typing import Tuple

def stalinSort(data: list[int])->Tuple[list[int], list[int]]:
    """
    スターリンソート．先頭から昇順になるようにデータを残す．
    戻り値は (ソート済データ, ソート対象外となったデータ)
    """
    survival = []
    purge = []
    for dat in data:
        if not survival or survival[-1] < dat:
            survival.append(dat)
        else:
            purge.append(dat)
    return survival, purge
