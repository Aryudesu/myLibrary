from dataclasses import dataclass

@dataclass
class BorderData:
    """罫線を設定します"""
    THIN = "thin"
    THICK = "thick"
    DOUBLE = "double"
    HAIR = "hair"
    DOTTED = "dotted"
    DASHED = "dashed"
    DASH_DOT = "dashDot"
    DASH_DO_TDOT = "dashDotDot"
    MEDIUM = "medium"
    MEDIUM_DASHED = "mediumDashed"
    MEDIUM_DASH_DOT = "mediumDashDot"
    MEDIUM_DASH_DOT_DOT = "mediumDashDotDot"
    SLANT_DASH_DOT = "slantDashDot"

    x1: int
    y1: int
    x2: int
    y2: int

    leftF: bool = True
    topF: bool = True
    rightF: bool = True
    bottomF: bool = True

    left: str = THIN
    right: str = THIN
    top: str = THIN
    bottom: str = THIN

    def __post_init__(self):
        assert 0 <= self.left <= self.right
        assert 0 <= self.top <= self.bottom

    def setAllStyle(self, style: str):
        """全周囲に同じスタイルを設定します"""
        self.left = style
        self.right = style
        self.top = style
        self.bottom = style
