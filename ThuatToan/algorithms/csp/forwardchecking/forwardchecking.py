from algorithms.utils import get_neighbors, manhattan
from algorithms.csp.csp_utils import MAX_STEPS, bfs_moves


def forward_checking_steps(start, goal):
    """Backtracking + forward checking: prune neighbor if FC detects dead domain."""
    steps = []
    explored = []

    path_len, _ = bfs_moves(start, goal)
    max_depth = len(path_len) - 1 if path_len else 31

    def snapshot(state, moves, frontier_states, step_type, added=None, limit=None):
        explored_render = [
            (e[0], e[1], e[2][-1] if e[2] else 'start') for e in explored[-12:]
        ]
        frontier_render = [
            {'state': st, 'via': d, 'depth': len(moves) + 1, 'cost': manhattan(st)}
            for st, d in frontier_states[:12]
        ]
        steps.append({
            'type': step_type,
            'state': state,
            'cost': manhattan(state),
            'moves': list(moves),
            'path': None,
            'neighbors': [],
            'added': added or [],
            'frontier': frontier_render,
            'frontier_count': len(frontier_states),
            'visited_count': len(explored),
            'explored': explored_render,
            'depth': len(moves),
            'limit': limit,
            'iteration': max_depth,
        })
        return len(steps) >= MAX_STEPS

    def forward_ok(nb, depth):
        if depth > max_depth:
            return False
        if manhattan(nb) > max_depth - depth:
            return False
        return True

    def search(state, path_set, moves):
        if len(steps) >= MAX_STEPS:
            return True

        nbrs = get_neighbors(state)
        viable = [(nb, d) for nb, d in nbrs if nb not in path_set and forward_ok(nb, len(moves) + 1)]
        pruned = [(nb, d) for nb, d in nbrs if nb not in path_set and not forward_ok(nb, len(moves) + 1)]

        if state == goal:
            explored.append((state, manhattan(state), moves))
            snapshot(state, moves, viable, 'goal')
            return True

        explored.append((state, manhattan(state), moves))
        added = [(nb, d, manhattan(nb)) for nb, d in viable[:4]]
        if pruned:
            added += [(nb, f'FC✗{d}', manhattan(nb)) for nb, d in pruned[:2]]
        if snapshot(state, moves, viable, 'expand', added=added):
            return True

        for nb, d in viable:
            path_set.add(nb)
            moves.append(d)
            if search(nb, path_set, moves):
                return True
            moves.pop()
            path_set.remove(nb)
            if snapshot(state, moves, [(n, dr) for n, dr in viable if n not in path_set], 'backtrack', limit=d):
                return True

        return False

    path_set = {start}
    search(start, path_set, [])
    return steps
