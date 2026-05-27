from config import GOAL, DIRS

def misplaced(state):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != GOAL[i])

def manhattan(state):
    dist = 0
    for i in range(9):
        val = state[i]
        if val != 0:
            target_idx = val - 1  # Vì GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
            r_curr, c_curr = divmod(i, 3)
            r_targ, c_targ = divmod(target_idx, 3)
            dist += abs(r_curr - r_targ) + abs(c_curr - c_targ)
    return dist


def get_neighbors(state):
    res = []
    bi = state.index(0)
    r, c = divmod(bi, 3)
    for dr, dc, d in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            s = list(state)
            ni = nr * 3 + nc
            s[bi], s[ni] = s[ni], s[bi]
            res.append((tuple(s), d))
    return res
