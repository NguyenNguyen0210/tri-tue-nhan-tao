from collections import deque
from algorithms.utils import get_neighbors

def bfs_steps(start, goals, walls):
    """
    Hiện thực thuật toán BFS cho Sokoban.
    Trả về danh sách các bước chạy để phục vụ giao diện trực quan hóa.
    """
    steps = []
    MAX_STEPS = 3000
    
    frontier_q = deque([(start, [start], [])])
    frontier_set = {start}
    
    explored_set = set()
    explored_list = []
    
    while frontier_q:
        state, path, moves = frontier_q.popleft()
        frontier_set.remove(state)
        
        if state not in explored_set:
            explored_set.add(state)
            explored_list.append((state, len(moves), moves))
            
        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': len(f_node[2])}
            for f_node in list(frontier_q)[:12]
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
                'frontier_count': len(frontier_q),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None
            })
            break
            
        # Goal check upon POP
        if set(state[1]) == goals:
            steps.append({
                'type': 'goal',
                'state': state,
                'moves': moves,
                'path': path,
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(frontier_q),
                'visited_count': len(explored_set),
                'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None
            })
            break
            
        nbrs = get_neighbors(state, walls, goals)
        added = []
        
        for nb_state, d, is_push in nbrs:
            if nb_state not in explored_set and nb_state not in frontier_set:
                child_path = path + [nb_state]
                child_moves = moves + [d]
                
                frontier_q.append((nb_state, child_path, child_moves))
                frontier_set.add(nb_state)
                added.append((nb_state, d, len(child_moves)))
                
        # Recompute frontier render after queue additions
        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': len(f_node[2])}
            for f_node in list(frontier_q)[:12]
        ]
        
        steps.append({
            'type': 'expand',
            'state': state,
            'moves': moves,
            'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ],
            'added': added,
            'frontier': frontier_render,
            'frontier_count': len(frontier_q),
            'visited_count': len(explored_set),
            'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None
        })
            
    return steps
