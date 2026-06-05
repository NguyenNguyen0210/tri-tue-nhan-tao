from algorithms.utils import misplaced, manhattan, get_neighbors

def hillclimbing_steps(start, goal):
    steps = []
    MAX_STEPS = 3000

    current_state = start
    current_path = [start]
    current_moves = []
    explored_global = []

    while True:
        h_curr = manhattan(current_state)
        
        # Check goal
        if current_state == goal:
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
                for exp_node in explored_global[-12:]
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
                'visited_count': len(explored_global) + 1,
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': None
            })
            break

        nbrs = get_neighbors(current_state)
        better_neighbor = None
        better_d = None
        better_h = None

        # Simple Hill Climbing: find the FIRST neighbor strictly better than current
        for nb, d in nbrs:
            nb_h = manhattan(nb)
            if nb_h < h_curr:
                better_neighbor = nb
                better_d = d
                better_h = nb_h
                break

        # Render frontier and explored lists
        frontier_render = [
            {
                'state': nb,
                'cost': manhattan(nb),
                'g': None,
                'h': None,
                'via': d
            }
            for nb, d in nbrs
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored_global[-12:]
        ]

        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': None
            })
            break

        if better_neighbor is not None:
            # We found a strictly better neighbor
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [(better_neighbor, better_d, better_h)],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': None
            })
            
            explored_global.append((current_state, h_curr, current_moves))
            current_state = better_neighbor
            current_moves = current_moves + [better_d]
            current_path = current_path + [better_neighbor]
        else:
            # stuck in local optimum/plateau
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
                'visited_count': len(explored_global) + 1,
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': None
            })
            break

    return steps
