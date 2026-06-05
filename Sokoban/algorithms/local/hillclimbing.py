from algorithms.utils import get_neighbors, manhattan

def hillclimbing_steps(start, goals, walls):
    """
    Hiện thực thuật toán Simple Hill Climbing cho Sokoban.
    Di chuyển đến lân cận đầu tiên tốt hơn hiện tại.
    """
    steps = []
    MAX_STEPS = 3000
    current_state = start
    current_path = [start]
    current_moves = []
    explored_global = []
    
    while True:
        h_curr = manhattan(current_state, goals)
        
        # Check goal
        if set(current_state[1]) == goals:
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
            
        nbrs = get_neighbors(current_state, walls, goals)
        better_neighbor = None
        better_d = None
        better_h = None
        
        # Simple HC: find the FIRST neighbor strictly better than current
        for nb_state, d, is_push in nbrs:
            nb_h = manhattan(nb_state, goals)
            if nb_h < h_curr:
                better_neighbor = nb_state
                better_d = d
                better_h = nb_h
                break
                
        frontier_render = [
            {
                'state': nb[0],
                'cost': manhattan(nb[0], goals),
                'g': None, 'h': None, 'via': nb[1]
            }
            for nb in nbrs
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
            steps.append({
                'type': 'expand',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [ (n[0], n[1]) for n in nbrs ],
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
            # Stuck in local optimum
            steps.append({
                'type': 'local_optimum',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [ (n[0], n[1]) for n in nbrs ],
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
