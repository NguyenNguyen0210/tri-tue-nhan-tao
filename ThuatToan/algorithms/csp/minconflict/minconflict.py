import random
from algorithms.utils import get_neighbors, manhattan, misplaced
from algorithms.csp.csp_utils import MAX_STEPS, is_reachable


def _conflicts(state, goal):
    """Return list of positions where tile is misplaced (excluding blank)."""
    return [i for i in range(9) if state[i] != 0 and state[i] != goal[i]]


def _total_conflicts(state, goal):
    return misplaced(state)


def min_conflict_steps(start, goal):
    steps = []
    explored = []

    current_state = start
    current_path = [start]
    current_moves = []
    max_restarts = 5
    restart = 0

    while restart <= max_restarts:
        step_iter = 0
        while True:
            h_curr = _total_conflicts(current_state, goal)

            if current_state == goal:
                explored_render = [
                    (e[0], e[1], e[2][-1] if e[2] else 'start') for e in explored[-12:]
                ]
                steps.append({
                    'type': 'goal',
                    'state': current_state,
                    'cost': h_curr,
                    'moves': current_moves,
                    'path': current_path,
                    'neighbors': [],
                    'added': [],
                    'frontier': [],
                    'frontier_count': 0,
                    'visited_count': len(explored) + 1,
                    'explored': explored_render,
                    'depth': len(current_moves),
                    'limit': restart,
                    'iteration': step_iter,
                })
                return steps

            conflicted = _conflicts(current_state, goal)
            if not conflicted:
                break

            nbrs = get_neighbors(current_state)
            if not nbrs:
                break

            pick_var = max(conflicted, key=lambda i: abs((i // 3) - (goal.index(current_state[i]) // 3)) + abs((i % 3) - (goal.index(current_state[i]) % 3)))

            best_nbrs = []
            best_h = h_curr
            for nb, d in nbrs:
                nb_h = _total_conflicts(nb, goal)
                if nb_h < best_h:
                    best_h = nb_h
                    best_nbrs = [(nb, d)]
                elif nb_h == best_h:
                    best_nbrs.append((nb, d))

            frontier_render = [
                {'state': nb, 'cost': _total_conflicts(nb, goal), 'via': d, 'depth': len(current_moves) + 1}
                for nb, d in nbrs
            ]
            explored_render = [
                (e[0], e[1], e[2][-1] if e[2] else 'start') for e in explored[-12:]
            ]

            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached',
                    'state': current_state,
                    'cost': h_curr,
                    'moves': current_moves,
                    'path': current_path,
                    'neighbors': nbrs,
                    'added': [],
                    'frontier': frontier_render,
                    'frontier_count': len(nbrs),
                    'visited_count': len(explored),
                    'explored': explored_render,
                    'depth': len(current_moves),
                    'limit': pick_var,
                    'iteration': step_iter,
                })
                return steps

            if not best_nbrs or best_h >= h_curr:
                explored.append((current_state, h_curr, current_moves))
                steps.append({
                    'type': 'local_optimum',
                    'state': current_state,
                    'cost': h_curr,
                    'moves': current_moves,
                    'path': current_path,
                    'neighbors': nbrs,
                    'added': [],
                    'frontier': frontier_render,
                    'frontier_count': len(nbrs),
                    'visited_count': len(explored),
                    'explored': explored_render,
                    'depth': len(current_moves),
                    'limit': pick_var,
                    'iteration': step_iter,
                })
                break

            nb, d = random.choice(best_nbrs)
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [(nb, d, best_h)],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': pick_var,
                'iteration': step_iter,
            })

            explored.append((current_state, h_curr, current_moves))
            current_state = nb
            current_moves = current_moves + [d]
            current_path = current_path + [nb]
            step_iter += 1

        if current_state == goal:
            return steps

        restart += 1
        if restart > max_restarts:
            break
        tiles = list(range(9))
        random.shuffle(tiles)
        while len(set(tiles)) < 9:
            random.shuffle(tiles)
        new_start = tuple(tiles)
        if not is_reachable(new_start, goal):
            continue
        explored.append((current_state, manhattan(current_state), current_moves))
        steps.append({
            'type': 'restart',
            'state': new_start,
            'cost': _total_conflicts(current_state, goal),
            'moves': [],
            'path': [new_start],
            'neighbors': [],
            'added': [],
            'frontier': [],
            'frontier_count': 0,
            'visited_count': len(explored),
            'explored': [(e[0], e[1], e[2][-1] if e[2] else 'start') for e in explored[-12:]],
            'depth': 0,
            'limit': restart - 1,
            'iteration': new_start,
        })
        current_state = new_start
        current_path = [new_start]
        current_moves = []

    return steps
