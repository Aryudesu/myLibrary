from typing import Iterable, Hashable, Dict, List
from atcoder.dsu import DSU

class ObjectUnionFind(DSU):
    """オブジェクトUnion-Find"""
    def __init__(self, items: Iterable[Hashable]):
        uniq: List[Hashable] = list(dict.fromkeys(items))
        self._obj2idx: Dict[Hashable, int] = {obj: i for i, obj in enumerate(uniq)}
        self._idx2obj: List[Hashable] = uniq[:]
        super().__init__(len(uniq))

    def __contains__(self, obj: Hashable) -> bool:
        return obj in self._obj2idx

    def _require(self, obj: Hashable) -> int:
        try:
            return self._obj2idx[obj]
        except KeyError:
            raise KeyError(obj) from None

    def merge(self, a: Hashable, b: Hashable) -> int:
        ia = self._require(a); ib = self._require(b)
        return super().merge(ia, ib)

    def same(self, a: Hashable, b: Hashable) -> bool:
        ia = self._require(a); ib = self._require(b)
        return super().same(ia, ib)

    def size(self, a: Hashable) -> int:
        ia = self._require(a)
        return super().size(ia)

    def leader_obj(self, a: Hashable):
        ia = self._require(a)
        return self._idx2obj[super().leader(ia)]

    def group_of(self, a: Hashable) -> List[Hashable]:
        ia = self._require(a)
        lead = super().leader(ia)
        return [self._idx2obj[i] for i in range(self.n) if super().leader(i) == lead]

    def groups_objects(self) -> List[List[Hashable]]:
        return [[self._idx2obj[i] for i in g] for g in super().groups()]


# === ABC413

H, W, K = [int(l) for l in input().split()]
LEFT, RIGHT, UP, DOWN = (0, -10), (0, -5), (-10, 0), (-5, 0)
wall = [LEFT, RIGHT, UP, DOWN]
rc = [tuple([int(l) - 1 for l in input().split()]) for _ in range(K)]

uf = ObjectUnionFind(rc + wall)
for r, c in rc:
    now_rc = (r, c)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if r + i < 0:
                uf.merge(now_rc, UP)
            if r + i >= H:
                uf.merge(now_rc, DOWN)
            if c + j < 0:
                uf.merge(now_rc, LEFT)
            if c + j >= W:
                uf.merge(now_rc, RIGHT)
            next_rc = (r + i, c + j)
            if next_rc in uf:
                uf.merge(now_rc, next_rc)

result = not (uf.same(LEFT, RIGHT) or uf.same(LEFT, UP) or uf.same(RIGHT, DOWN) or uf.same(UP, DOWN))
print("Yes" if result else "No")
