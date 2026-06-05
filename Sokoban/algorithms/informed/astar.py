import heapq
from algorithms.utils import get_neighbors, manhattan

def astar_steps(start, goals, walls):
    """
    Hiện thực thuật toán A* Search cho Sokoban.
    Sắp xếp Frontier dựa theo giá trị f(n) = g(n) + h(n).
    """
    counter = 0
    g_start = 0
    h_start = manhattan(start, goals)
    f_start = g_start + h_start
    
    # Priority Queue stores: (f_score, counter, state, path, moves, g_score)
    pq = [(f_start, counter, start, [start], [], g_start)]
    visited = {} # state -> g_score
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
        if set(state[1]) == goals:
            steps.append({
                'type': 'goal', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
                'moves': moves, 'path': path, 'neighbors': [], 'added': [],
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        nbrs = get_neighbors(state, walls, goals)
        added = []
        for nb_state, d, is_push in nbrs:
            # For Sokoban, step cost is always 1
            nb_g = g_score + 1
            if nb_state not in visited or nb_g < visited[nb_state]:
                nb_h = manhattan(nb_state, goals)
                nb_f = nb_g + nb_h
                counter += 1
                heapq.heappush(pq, (nb_f, counter, nb_state, path+[nb_state], moves+[d], nb_g))
                added.append((nb_state, d, nb_f))
        
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
                'moves': moves, 'path': path, 'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added,
                'frontier': frontier_render, 'frontier_count': len(pq),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None,
            })
            break
            
        steps.append({
            'type': 'expand', 'state': state, 'cost': f_score, 'g': g_score, 'h': f_score - g_score,
            'moves': moves, 'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added,
            'frontier': frontier_render, 'frontier_count': len(pq),
            'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None,
        })
            
    return steps
