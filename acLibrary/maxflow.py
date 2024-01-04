class simpleQueue:
    def __init__(self) -> None:
        self.__payload = []
        self.__pos = 0

    def reserve(self, n):
        while len(self.__payload) < n:
            self.__payload.append(None)

    def clear(self):
        self.__payload.clear()
        self.__pos = 0

    def empty(self):
        return self.__pos == len(self.__payload)

    def push(self, x):
        self.__payload.append(x)

    def front(self):
        return self.__payload[self.__pos]

    def size(self):
        return len(self.__payload) - self.__pos

    def pop(self):
        self.__pos += 1


class maxFlow:
    """maxflowクラス"""

    class __edge:
        def __init__(self, to, rev, cap):
            self.to = to
            self.rev = rev
            self.cap = cap

    class edge:
        def __init__(self, frm, to, cap, flow) -> None:
            self.frm = frm
            self.to = to
            self.cap = cap
            self.flow = flow
        def print(self):
            print("{", self.frm, self.to, self.cap, self.flow, "}")

    def __init__(self, n=0, m = 10 ** 10) -> None:
        self.__n = n
        self.__pos = []
        self.__g = []
        self.__M = m
        for i in range(n):
            self.__g.append([])

    def add_edge(self, frm, to, cap):
        """frmからtoへ最大容量cap，流量0の変を追加し，何番目に追加された辺かを返す．"""
        assert 0 <= frm and frm < self.__n
        assert 0 <= to and to < self.__n
        m = len(self.__pos)
        self.__pos.append([frm, len(self.__g[frm])])
        from_id = len(self.__g[frm])
        to_id = len(self.__g[to])
        if frm == to:
            to_id += 1
        self.__g[frm].append(self.__edge(to, to_id, cap))
        self.__g[to].append(self.__edge(frm, from_id, 0))
        return m

    def get_edge(self, i):
        """今の内部の辺の状態を返す．"""
        m = len(self.__pos)
        assert 0 <= i and i < m
        _e = self.__g[self.__pos[i][0]][self.__pos[i][1]]
        _re = self.__g[_e.to][_e.rev]
        return self.edge(self.__pos[i][0], _e.to, _e.cap + _re.cap, _re.cap)

    def edges(self):
        """今の内部の辺の状態を返す．"""
        m = len(self.__pos)
        result = []
        for i in range(m):
            result.append(self.get_edge(i))
        return result

    def change_edge(self, i, new_cap, new_flow):
        """i番目に追加された辺の容量，流量をnew_cap, new_flowに変更する．"""
        m = len(self.__pos)
        assert 0 <= i and i < m
        assert 0 <= new_flow and new_flow <= new_cap
        _e = self.__g[self.__pos[i][0]][self.__pos[i][1]]
        _re = self.__g[_e.to][_e.rev]
        _e.cap = new_cap - new_flow
        _re.cap = new_flow

    def flow(self, s, t, flow_limit = 10 ** 10):
        """
        頂点sからtへ流量flow_limitに達するまで流せる限り流し，流せた量を返す．
        """
        assert 0 <= s and s < self.__n
        assert 0 <= t and t < self.__n
        assert s != t
        level = [0] * self.__n
        iter = [0] * self.__n
        que = simpleQueue()

        def bfs():
            for i in range(self.__n):
                level[i] = -1
            level[s] = 0
            que.clear()
            que.push(s)
            while not que.empty():
                v = que.front()
                que.pop()
                for e in self.__g[v]:
                    if e.cap == 0 or level[e.to] >= 0:
                        continue
                    level[e.to] = level[v] + 1
                    if e.to == t:
                        return
                    que.push(e.to)

        def dfs(v, up):
            if v == s:
                return up
            res = 0
            level_v = level[v]
            for i in range(iter[v], len(self.__g[v])):
                e = self.__g[v][i]
                if level_v <= level[e.to] or self.__g[e.to][e.rev].cap == 0:
                    continue
                d = dfs(e.to, min([up-res, self.__g[e.to][e.rev].cap]))
                if d <= 0:
                    continue
                self.__g[v][i].cap += d
                self.__g[e.to][e.rev].cap -= d
                res += d
                if res == up:
                    return res
            level[v] = self.__n
            return res

        flow = 0
        while flow < flow_limit:
            bfs()
            if level[t] == - 1:
                break
            for i in range(self.__n):
                iter[i] = 0
            f = dfs(t, flow_limit - flow)
            if not f:
                break
            flow += f
        return flow

    """
    長さnのvectorを返却する．i番目の要素には頂点sからiへ残余グラフで到達可能なとき，またその時のみTrueを返却する．
    flow(s,t)をflow_limitなしでちょうど一回読んだ後に呼ぶと，返り値はs,t間のmincutに対応する．
    """
    def min_cut(self, s):
        visited = [0] * self.__n
        que = simpleQueue()
        que.append(s)
        while not que.empty():
            p = que.front()
            que.pop()
            visited[p] = True
            for e in self.__g[p]:
                if e.cap and not visited[e.to]:
                    visited[e.to] = True
                    que.push(e.to)
        return visited


N, M = [int(l) for l in input().split()]
S = []
for n in range(N):
    S.append(list(input()))

g = maxFlow(n = N * M + 2)
s = N * M
t = N * M + 1
for i in range(N):
    for j in range(M):
        if S[i][j] == "#":
            continue
        v = i * M + j
        if (i + j) % 2 == 0:
            g.add_edge(s, v, 1)
        else:
            g.add_edge(v, t, 1)

for i in range(N):
    for j in range(M):
        if (i + j) % 2 or S[i][j] == "#":
            continue
        v0 = i * M + j
        if i and S[i-1][j] == ".":
            v1 = (i-1) * M + j
            g.add_edge(v0, v1, 1)
        if j and S[i][j-1] == ".":
            v1 = i * M + (j- 1)
            g.add_edge(v0, v1, 1)
        if i + 1 < N and S[i + 1][j] == ".":
            v1 = (i + 1) * M + j
            g.add_edge(v0, v1, 1)
        if j + 1 < M and S[i][j+1] == ".":
            v1 = i * M + (j + 1)
            g.add_edge(v0, v1, 1)

print(g.flow(s,t))
edges = g.edges()
for e in edges:
    if e.frm == s or e.to == t or e.flow == 0:
        continue
    i0 = e.frm//M
    j0 = e.frm % M
    i1 = e.to // M
    j1 = e.to % M

    if i0 == i1 + 1:
        S[i1][j1] = "v"
        S[i0][j0] = "^"
    elif j0 == j1 + 1:
        S[i1][j1] = ">"
        S[i0][j0] = "<"
    elif i0 == i1 - 1:
        S[i0][j0] = "v"
        S[i1][j1] = "^"
    else:
        S[i0][j0] = ">"
        S[i1][j1] = "<"

for i in range(N):
    print("".join(S[i]))