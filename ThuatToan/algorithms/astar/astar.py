import heapq
from ..utils import misplaced, manhattan, get_neighbors

def astar_steps(start, goal):
    counter = 0
    g_start = manhattan(start)
    h_start = misplaced(start)
    f_start = g_start + h_start
    
    # Priority Queue stores: (f_score, counter, state, path, moves, g_score)
    pq = [(f_start, counter, start, [start], [], g_start)]
    visited = {}  # state -> g_score (for optimal path updates)
    explored = []
    steps = []
    MAX_STEPS = 3000
    
    while pq:
        f_score, _, state, path, moves, g_score = heapq.heappop(pq)
        
        # Precompute frontier and explored render lists to avoid memory bloat
        frontier_render = [
            {
                'state': s_node[2],
                'cost': s_node[0],
                'g': s_node[5],
                'h': s_node[0] - s_node[5],
                'via': s_node[4][-1] if s_node[4] else 'start'
            }
            for s_node in heapq.nsmallest(16, pq)
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start', exp_node[3], exp_node[4])
            for exp_node in explored[-12:]
        ]
        
        # skip check if we already found a cheaper/equal path to this state
        if state in visited and visited[state] <= g_score:
            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                    'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                    'frontier': frontier_render, 'frontier_count': len(pq),
                    'visited_count': len(visited), 'explored': explored_render,
                    'depth': len(moves), 'limit': None, 'iteration': None,
                })
                break
            steps.append({
                'type': 'skip', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                'moves': moves, 'path': path,
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            continue
            
        visited[state] = g_score
        
        # Goal check upon POP
        if state == goal:
            steps.append({
                'type': 'goal', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        nbrs = get_neighbors(state)
        added = []
        for nb, d in nbrs:
            nb_g = manhattan(nb)
            if nb not in visited or nb_g < visited[nb]:
                nb_h = misplaced(nb)
                nb_f = nb_g + nb_h
                counter += 1
                heapq.heappush(pq, (nb_f, counter, nb, path+[nb], moves+[d], nb_g))
                added.append((nb, d, nb_f))
        
        explored.append((state, f_score, moves, g_score, f_score - g_score))
        
        # Recalculate frontier and explored render lists after expansion/exploration
        frontier_render = [
            {
                'state': s_node[2],
                'cost': s_node[0],
                'g': s_node[5],
                'h': s_node[0] - s_node[5],
                'via': s_node[4][-1] if s_node[4] else 'start'
            }
            for s_node in heapq.nsmallest(16, pq)
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start', exp_node[3], exp_node[4])
            for exp_node in explored[-12:]
        ]
        
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                'moves': moves, 'path': path, 'neighbors': nbrs, 'added': added,
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        steps.append({
            'type': 'expand', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
            'moves': moves, 'path': path,
            'neighbors': nbrs, 'added': added,
            'frontier': frontier_render, 'frontier_count': len(pq),
            'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None,
        })
        
    return steps
