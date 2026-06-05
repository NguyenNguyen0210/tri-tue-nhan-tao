import random
from algorithms.utils import manhattan, get_neighbors

def localbeam_steps(start, goal, k=4):
    steps = []
    MAX_STEPS = 3000
    
    # beam elements: (state, h, moves, path)
    beam = [(start, manhattan(start), [], [start])]
    explored_global = [] # For rendering explored list

    # initial check
    if start == goal:
        steps.append({
            'type': 'goal',
            'state': start,
            'cost': manhattan(start),
            'moves': [],
            'path': [start],
            'neighbors': [],
            'added': [],
            'frontier': [],
            'frontier_count': 0,
            'visited_count': 1,
            'explored': [(start, manhattan(start), 'start')],
            'depth': 0,
            'limit': k,
            'iteration': None
        })
        return steps

    step_count = 0
    while True:
        # Check if limit reached
        if len(steps) >= MAX_STEPS:
            best_node = min(beam, key=lambda x: x[1])
            steps.append({
                'type': 'limit_reached',
                'state': best_node[0],
                'cost': best_node[1],
                'moves': best_node[2],
                'path': best_node[3],
                'neighbors': [],
                'added': [],
                'frontier': [],
                'frontier_count': len(beam),
                'visited_count': len(explored_global),
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(best_node[2]),
                'limit': k,
                'iteration': None
            })
            break
            
        step_count += 1
        
        # The best state currently in beam (for visualization as current_state)
        current_best = min(beam, key=lambda x: x[1])
        
        # Generate all successors of all states in beam
        all_successors = []
        for state, h, moves, path in beam:
            if state not in [e[0] for e in explored_global]:
                explored_global.append((state, h, moves))
                
            nbrs = get_neighbors(state)
            for nb, d in nbrs:
                # avoid simple cycles (don't go back to the immediate parent)
                if len(path) > 1 and nb == path[-2]:
                    continue
                nb_h = manhattan(nb)
                nb_moves = moves + [d]
                nb_path = path + [nb]
                all_successors.append((nb, nb_h, nb_moves, nb_path))
                
        # Check if goal is in successors
        goal_node = None
        for succ in all_successors:
            if succ[0] == goal:
                goal_node = succ
                break
                
        if goal_node:
            steps.append({
                'type': 'goal',
                'state': goal_node[0],
                'cost': goal_node[1],
                'moves': goal_node[2],
                'path': goal_node[3],
                'neighbors': [],
                'added': [],
                'frontier': [],
                'frontier_count': len(all_successors),
                'visited_count': len(explored_global) + 1,
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(goal_node[2]),
                'limit': k,
                'iteration': None
            })
            break
            
        if not all_successors:
            # Dead end (local optimum and no neighbors)
            steps.append({
                'type': 'local_optimum',
                'state': current_best[0],
                'cost': current_best[1],
                'moves': current_best[2],
                'path': current_best[3],
                'neighbors': [],
                'added': [],
                'frontier': [],
                'frontier_count': 0,
                'visited_count': len(explored_global),
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(current_best[2]),
                'limit': k,
                'iteration': None
            })
            break
            
        # Select best k successors
        # Sort by heuristic ascending
        all_successors.sort(key=lambda x: x[1])
        # Eliminate duplicates in successors (multiple parents could generate the same state)
        unique_successors = []
        seen = set()
        for succ in all_successors:
            if succ[0] not in seen:
                seen.add(succ[0])
                unique_successors.append(succ)
                
        next_beam = unique_successors[:k]
        
        # Prepare visualization info
        frontier_render = [
            {
                'state': nb,
                'cost': nb_h,
                'g': None,
                'h': None,
                'via': nb_moves[-1]
            }
            for nb, nb_h, nb_moves, nb_path in next_beam
        ]
        
        explored_render = [
            (exp[0], exp[1], exp[2][-1] if exp[2] else 'start')
            for exp in explored_global[-12:]
        ]
        
        # We step to the new beam
        steps.append({
            'type': 'expand',
            'state': current_best[0], # Just show the best of the previous beam as "current"
            'cost': current_best[1],
            'moves': current_best[2],
            'path': current_best[3],
            'neighbors': [ (s[0], s[2][-1]) for s in all_successors ], # just for info
            'added': [ (s[0], s[2][-1], s[1]) for s in next_beam ],
            'frontier': frontier_render,
            'frontier_count': len(all_successors), # Show how many we generated total
            'visited_count': len(explored_global),
            'explored': explored_render,
            'depth': len(current_best[2]),
            'limit': k,
            'iteration': None
        })
        
        # update beam
        beam = next_beam
        
    return steps
