from algorithms.utils import get_neighbors

def dfs_steps(start, goal):
    steps = []
    MAX_STEPS = 3000
    
    frontier = [(start, [start], [])]
    frontier_set = {start}
    
    explored_set = set()
    explored_list = []
    
    while frontier:
        state, path, moves = frontier.pop()
        frontier_set.remove(state)
        
        if state not in explored_set:
            explored_set.add(state)
            explored_list.append((state, len(moves), moves))
            
        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': len(f_node[2])}
            for f_node in list(reversed(frontier[-12:]))
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored_list[-12:]
        ]
        
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(frontier),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None
            })
            break
            
        # Goal check upon POP
        if state == goal:
            steps.append({
                'type': 'goal',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(frontier),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None
            })
            break
            
        nbrs = get_neighbors(state)
        added = []
        
        for nb, d in reversed(nbrs):
            if nb not in explored_set and nb not in frontier_set:
                child_path = path + [nb]
                child_moves = moves + [d]
                
                frontier.append((nb, child_path, child_moves))
                frontier_set.add(nb)
                added.append((nb, d, len(child_moves)))
                
        # Recompute frontier render after stack additions
        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': len(f_node[2])}
            for f_node in list(reversed(frontier[-12:]))
        ]
        
        steps.append({
            'type': 'expand',
            'state': state,
            'moves': moves,
            'path': path,
            'neighbors': nbrs,
            'added': added,
            'frontier': frontier_render,
            'frontier_count': len(frontier),
            'visited_count': len(explored_set),
            'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None
        })
        
    return steps
