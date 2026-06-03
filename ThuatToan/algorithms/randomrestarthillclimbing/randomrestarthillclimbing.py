import random
from ..utils import manhattan, get_neighbors

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions % 2 == 0

def generate_random_solvable_state(goal):
    while True:
        state = list(range(9))
        random.shuffle(state)
        state_tuple = tuple(state)
        if state_tuple != goal and is_solvable(state_tuple):
            return state_tuple

def random_restart_hillclimbing_steps(start, goal):
    steps = []
    MAX_STEPS = 3000
    restart_count = 0

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
                'limit': restart_count,
                'iteration': None
            })
            break

        if len(steps) >= MAX_STEPS:
            # Render frontier and explored lists
            nbrs = get_neighbors(current_state)
            sorted_nbrs = sorted(nbrs, key=lambda x: manhattan(x[0]))
            frontier_render = [
                {
                    'state': nb,
                    'cost': manhattan(nb),
                    'g': None,
                    'h': None,
                    'via': d
                }
                for nb, d in sorted_nbrs
            ]
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
                for exp_node in explored_global[-12:]
            ]
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
                'limit': restart_count,
                'iteration': None
            })
            break

        nbrs = get_neighbors(current_state)
        
        # Evaluate all neighbors to find the best one
        best_neighbor = None
        best_d = None
        best_h = float('inf')

        for nb, d in nbrs:
            nb_h = manhattan(nb)
            if nb_h < best_h:
                best_h = nb_h
                best_neighbor = nb
                best_d = d

        # Sort neighbors by heuristic value ascending for frontier rendering
        sorted_nbrs = sorted(nbrs, key=lambda x: manhattan(x[0]))
        frontier_render = [
            {
                'state': nb,
                'cost': manhattan(nb),
                'g': None,
                'h': None,
                'via': d
            }
            for nb, d in sorted_nbrs
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored_global[-12:]
        ]

        # Move if the best neighbor is strictly better than current
        if best_neighbor is not None and best_h < h_curr:
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [(best_neighbor, best_d, best_h)],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': restart_count,
                'iteration': None
            })
            
            explored_global.append((current_state, h_curr, current_moves))
            current_state = best_neighbor
            current_moves = current_moves + [best_d]
            current_path = current_path + [best_neighbor]
        else:
            # Stuck in local optimum/plateau: restart!
            new_start = generate_random_solvable_state(goal)
            steps.append({
                'type': 'restart',
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
                'limit': restart_count,
                'iteration': new_start
            })
            
            # Record current state as explored before restarting
            explored_global.append((current_state, h_curr, current_moves))
            
            # Restart parameters
            restart_count += 1
            current_state = new_start
            current_moves = []
            current_path = [new_start]

    return steps
