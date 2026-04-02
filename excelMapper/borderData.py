from dataclasses import dataclass

@dataclass
class BorderData:
    """罫線を設定します"""
    left: int
    top: int
    right: int
    bottom: int

    leftF: bool = True
    topF: bool = True
    rightF: bool = True
    bottomF: bool = True

    def __post_init__(self):
        assert 0 <= self.left <= self.right
        assert 0 <= self.top <= self.bottom
