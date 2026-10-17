##
##  最大フロー問題を解くためのグラフ
##

from collections import deque

class MFGraph:
    class Edge:
        __slots__ = ("to", "rev", "cap")
        def __init__(self, to, rev, cap):
            self.to = to
            self.rev = rev
            self.cap = cap

    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        forward = MFGraph.Edge(to, len(self.g[to]), cap)
        backward = MFGraph.Edge(fr, len(self.g[fr]), 0)
        self.g[fr].append(forward)
        self.g[to].append(backward)

    def flow(self, s, t):
        flow = 0
        INF = 10**30

        while True:
            level = [-1] * self.n
            q = deque([s])
            level[s] = 0

            # BFS
            while q:
                v = q.popleft()
                for e in self.g[v]:
                    if e.cap > 0 and level[e.to] < 0:
                        level[e.to] = level[v] + 1
                        q.append(e.to)

            if level[t] < 0:
                return flow

            it = [0] * self.n

            def dfs(v, f):
                if v == t:
                    return f
                for i in range(it[v], len(self.g[v])):
                    it[v] = i
                    e = self.g[v][i]
                    if e.cap > 0 and level[v] < level[e.to]:
                        d = dfs(e.to, min(f, e.cap))
                        if d > 0:
                            e.cap -= d
                            self.g[e.to][e.rev].cap += d
                            return d
                return 0

            while True:
                f = dfs(s, INF)
                if f == 0:
                    break
                flow += f
