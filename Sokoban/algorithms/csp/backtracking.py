from algorithms.utils import get_neighbors

def backtracking_steps(start, goals, walls):
    """
    Hiện thực thuật toán Backtracking Search cho Sokoban (dưới dạng tìm kiếm quay lui).
    """
    steps = []
    MAX_STEPS = 3000
    
    # LIFO stack: (state, path, moves)
    stack = [(start, [start], [])]
    visited = set()
    explored = []
    
    while stack:
        state, path, moves = stack.pop()
        
        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': len(f_node[2])}
            for f_node in list(reversed(stack[-12:]))
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored[-12:]
        ]
        
        if state in visited:
            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached', 'state': state, 'moves': moves, 'path': path,
                    'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(stack),
                    'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                    'limit': None, 'iteration': None
                })
                break
            steps.append({
                'type': 'skip', 'state': state, 'moves': moves, 'path': path,
                'frontier': frontier_render, 'frontier_count': len(stack),
                'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                'limit': None, 'iteration': None
            })
            continue
            
        visited.add(state)
        explored.append((state, len(moves), moves))
        
        # Goal check
        if set(state[1]) == goals:
            steps.append({
                'type': 'goal', 'state': state, 'moves': moves, 'path': path,
                'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(stack),
                'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                'limit': None, 'iteration': None
            })
            break
            
        nbrs = get_neighbors(state, walls, goals)
        added = []
        for nb_state, d, is_push in nbrs:
            if nb_state not in visited:
                stack.append((nb_state, path + [nb_state], moves + [d]))
                added.append((nb_state, d, len(moves) + 1))
                
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached', 'state': state, 'moves': moves, 'path': path,
                'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added, 'frontier': frontier_render,
                'frontier_count': len(stack), 'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None
            })
            break
            
        steps.append({
            'type': 'expand', 'state': state, 'moves': moves, 'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added, 'frontier': frontier_render,
            'frontier_count': len(stack), 'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None
        })
        
    return steps
