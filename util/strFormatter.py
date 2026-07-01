def bitstr_to_int(s: str) -> int:
    return int(s, 2)

def int_to_bitstr(x: int, length: int) -> str:
    return format(x, f"0{length}b")

def has_bit(x: int, i: int) -> bool:
    """下位から i ビット目が立っているか"""
    return (x >> i) & 1

def set_bit(x: int, i: int) -> int:
    """i ビット目を1にする"""
    return x | (1 << i)

def reset_bit(x: int, i: int) -> int:
    """i ビット目を0にする"""
    return x & ~(1 << i)

def flip_bit(x: int, i: int) -> int:
    """i ビット目を反転する"""
    return x ^ (1 << i)
