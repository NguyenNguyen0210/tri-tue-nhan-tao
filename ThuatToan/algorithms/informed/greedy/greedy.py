import heapq
from algorithms.utils import manhattan, get_neighbors

def greedy_steps(start, goal):
    counter = 0
    pq = [(manhattan(start), counter, start, [start], [])]
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
        nbrs = get_neighbors(state)
        added = []
        for nb, d in nbrs:
            if nb not in visited:
                nb_h = manhattan(nb)
                counter += 1
                heapq.heappush(pq, (nb_h, counter, nb, path+[nb], moves+[d]))
                added.append((nb, d, nb_h))
        
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
                'moves': moves, 'path': path, 'neighbors': nbrs, 'added': added,
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        steps.append({
            'type': 'goal' if state == goal else 'expand',
            'state': state, 'cost': cost,
            'moves': moves, 'path': path,
            'neighbors': nbrs, 'added': added,
            'frontier': frontier_render, 'frontier_count': len(pq),
            'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None,
        })
        if state == goal:
            break
            
    return steps
