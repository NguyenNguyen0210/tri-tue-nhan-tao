import random
from ..utils import manhattan, get_neighbors

def stochastic_hillclimbing_steps(start, goal):
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
        
        # Stochastic Hill Climbing: filter all neighbors that are strictly better than current state
        better_neighbors = []
        for nb, d in nbrs:
            nb_h = manhattan(nb)
            if nb_h < h_curr:
                better_neighbors.append((nb, d, nb_h))
                
        # If we have better neighbors, choose one randomly
        chosen_nb = None
        chosen_d = None
        chosen_h = None
        if better_neighbors:
            chosen_nb, chosen_d, chosen_h = random.choice(better_neighbors)

        # Arrange frontier so that the chosen neighbor is at index 0 (if there is one)
        # We still want to show all neighbors of current state in the frontier list.
        # Let's put the chosen neighbor at the front.
        frontier_nbrs = []
        if chosen_nb is not None:
            # First element is the chosen one
            frontier_nbrs.append((chosen_nb, chosen_d))
            # Followed by all other neighbors
            for nb, d in nbrs:
                if nb != chosen_nb:
                    frontier_nbrs.append((nb, d))
        else:
            # If no neighbor is chosen, just use the original neighbors list
            frontier_nbrs = nbrs

        frontier_render = [
            {
                'state': nb,
                'cost': manhattan(nb),
                'g': None,
                'h': None,
                'via': d
            }
            for nb, d in frontier_nbrs
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

        if chosen_nb is not None:
            # We found better neighbor and chose one randomly
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': nbrs,
                'added': [(chosen_nb, chosen_d, chosen_h)],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': None
            })
            
            explored_global.append((current_state, h_curr, current_moves))
            current_state = chosen_nb
            current_moves = current_moves + [chosen_d]
            current_path = current_path + [chosen_nb]
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
