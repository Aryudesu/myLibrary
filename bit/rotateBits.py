def rotate_bits_left(x: int, width: int) -> int:
    mask = (1 << width) - 1
    return ((x << 1) & mask) | (x >> (width - 1))


def rotate_bits_right(x: int, width: int) -> int:
    return (x >> 1) | ((x & 1) << (width - 1))

