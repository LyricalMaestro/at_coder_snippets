from collections import deque

def scc(N, next_nodes):
    """
    有向グラフにおける強連結成分分解
    """
    # 深さ優先探索をしてラベリング
    stack = deque()
    v_list = []
    parents = [-2] * N
    for s_i in range(N):
        if parents[s_i] == -2:
            parents[s_i] = -1
            stack.append((s_i, 0))
            while len(stack) > 0:
                v, index = stack.pop()
                while index < len(next_nodes[v]):
                    w = next_nodes[v][index]
                    if w == parents[v]:
                        index += 1
                        continue
    
                    if parents[w] != -2:
                        index += 1
                        continue

                    parents[w] = v
                    stack.append((v, index + 1))
                    stack.append((w, 0))
                    break

                if len(next_nodes[v]) == index:
                    v_list.append(v)
    
    # 逆グラフの生成
    reversed_nodes = [[] for _ in range(N)]
    for i in range(N):
        for w in next_nodes[i]:
            reversed_nodes[w].append(i)

    scc_label = [-1] * N
    scc_index = 0
    for s_v in reversed(v_list):
        if scc_label[s_v] == -1:
            queue = deque()
            queue.append(s_v)
            scc_label[s_v] = scc_index
            while len(queue) > 0:
                v = queue.popleft()
                for w in reversed_nodes[v]:
                    if scc_label[w] == -1:
                        scc_label[w] = scc_index
                        queue.append(w)
            scc_index += 1
    return scc_label
