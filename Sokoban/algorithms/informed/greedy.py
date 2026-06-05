import heapq
from algorithms.utils import get_neighbors, manhattan

def greedy_steps(start, goals, walls):
    """
    Hiện thực thuật toán Greedy Best-First Search cho Sokoban.
    Sắp xếp Frontier dựa theo giá trị Heuristic h(n) Manhattan.
    """
    counter = 0
    h_start = manhattan(start, goals)
    pq = [(h_start, counter, start, [start], [])]
    visited = set()
    explored = []
    steps = []
    MAX_STEPS = 3000
    
    while pq:
        cost, _, state, path, moves = heapq.heappop(pq)
        
        # Precompute frontier and explored render lists to avoid memory bloat
        frontier_render = [
            {'state': s_node[2], 'cost': s_node[0], 'via': s_node[4][-1] if s_node[4] else 'start'}
            for s_node in heapq.nsmallest(16, pq)
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored[-12:]
        ]
        
        if state in visited:
            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached', 'state': state, 'cost': cost,
                    'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                    'frontier': frontier_render, 'frontier_count': len(pq),
                    'visited_count': len(visited), 'explored': explored_render,
                    'depth': len(moves), 'limit': None, 'iteration': None,
                })
                break
            steps.append({
                'type': 'skip', 'state': state, 'cost': cost,
                'moves': moves, 'path': path,
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            continue
            
        visited.add(state)
        
        # Goal check upon POP
        if set(state[1]) == goals:
            steps.append({
                'type': 'goal', 'state': state, 'cost': cost,
                'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        nbrs = get_neighbors(state, walls, goals)
        added = []
        for nb_state, d, is_push in nbrs:
            if nb_state not in visited:
                nb_h = manhattan(nb_state, goals)
                counter += 1
                heapq.heappush(pq, (nb_h, counter, nb_state, path+[nb_state], moves+[d]))
                added.append((nb_state, d, nb_h))
        
        explored.append((state, cost, moves))
        
        # Recalculate frontier and explored render lists after expansion/exploration
        frontier_render = [
            {'state': s_node[2], 'cost': s_node[0], 'via': s_node[4][-1] if s_node[4] else 'start'}
            for s_node in heapq.nsmallest(16, pq)
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored[-12:]
        ]
        
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached', 'state': state, 'cost': cost,
                'moves': moves, 'path': path, 'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added,
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        steps.append({
            'type': 'expand', 'state': state, 'cost': cost,
            'moves': moves, 'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added,
            'frontier': frontier_render, 'frontier_count': len(pq),
            'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None,
        })
            
    return steps
