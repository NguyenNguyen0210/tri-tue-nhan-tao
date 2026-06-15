import random
import math
from algorithms.utils import manhattan, get_neighbors

def simulated_annealing_steps(start, goal):
    steps = []
    MAX_STEPS = 3000

    current_state = start
    current_path = [start]
    current_moves = []
    explored_global = []

    # Simulated Annealing parameters
    T = 100.0
    cooling_rate = 0.95
    min_T = 0.01

    step_count = 0

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
                'limit': round(T, 2),
                'iteration': step_count
            })
            break

        nbrs = get_neighbors(current_state)
        if not nbrs:
            # stuck / no neighbors
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
                for exp_node in explored_global[-12:]
            ]
            steps.append({
                'type': 'local_optimum',
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
                'limit': round(T, 2),
                'iteration': step_count
            })
            break

        # Select a random neighbor
        nb, d = random.choice(nbrs)
        nb_h = manhattan(nb)
        delta_E = nb_h - h_curr

        accept = False
        if delta_E < 0:
            accept = True
        else:
            p = math.exp(-delta_E / T) if T > 0 else 0.0
            if random.random() < p:
                accept = True

        # Arrange frontier so that the evaluated neighbor is at index 0
        frontier_nbrs = [(nb, d)] + [n for n in nbrs if n[0] != nb]
        frontier_render = [
            {
                'state': n,
                'cost': manhattan(n),
                'g': None,
                'h': None,
                'via': direction
            }
            for n, direction in frontier_nbrs
        ]

        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored_global[-12:]
        ]

        if len(steps) >= MAX_STEPS or T < min_T:
            steps.append({
                'type': 'limit_reached' if len(steps) >= MAX_STEPS else 'local_optimum',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': round(T, 2),
                'iteration': step_count
            })
            break

        if accept:
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [(nb, d, nb_h)],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': round(T, 2),
                'iteration': step_count
            })
            
            explored_global.append((current_state, h_curr, current_moves))
            current_state = nb
            current_moves = current_moves + [d]
            current_path = current_path + [nb]
        else:
            # We rejected the neighbor, so we stay at the current state, but T still decreases
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': round(T, 2),
                'iteration': step_count
            })

        # Cooling schedule
        T *= cooling_rate
        step_count += 1

    return steps
