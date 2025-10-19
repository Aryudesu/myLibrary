from collections import deque

class GridBFS:
    INF = 10**18
    dirs4 = ((1,0),(-1,0),(0,1),(0,-1))
    def calc(self, H: int, W: int, field, starts: list, states: int=1):
        """
        H*WのグリッドfieldについてstartsからBFSを行う
        戻り値はdist
        """
        dist = [[[self.INF]*W for _ in range(H)] for __ in range(states)]
        dq = deque()
        for st in starts:
            dq.append((st))
        while dq:
            s, y, x = dq.popleft()
            d = dist[s][y][x]
            for dy,dx in self.dirs4:
                ny,nx = y+dy, x+dx
                if not (0 <= ny < H and 0 <= nx <W): continue
                # TODO 状態遷移
                ns = s
                if dist[ns][ny][nx] > d+1:
                    dist[ns][ny][nx] = d+1
                    dq.append((ns,ny,nx))
        return dist

