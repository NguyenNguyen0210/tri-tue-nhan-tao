from algorithms.utils import get_neighbors, manhattan

def expectimax_steps(start, goal, max_depth=4):
    steps = []
    MAX_STEPS = 1000
    
    explored_set = set()
    explored_list = []
    
    def utility(s):
        if s == goal:
            return 1000
        return -manhattan(s)

    state_path = [start]
    moves_path = []
    
    def evaluate_node(state, depth, is_max, path, moves):
        nonlocal steps
        if len(steps) >= MAX_STEPS:
            return utility(state), None

        if state not in explored_set:
            explored_set.add(state)
            explored_list.append((state, round(utility(state), 2), moves[-1] if moves else 'start'))
            
        nbrs = get_neighbors(state)
        
        frontier_render = [
            {'state': nb, 'via': d, 'cost': utility(nb)}
            for nb, d in nbrs[:12]
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2])
            for exp_node in explored_list[-12:]
        ]

        if state == goal:
            steps.append({
                'type': 'goal',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': depth, 'cost': 1000, 'limit': 'MAX win', 'iteration': 'MAX' if is_max else 'CHANCE'
            })
            return 1000, None

        if depth >= max_depth:
            val = utility(state)
            steps.append({
                'type': 'expand',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': nbrs,
                'added': [(nb, d, utility(nb)) for nb, d in nbrs],
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': depth, 'cost': round(val, 2), 'limit': f'Depth {depth}', 'iteration': 'MAX' if is_max else 'CHANCE'
            })
            return val, None

        best_move = None
        added_list = []

        if is_max:
            best_val = -float('inf')
            for nb, d in nbrs:
                val, _ = evaluate_node(nb, depth + 1, False, path + [nb], moves + [d])
                added_list.append((nb, d, round(val, 2)))
                if val > best_val:
                    best_val = val
                    best_move = d
            
            steps.append({
                'type': 'expand',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': nbrs,
                'added': added_list,
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': depth, 'cost': round(best_val, 2), 'limit': 'MAX choice', 'iteration': 'MAX'
            })
            return best_val, best_move
        else:
            total_val = 0
            count = len(nbrs)
            for nb, d in nbrs:
                val, _ = evaluate_node(nb, depth + 1, True, path + [nb], moves + [d])
                added_list.append((nb, d, round(val, 2)))
                total_val += val
            
            expected_val = total_val / count if count > 0 else 0
            steps.append({
                'type': 'expand',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': nbrs,
                'added': added_list,
                'frontier': frontier_render,
                'frontier_count': len(nbrs),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': depth, 'cost': round(expected_val, 2), 'limit': f'E[x] ({count} outcomes)', 'iteration': 'CHANCE'
            })
            return expected_val, None

    evaluate_node(start, 0, True, state_path, moves_path)
    return steps
