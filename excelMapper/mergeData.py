from dataclasses import dataclass

@dataclass
class MergeData:
    """結合範囲を設定します"""
    left: int
    top: int
    right: int
    bottom: int

    def __post_init__(self):
        assert 0 <= self.left <= self.right
        assert 0 <= self.top <= self.bottom
