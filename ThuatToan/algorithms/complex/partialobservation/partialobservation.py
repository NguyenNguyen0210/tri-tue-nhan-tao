from collections import deque
from algorithms.utils import get_neighbors, manhattan

def count_inversions(state):
    tiles = [v for v in state if v != 0]
    inv = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inv += 1
    return inv

def is_solvable(state, goal):
    return (count_inversions(state) % 2) == (count_inversions(goal) % 2)

def get_assumed_state(true_state, revealed_indices, goal):
    revealed_values = {true_state[i] for i in revealed_indices}
    remaining_values = [v for v in goal if v not in revealed_values]
    
    assumed = list(true_state)
    rem_idx = 0
    for i in range(9):
        if i not in revealed_indices:
            assumed[i] = remaining_values[rem_idx]
            rem_idx += 1
            
    assumed_tuple = tuple(assumed)
    
    # 1. Ensure the assumed state is solvable
    if not is_solvable(assumed_tuple, goal):
        unrevealed = [i for i in range(9) if i not in revealed_indices]
        if len(unrevealed) >= 2:
            idx1, idx2 = unrevealed[0], unrevealed[1]
            assumed[idx1], assumed[idx2] = assumed[idx2], assumed[idx1]
            assumed_tuple = tuple(assumed)
            
    # 2. Prevent false goal belief if the assumed state equals goal but true state does not
    if assumed_tuple == goal and true_state != goal:
        unrevealed = [i for i in range(9) if i not in revealed_indices]
        if len(unrevealed) >= 3:
            idx1, idx2, idx3 = unrevealed[0], unrevealed[1], unrevealed[2]
            # Perform a 3-cycle swap (which is parity-preserving) to make it different
            assumed[idx1], assumed[idx2], assumed[idx3] = assumed[idx2], assumed[idx3], assumed[idx1]
            assumed_tuple = tuple(assumed)
            
    return assumed_tuple

def solve_bfs(start_assumed, goal):
    if start_assumed == goal:
        return []
        
    queue = deque([(start_assumed, [])])
    visited = {start_assumed}
    
    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path
            
        for nb, d in get_neighbors(state):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [d]))
    return None

def partial_observation_steps(start, goal):
    steps = []
    MAX_STEPS = 500
    
    # 1. Initialize revealed indices with blank position and its neighbors
    blank_idx = start.index(0)
    revealed_indices = {blank_idx}
    r, c = blank_idx // 3, blank_idx % 3
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            revealed_indices.add(nr * 3 + nc)
            
    # Initial assumed state
    current_assumed = get_assumed_state(start, revealed_indices, goal)
    
    current_state = start
    current_moves = []
    current_path = [start]
    explored_global = []
    planned_moves = []
    step_count = 0
    
    def make_foggy_state(true_state, revealed):
        return tuple(true_state[i] if i in revealed else -1 for i in range(9))
        
    while True:
        # Check goal
        if current_state == goal:
            explored_global.append((current_state, len(current_moves), current_moves))
            explored_render = [
                (exp[0], exp[1], exp[2][-1] if exp[2] else 'start')
                for exp in explored_global[-12:]
            ]
            steps.append({
                'type': 'goal',
                'state': current_state,
                'cost': manhattan(current_state),
                'moves': current_moves,
                'path': current_path,
                'neighbors': [],
                'added': [],
                'frontier': [],
                'frontier_count': 0,
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': step_count
            })
            break
            
        if step_count >= MAX_STEPS:
            explored_global.append((current_state, len(current_moves), current_moves))
            explored_render = [
                (exp[0], exp[1], exp[2][-1] if exp[2] else 'start')
                for exp in explored_global[-12:]
            ]
            steps.append({
                'type': 'limit_reached',
                'state': current_state,
                'cost': manhattan(current_state),
                'moves': current_moves,
                'path': current_path,
                'neighbors': [],
                'added': [],
                'frontier': [],
                'frontier_count': 0,
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': len(current_moves),
                'limit': None,
                'iteration': step_count
            })
            break
            
        # Replan using BFS if we run out of planned moves
        replan_occurred = False
        if not planned_moves:
            planned_moves = solve_bfs(current_assumed, goal)
            replan_occurred = True
            if not planned_moves:
                explored_global.append((current_state, len(current_moves), current_moves))
                explored_render = [
                    (exp[0], exp[1], exp[2][-1] if exp[2] else 'start')
                    for exp in explored_global[-12:]
                ]
                steps.append({
                    'type': 'local_optimum',
                    'state': current_state,
                    'cost': manhattan(current_state),
                    'moves': current_moves,
                    'path': current_path,
                    'neighbors': [],
                    'added': [],
                    'frontier': [],
                    'frontier_count': 0,
                    'visited_count': len(explored_global),
                    'explored': explored_render,
                    'depth': len(current_moves),
                    'limit': None,
                    'iteration': step_count
                })
                break
                
        # Move blank cell
        move = planned_moves.pop(0)
        nbrs = get_neighbors(current_state)
        next_state = None
        for nb, d in nbrs:
            if d == move:
                next_state = nb
                break
                
        if next_state is None:
            break
            
        # Add to explored
        explored_global.append((current_state, len(current_moves), current_moves))
        
        # Calculate next reveals
        next_blank_idx = next_state.index(0)
        new_reveals = {next_blank_idx}
        r, c = next_blank_idx // 3, next_blank_idx % 3
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_reveals.add(nr * 3 + nc)
                
        # Check if the theoretical assumed state after the move matches the newly revealed elements
        next_assumed_theoretical = None
        for nb, d in get_neighbors(current_assumed):
            if d == move:
                next_assumed_theoretical = nb
                break
                
        mismatch = False
        if next_assumed_theoretical is None:
            mismatch = True
        else:
            for idx in new_reveals:
                if idx in revealed_indices:
                    continue
                if next_state[idx] != next_assumed_theoretical[idx]:
                    mismatch = True
                    break
                    
        revealed_indices.update(new_reveals)
        
        if mismatch:
            current_assumed = get_assumed_state(next_state, revealed_indices, goal)
            planned_moves = []
        else:
            current_assumed = next_assumed_theoretical
            
        # Prepare frontier rendering showing the planned path on assumed board
        frontier_render = []
        temp_state = current_assumed
        for pm in planned_moves[:12]:
            found = False
            for nb, d in get_neighbors(temp_state):
                if d == pm:
                    temp_state = nb
                    frontier_render.append({
                        'state': temp_state,
                        'via': pm,
                        'cost': manhattan(temp_state),
                        'g': None,
                        'h': None
                    })
                    found = True
                    break
            if not found:
                break
                
        explored_render = [
            (exp[0], exp[1], exp[2][-1] if exp[2] else 'start')
            for exp in explored_global[-12:]
        ]
        
        steps.append({
            'type': 'expand',
            'state': current_state,
            'cost': manhattan(current_state),
            'moves': current_moves,
            'path': current_path,
            'neighbors': [{'state': n, 'via': d} for n, d in nbrs],
            'added': [(next_state, move, len(current_moves) + 1)],
            'frontier': frontier_render,
            'frontier_count': len(planned_moves),
            'visited_count': len(explored_global),
            'explored': explored_render,
            'depth': len(current_moves),
            'limit': 1 if replan_occurred else 0,  # 1 = replanned in this step, 0 = reused plan
            'iteration': step_count
        })
        
        current_state = next_state
        current_moves = current_moves + [move]
        current_path = current_path + [next_state]
        step_count += 1
        
    return steps
