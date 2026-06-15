from collections import deque
from algorithms.utils import get_neighbors, manhattan

def transition_belief(belief_state, d):
    """
    Transition a belief state (frozenset of states) by action/direction d.
    If the move d is blocked/invalid in any world, the agent remains in the same state in that world.
    """
    next_states = []
    for state in belief_state:
        nbrs = get_neighbors(state)
        moved = False
        for nb_s, nb_d in nbrs:
            if nb_d == d:
                next_states.append(nb_s)
                moved = True
                break
        if not moved:
            next_states.append(state)
    return frozenset(next_states)

def belief_state_steps(start, goal):
    """
    Belief State Search for 8-Puzzle.
    Simulates uncertainty: the agent is not sure if the board is in 'start' state
    or in 'start_alt' (obtained by applying the first legal move to 'start').
    Finds a single sequence of moves that solves both configurations.
    """
    steps = []
    MAX_STEPS = 2000
    
    # Generate alternate solvable state
    nbrs = get_neighbors(start)
    if nbrs:
        # Choose the first neighbor as start_alt
        start_alt = nbrs[0][0]
    else:
        start_alt = start
        
    initial_belief = frozenset([start, start_alt])
    
    # BFS on Belief States Space
    # Queue stores: (belief_state, moves, path_of_beliefs)
    frontier_q = deque([(initial_belief, [], [initial_belief])])
    visited = {initial_belief}
    
    explored = []
    step_count = 0
    
    while frontier_q:
        belief, moves, path = frontier_q.popleft()
        
        # Representative state for GUI rendering
        repr_state = list(belief)[0]
        h_repr = manhattan(repr_state)
        explored.append((repr_state, h_repr, moves))
        
        frontier_render = [
            {
                'state': list(fn[0])[0],
                'via': fn[1][-1] if fn[1] else 'start',
                'depth': len(fn[1]),
                'belief_size': len(fn[0])
            }
            for fn in list(frontier_q)[:12]
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored[-12:]
        ]
        
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached',
                'state': repr_state,
                'cost': h_repr,
                'moves': moves,
                'path': [list(b)[0] for b in path],
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(frontier_q),
                'visited_count': len(visited),
                'explored': explored_render,
                'depth': len(moves),
                'limit': len(belief),
                'iteration': step_count
            })
            break
            
        # Goal check: All worlds in the belief state must be at the goal state
        is_goal = all(state == goal for state in belief)
        
        if is_goal:
            steps.append({
                'type': 'goal',
                'state': repr_state,
                'cost': h_repr,
                'moves': moves,
                'path': [list(b)[0] for b in path],
                'neighbors': [],
                'added': [],
                'frontier': frontier_render,
                'frontier_count': len(frontier_q),
                'visited_count': len(visited),
                'explored': explored_render,
                'depth': len(moves),
                'limit': len(belief),
                'iteration': step_count
            })
            break
            
        # Try 4 moves (directions)
        added = []
        for d in ['↑', '↓', '←', '→']:
            next_belief = transition_belief(belief, d)
            if next_belief not in visited:
                visited.add(next_belief)
                frontier_q.append((next_belief, moves + [d], path + [next_belief]))
                next_repr = list(next_belief)[0]
                added.append((next_repr, d, len(moves) + 1))
                
        # Recompute frontier render
        frontier_render = [
            {
                'state': list(fn[0])[0],
                'via': fn[1][-1] if fn[1] else 'start',
                'depth': len(fn[1]),
                'belief_size': len(fn[0])
            }
            for fn in list(frontier_q)[:12]
        ]
        
        steps.append({
            'type': 'expand',
            'state': repr_state,
            'cost': h_repr,
            'moves': moves,
            'path': [list(b)[0] for b in path],
            'neighbors': [],
            'added': added,
            'frontier': frontier_render,
            'frontier_count': len(frontier_q),
            'visited_count': len(visited),
            'explored': explored_render,
            'depth': len(moves),
            'limit': len(belief),
            'iteration': step_count
        })
        step_count += 1
        
    return steps
