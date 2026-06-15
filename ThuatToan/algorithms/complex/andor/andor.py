from collections import deque
from algorithms.utils import get_neighbors, manhattan

perp_map = {
    '↑': ['←', '→'],
    '↓': ['←', '→'],
    '←': ['↑', '↓'],
    '→': ['↑', '↓']
}

def results_and_or(state, action):
    """
    Returns (primary, perpendiculars) blank tile outcomes.
    - primary: state resulting from moving blank in chosen direction.
    - perpendiculars: valid states resulting from moving blank in perpendicular directions.
    """
    nbrs = get_neighbors(state)
    primary = None
    for next_state, d in nbrs:
        if d == action:
            primary = next_state
            break
    if primary is None:
        return None, []
    
    perpendiculars = []
    for perp_d in perp_map[action]:
        for next_state, d in nbrs:
            if d == perp_d:
                perpendiculars.append(next_state)
    return primary, perpendiculars

def and_or_graph_search(start, goal):
    """
    Recursive depth-limited AND-OR graph search for 8-Puzzle.
    Returns (plan, memo) where plan is: state -> (action, subplans_dict)
    """
    memo = {}
    MAX_DEPTH = 8
    
    def or_search(state, path):
        if state == goal:
            return 'goal'
        if state in path:
            return None
        if len(path) > MAX_DEPTH:
            return None
        if state in memo:
            return memo[state]
            
        nbrs = get_neighbors(state)
        actions_sorted = []
        for next_state, d in nbrs:
            h = manhattan(next_state)
            actions_sorted.append((h, d))
        actions_sorted.sort()
        
        for _, action in actions_sorted:
            primary, perpendiculars = results_and_or(state, action)
            if primary is None:
                continue
            
            outcomes = [primary] + perpendiculars
            plan = and_search(outcomes, path + [state])
            if plan is not None:
                res = (action, plan)
                memo[state] = res
                return res
        
        memo[state] = None
        return None

    def and_search(states, path):
        plan = {}
        for s in states:
            p = or_search(s, path)
            if p is None:
                return None
            plan[s] = p
        return plan

    plan = or_search(start, [])
    return plan, memo

def solve_bfs(start, goal):
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path
        for nb, d in get_neighbors(state):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [d]))
    return None

def and_or_steps(start, goal):
    steps = []
    
    # Run AND-OR Search
    plan, memo = and_or_graph_search(start, goal)
    
    if plan is not None:
        curr = start
        moves = []
        path = [start]
        explored = []
        step_count = 0
        
        while curr != goal:
            node = memo.get(curr)
            if not node or node == 'goal':
                break
            action, subplans = node
            
            primary, perpendiculars = results_and_or(curr, action)
            
            frontier_render = []
            for alt_state in perpendiculars:
                alt_dir = 'start'
                for nb_s, nb_d in get_neighbors(curr):
                    if nb_s == alt_state:
                        alt_dir = nb_d
                        break
                frontier_render.append({
                    'state': alt_state,
                    'via': alt_dir,
                    'depth': len(moves) + 1
                })
            
            explored.append((curr, manhattan(curr), moves[-1] if moves else 'start'))
            explored_render = [
                (exp[0], exp[1], exp[2])
                for exp in explored[-12:]
            ]
            
            steps.append({
                'type': 'expand',
                'state': curr,
                'cost': manhattan(curr),
                'moves': list(moves),
                'path': list(path),
                'added': [(primary, action, len(moves) + 1)] + [(alt['state'], alt['via'], alt['depth']) for alt in frontier_render],
                'frontier': frontier_render,
                'frontier_count': len(frontier_render),
                'visited_count': len(explored),
                'explored': explored_render,
                'depth': len(moves),
                'limit': 1 + len(perpendiculars),
                'iteration': step_count
            })
            
            curr = primary
            moves.append(action)
            path.append(curr)
            step_count += 1
            
        explored.append((curr, manhattan(curr), moves[-1] if moves else 'start'))
        explored_render = [
            (exp[0], exp[1], exp[2])
            for exp in explored[-12:]
        ]
        steps.append({
            'type': 'goal',
            'state': curr,
            'cost': manhattan(curr),
            'moves': list(moves),
            'path': list(path),
            'added': [],
            'frontier': [],
            'frontier_count': 0,
            'visited_count': len(explored),
            'explored': explored_render,
            'depth': len(moves),
            'limit': 1,
            'iteration': step_count
        })
    else:
        # Fallback to deterministic BFS solver
        path = solve_bfs(start, goal)
        if path is not None:
            curr = start
            moves = []
            states_path = [start]
            explored = []
            step_count = 0
            
            for action in path:
                next_state = None
                for nb_s, nb_d in get_neighbors(curr):
                    if nb_d == action:
                        next_state = nb_s
                        break
                if next_state is None:
                    break
                
                explored.append((curr, manhattan(curr), moves[-1] if moves else 'start'))
                explored_render = [
                    (exp[0], exp[1], exp[2])
                    for exp in explored[-12:]
                ]
                
                steps.append({
                    'type': 'expand',
                    'state': curr,
                    'cost': manhattan(curr),
                    'moves': list(moves),
                    'path': list(states_path),
                    'added': [(next_state, action, len(moves) + 1)],
                    'frontier': [],
                    'frontier_count': 0,
                    'visited_count': len(explored),
                    'explored': explored_render,
                    'depth': len(moves),
                    'limit': 0, # fallback indicator
                    'iteration': step_count
                })
                
                curr = next_state
                moves.append(action)
                states_path.append(curr)
                step_count += 1
                
            explored.append((curr, manhattan(curr), moves[-1] if moves else 'start'))
            explored_render = [
                (exp[0], exp[1], exp[2])
                for exp in explored[-12:]
            ]
            steps.append({
                'type': 'goal',
                'state': curr,
                'cost': manhattan(curr),
                'moves': list(moves),
                'path': list(states_path),
                'added': [],
                'frontier': [],
                'frontier_count': 0,
                'visited_count': len(explored),
                'explored': explored_render,
                'depth': len(moves),
                'limit': 0,
                'iteration': step_count
            })
            
    return steps
