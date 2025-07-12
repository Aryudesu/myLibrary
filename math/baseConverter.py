class BaseConverter:
    """進数表記変換クラス"""

    def __init__(self):
        self.digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def from_base(self, s: str, base: int) -> int:
        """任意の基数表記の文字列 s を10進整数に変換"""
        return int(s, base)

    def to_base(self, n: int, base: int) -> str:
        """10進整数 n を任意の基数 base の文字列に変換"""
        if n == 0:
            return "0"
        result = []
        while n > 0:
            result.append(self.digits[n % base])
            n //= base
        return "".join(reversed(result))

    def convert(self, s: str, from_base: int, to_base: int) -> str:
        """任意の基数表記の文字列 s を、別の基数 to_base の文字列に変換"""
        n = self.from_base(s, from_base)
        return self.to_base(n, to_base)
