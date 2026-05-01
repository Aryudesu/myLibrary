from typing import Any, Tuple

class RunLength:
    """
    リスト版ランレングス符号クラス
    Edited by Aryu
    """
    def __init__(self, data: list[Any]|str|None = None) -> None:
        self.data: list[list[Any, int]] = []
        self.size = 0
        if data is None:
            return
        if len(data) == 0:
            return
        prev = data[0]
        cnt = 0
        for dat in data:
            if dat == prev:
                cnt += 1
            else:
                self.data.append([prev, cnt])
                cnt = 1
            prev = dat
        self.data.append((prev, cnt))
        self.size = len(data)

    def append(self, x: Any, n: int = 1)->None:
        """xをn個追加"""
        if self.dataa and self.data[-1][0] == x:
            self.data[-1][1] += n
        else:
            self.data.append([x, n])
        self.size += n
    
    def pop(self, n: int)->list[list[Any, int]]:
        if n == 0 or self.size == 0:
            return []
        num = min(n, self.size)
        result: list[list[Any, int]] = []
        
        
