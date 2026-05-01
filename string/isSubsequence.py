def is_subsequence(S: str, T: str)->bool:
    """TがSの部分列か"""
    if len(T) == 0:
        return True
    if len(T) > len(S):
        return False
    tIdx = 0
    for s in S:
        if s == T[tIdx]:
            tIdx += 1
            if tIdx == len(T):
                return True
    return len(T) == 0
