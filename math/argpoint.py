from math import gcd

class ArgPoint:
    """偏角を考慮した点クラス"""
    def __init__(self, x: int, y: int, id: int = -1):
        self.x = x
        self.y = y
        self.id = id
        self.isNormed = False
    
    def setId(self, id: int):
        """IDを設定します"""
        self.id = id
    
    def normalize(self):
        """
        座標の正規化を行います．
        """
        g = gcd(self.x, self.y)
        self.x = self.x//g
        self.y = self.y//g
        self.isNormed = True
    
    def getNormalizePoint(self):
        """正規化した点を返却します．"""
        if self.isNormed:
            return (self.x, self.y)
        g = gcd(self.x, self.y)
        return (self.x//g, self.y//g)
    
    def __lt__(self, other: "ArgPoint"):
        """大小判定を行います"""
        ah = 1 if self.y < 0 or self.y == 0 and self.x < 0 else 0
        bh = 1 if other.y < 0 or other.y == 0 and other.x < 0 else 0
        if ah != bh:
            return ah < bh
        return self.x * other.y - self.y * other.x > 0

    def __repr__(self):
        if self.id == -1:
            return f"({self.x}, {self.y})"
        else:
            return f"{self.id}({self.x}, {self.y})"

def compress_direction(points: list[ArgPoint]):
    """
    偏角ソート済＆正規化済のpointsから
    countPerDir: 方向で圧縮した個数
    indexData: 圧縮後のインデックス
    を返却する．
    """
    N = len(points)
    p2Id = dict()
    countPerDir = []
    indexData = [0] * N
    count = 0
    for p in points:
        key = (p.x, p.y)
        if not key in p2Id:
            p2Id[key] = count
            countPerDir.append(0)
            count += 1
        idx = p2Id[key]
        indexData[p.id] = idx
        countPerDir[idx] += 1
    return countPerDir, indexData

# ====== ABC442E

N, Q = map(int, input().split())
points = []
for n in range(N):
    x, y = map(int, input().split())
    ap = ArgPoint(x, y, n)
    ap.normalize()
    points.append(ap)
points.sort(reverse=True)

data, indexData = compress_direction(points)
pData = [0]
l = len(data)
s = 0
for i in range(2*l):
    s += data[i%l]
    pData.append(s)

result = []
for _ in range(Q):
    a, b = map(int, input().split())
    aidx = indexData[a-1]
    bidx = indexData[b-1]
    if aidx == bidx:
        result.append(pData[bidx+1] - pData[aidx])
    else:
        if aidx > bidx:
            bidx += l
        if aidx > bidx:
            raise Exception()
        result.append(pData[bidx+1] - pData[aidx])
for r in result:
    print(r)
