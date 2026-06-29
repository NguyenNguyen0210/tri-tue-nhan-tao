"""Shared CSP helpers for 8-Puzzle (variables = board positions 0..8)."""
from collections import deque
from algorithms.utils import get_neighbors, misplaced, manhattan

MAX_STEPS = 3000
VARIABLES = list(range(9))


def assignment_to_state(assignment):
    state = [-1] * 9
    for pos, val in assignment.items():
        state[pos] = val
    return tuple(state)


def is_complete(assignment):
    return len(assignment) == 9


def inversion_parity(state):
    """Parity of inversion count (excluding blank)."""
    tiles = [t for t in state if t != 0]
    inv = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inv % 2


def is_reachable(start, target):
    return inversion_parity(start) == inversion_parity(target)


def init_domains(assignment, goal, goal_directed=True):
    used = set(assignment.values())
    domains = {}
    for var in VARIABLES:
        if var in assignment:
            continue
        dom = set(range(9)) - used
        if goal_directed and goal[var] in dom:
            dom = {goal[var]}
        domains[var] = dom
    return domains


def forward_check(assignment, goal, goal_directed=True):
    domains = init_domains(assignment, goal, goal_directed)
    for dom in domains.values():
        if not dom:
            return False, domains
    return True, domains


def _all_diff_arc_revise(domains, xi, xj):
    revised = False
    if xi not in domains or xj not in domains:
        return revised
    to_remove = []
    for val in domains[xi]:
        if val not in domains[xj]:
            continue
        if len(domains[xj] - {val}) == 0:
            to_remove.append(val)
    for val in to_remove:
        domains[xi].remove(val)
        revised = True
    return revised


def ac3_propagate(domains, goal, goal_directed=True):
    """Run AC-3 on all-different + optional unary goal constraints. Returns (ok, revisions)."""
    domains = {k: set(v) for k, v in domains.items()}
    revisions = []

    if goal_directed:
        for var in VARIABLES:
            if var not in domains:
                continue
            gval = goal[var]
            removed = domains[var] - {gval}
            if removed:
                domains[var] = {gval}
                revisions.append((var, 'unary', sorted(removed), {k: set(v) for k, v in domains.items()}))
            elif gval not in domains[var]:
                return False, revisions

    queue = deque()
    for i in VARIABLES:
        for j in VARIABLES:
            if i != j and i in domains and j in domains:
                queue.append((i, j))

    while queue:
        xi, xj = queue.popleft()
        if xi not in domains or xj not in domains:
            continue
        before = set(domains[xi])
        if _all_diff_arc_revise(domains, xi, xj):
            if not domains[xi]:
                return False, revisions
            revisions.append((xi, xj, sorted(before - domains[xi]), {k: set(v) for k, v in domains.items()}))
            for xk in VARIABLES:
                if xk != xi and xk in domains:
                    queue.append((xk, xi))
    return True, revisions


def domains_to_state(domains):
    state = [-1] * 9
    for var, dom in domains.items():
        if len(dom) == 1:
            state[var] = next(iter(dom))
    return tuple(state)


def domain_size_sum(domains):
    return sum(len(d) for d in domains.values())


def make_step(step_type, state, assignment, moves, path, cost, explored, frontier, frontier_count,
              visited_count, depth, limit=None, iteration=None, added=None, domains=None):
    explored_render = [
        (exp[0], exp[1], exp[2][-1] if exp[2] else 'start')
        for exp in explored[-12:]
    ]
    return {
        'type': step_type,
        'state': state,
        'cost': cost,
        'moves': moves,
        'path': path,
        'neighbors': [],
        'added': added or [],
        'frontier': frontier,
        'frontier_count': frontier_count,
        'visited_count': visited_count,
        'explored': explored_render,
        'depth': depth,
        'limit': limit,
        'iteration': iteration,
        'assignment': dict(assignment),
        'domains': {k: set(v) for k, v in domains.items()} if domains else None,
    }


def frontier_from_domains(domains, assignment, goal):
    items = []
    for var in sorted(domains.keys()):
        dom = domains[var]
        partial = dict(assignment)
        for val in sorted(dom)[:3]:
            partial[var] = val
            st = assignment_to_state(partial)
            items.append({
                'state': st,
                'cost': misplaced(st) if -1 not in st else manhattan(st) if all(x != -1 for x in st) else len(dom),
                'via': f'pos{var}={val}',
                'depth': len(assignment),
            })
        if len(items) >= 12:
            break
    return items[:12]


def bfs_moves(start, goal):
    if start == goal:
        return [start], []
    q = deque([(start, [start], [])])
    seen = {start}
    while q:
        state, path, moves = q.popleft()
        for nb, d in get_neighbors(state):
            if nb in seen:
                continue
            npath = path + [nb]
            nmoves = moves + [d]
            if nb == goal:
                return npath, nmoves
            seen.add(nb)
            q.append((nb, npath, nmoves))
    return None, None
