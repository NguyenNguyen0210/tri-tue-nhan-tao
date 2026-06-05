import heapq
from algorithms.utils import misplaced, manhattan, get_neighbors

def idastar_steps(start, goal):
    steps = []
    explored_global = []  # Tích lũy qua các vòng lặp để phục vụ giao diện hiển thị
    MAX_STEPS = 3000

    g_start = manhattan(start)
    h_start = misplaced(start)
    f_start = g_start + h_start
    threshold = f_start
    iteration_count = 0

    while True:
        iteration_count += 1
        # Stack stores: (state, path, moves, g_score, f_score)
        frontier = [(start, [start], [], g_start, f_start)]
        next_threshold = float('inf')
        result = 'failure'

        if len(steps) >= MAX_STEPS:
            break

        # Render lists for start of iteration
        frontier_render = [
            {
                'state': f_node[0],
                'cost': f_node[4],
                'g': f_node[3],
                'h': f_node[4] - f_node[3],
                'via': f_node[2][-1] if f_node[2] else 'start'
            }
            for f_node in list(reversed(frontier[-12:]))
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start', exp_node[3], exp_node[4])
            for exp_node in explored_global[-12:]
        ]

        steps.append({
            'type': 'new_iteration',
            'state': start, 'cost': f_start, 'g': g_start, 'h': h_start,
            'moves': [], 'frontier': frontier_render,
            'frontier_count': len(frontier),
            'visited_count': len(explored_global),
            'explored': explored_render,
            'depth': 0, 'limit': threshold, 'iteration': iteration_count,
            'added': [], 'neighbors': [],
            'message': f'🔄 Bắt đầu vòng lặp {iteration_count}: ngưỡng f_limit = {threshold}',
        })

        while frontier:
            state, path, moves, g_score, f_score = frontier.pop()
            nbrs = get_neighbors(state)

            frontier_render = [
                {
                    'state': f_node[0],
                    'cost': f_node[4],
                    'g': f_node[3],
                    'h': f_node[4] - f_node[3],
                    'via': f_node[2][-1] if f_node[2] else 'start'
                }
                for f_node in list(reversed(frontier[-12:]))
            ]
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start', exp_node[3], exp_node[4])
                for exp_node in explored_global[-12:]
            ]

            # Check cycle in the current path to prevent infinite loops
            is_cycle = state in path[:-1]
            if is_cycle:
                if len(steps) >= MAX_STEPS:
                    steps.append({
                        'type': 'limit_reached', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                        'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                        'frontier': frontier_render, 'frontier_count': len(frontier),
                        'visited_count': len(explored_global), 'explored': explored_render,
                        'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                    })
                    return steps

                steps.append({
                    'type': 'cycle', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                    'moves': moves, 'path': path, 'frontier': frontier_render, 'frontier_count': len(frontier),
                    'visited_count': len(explored_global), 'explored': explored_render,
                    'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                })
                continue

            # Check threshold
            if f_score > threshold:
                next_threshold = min(next_threshold, f_score)
                result = 'cutoff'
                if len(steps) >= MAX_STEPS:
                    steps.append({
                        'type': 'limit_reached', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                        'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                        'frontier': frontier_render, 'frontier_count': len(frontier),
                        'visited_count': len(explored_global), 'explored': explored_render,
                        'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                    })
                    return steps

                steps.append({
                    'type': 'cutoff', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                    'moves': moves, 'path': path, 'frontier': frontier_render, 'frontier_count': len(frontier),
                    'visited_count': len(explored_global), 'explored': explored_render,
                    'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                })
                continue

            # Check goal
            if state == goal:
                explored_global.append((state, f_score, moves, g_score, f_score - g_score))
                explored_render = [
                    (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start', exp_node[3], exp_node[4])
                    for exp_node in explored_global[-12:]
                ]
                if len(steps) >= MAX_STEPS:
                    steps.append({
                        'type': 'limit_reached', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                        'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                        'frontier': frontier_render, 'frontier_count': len(frontier),
                        'visited_count': len(explored_global), 'explored': explored_render,
                        'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                    })
                    return steps

                steps.append({
                    'type': 'goal', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                    'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                    'frontier': frontier_render, 'frontier_count': len(frontier),
                    'visited_count': len(explored_global), 'explored': explored_render,
                    'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                })
                return steps

            # Expand neighbors
            added = []
            for nb, d in reversed(nbrs):
                nb_g = manhattan(nb)
                nb_h = misplaced(nb)
                nb_f = nb_g + nb_h
                frontier.append((nb, path+[nb], moves+[d], nb_g, nb_f))
                added.append((nb, d, nb_f))

            explored_global.append((state, f_score, moves, g_score, f_score - g_score))

            frontier_render = [
                {
                    'state': f_node[0],
                    'cost': f_node[4],
                    'g': f_node[3],
                    'h': f_node[4] - f_node[3],
                    'via': f_node[2][-1] if f_node[2] else 'start'
                }
                for f_node in list(reversed(frontier[-12:]))
            ]
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start', exp_node[3], exp_node[4])
                for exp_node in explored_global[-12:]
            ]

            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                    'moves': moves, 'path': path, 'neighbors': nbrs, 'added': added,
                    'frontier': frontier_render, 'frontier_count': len(frontier),
                    'visited_count': len(explored_global), 'explored': explored_render,
                    'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
                })
                return steps

            steps.append({
                'type': 'expand', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                'moves': moves, 'path': path, 'neighbors': nbrs, 'added': added,
                'frontier': frontier_render, 'frontier_count': len(frontier),
                'visited_count': len(explored_global), 'explored': explored_render,
                'depth': len(moves), 'limit': threshold, 'iteration': iteration_count,
            })

        if result == 'cutoff':
            threshold = next_threshold
        else:
            break

    return steps
