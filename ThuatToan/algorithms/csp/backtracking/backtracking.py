from algorithms.utils import get_neighbors, manhattan
from algorithms.csp.csp_utils import MAX_STEPS


def backtracking_steps(start, goal):
    steps = []
    explored = []

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
            'iteration': None,
        })
        return len(steps) >= MAX_STEPS

    def search(state, path_set, moves):
        if len(steps) >= MAX_STEPS:
            return True

        nbrs = get_neighbors(state)
        frontier_states = [(nb, d) for nb, d in nbrs if nb not in path_set]

        if state == goal:
            explored.append((state, manhattan(state), moves))
            snapshot(state, moves, frontier_states, 'goal')
            return True

        explored.append((state, manhattan(state), moves))
        if snapshot(state, moves, frontier_states, 'expand',
                    added=[(nb, d, manhattan(nb)) for nb, d in frontier_states[:4]]):
            return True

        for nb, d in nbrs:
            if nb in path_set:
                continue
            path_set.add(nb)
            moves.append(d)
            if search(nb, path_set, moves):
                return True
            moves.pop()
            path_set.remove(nb)
            if snapshot(state, moves, [(n, dr) for n, dr in nbrs if n not in path_set], 'backtrack', limit=d):
                return True

        return False

    path_set = {start}
    search(start, path_set, [])
    return steps
