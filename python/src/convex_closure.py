from collections import deque
from typing import List, Tuple


def convex_closure(N: int, points:List[Tuple[int, int]]) -> List[int]:
    """
    凸包計算(2次元平面)
    全ての点が同一直線上にないことが前提
    """
    MAX_INT = 2 * 10 ** 18

    # 上側凸を計算
    upper_points_map = {}
    for i in range(N):
        x, y = points[i]
        if x not in upper_points_map:
            upper_points_map[x] = (-MAX_INT, i)
        upper_points_map[x] = max(upper_points_map[x], (y, i))
    upper_points_array = [(x, y[0], y[1]) for x, y in upper_points_map.items()]
    upper_points_array.sort(key=lambda x : x[0])

    x, y, i = upper_points_array[0]
    upper_deque = deque([(x, y, i, (MAX_INT, 1))])
    for index in range(1, len(upper_points_array)):
        x, y, i = upper_points_array[index]
        while len(upper_deque) >= 2:
            px, py, _, coef = upper_deque[-1]
            new_coef = (y - py, x - px)
            if new_coef[0] * coef[1] >= new_coef[1] * coef[0]:
                upper_deque.pop()
            else:
                break

        px, py, _, _ = upper_deque[-1]
        new_coef = (y - py, x - px)
        upper_deque.append((x, y, i, new_coef))

    # 下側凸を計算
    lower_points_map = {}
    for i in range(N):
        x, y = points[i]
        if x not in lower_points_map:
            lower_points_map[x] = (MAX_INT, i)
        lower_points_map[x] = min(lower_points_map[x], (y, i))
    lower_points_array = [(x, y[0], y[1]) for x, y in lower_points_map.items()]
    lower_points_array.sort(key=lambda x : x[0])

    x, y, i = lower_points_array[0]
    lower_deque = deque([(x, y, i, (-MAX_INT, 1))])
    for index in range(1, len(lower_points_array)):
        x, y, i = lower_points_array[index]
        while len(lower_deque) >= 2:
            px, py, _, coef = lower_deque[-1]
            new_coef = (y - py, x - px)
            if new_coef[0] * coef[1] <= new_coef[1] * coef[0]:
                lower_deque.pop()
            else:
                break

        px, py, _, _ = lower_deque[-1]
        new_coef = (y - py, x - px)
        lower_deque.append((x, y, i, new_coef))

    # 上側凸と下側凸を組み合わせて、凸包を構成する点のindexリストを作成
    vertices = []
    while len(lower_deque) > 0:
        _, _, i, _ = lower_deque.popleft()
        vertices.append(i)
    while len(upper_deque) > 0:
        _, _, i, _ = upper_deque.pop()
        vertices.append(i)

    # pointのindexの重複削除
    new_vertices = []
    prev = -1
    for i in vertices:
        if prev != i:
            new_vertices.append(i)
        prev = i
    if new_vertices[0] == new_vertices[-1]:
        new_vertices.pop()
    return new_vertices
