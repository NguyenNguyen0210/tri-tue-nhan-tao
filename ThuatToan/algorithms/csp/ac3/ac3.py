from algorithms.csp.csp_utils import (
    MAX_STEPS, VARIABLES, assignment_to_state, is_reachable, domains_to_state,
    init_domains, ac3_propagate, make_step, frontier_from_domains, bfs_moves,
    domain_size_sum,
)


def _append_path_steps(steps, explored, path, moves):
    if len(steps) >= MAX_STEPS:
        return
    steps.append(make_step(
        'new_iteration', path[0], {}, [], [path[0]], 0,
        explored, [], 0, len(explored), 0, limit=len(moves), iteration=1,
    ))
    for i in range(1, len(path)):
        if len(steps) >= MAX_STEPS:
            break
        state = path[i]
        move_so_far = moves[:i]
        explored.append((state, 0, move_so_far))
        frontier_render = [
            {'state': path[j], 'via': moves[j - 1] if j > 0 else 'start', 'depth': j, 'cost': 0}
            for j in range(i + 1, min(i + 5, len(path)))
        ]
        step_type = 'goal' if i == len(path) - 1 else 'expand'
        steps.append({
            'type': step_type,
            'state': state,
            'cost': 0,
            'moves': move_so_far,
            'path': path[: i + 1],
            'neighbors': [],
            'added': [(path[i], moves[i - 1], 0)] if i <= len(moves) else [],
            'frontier': frontier_render,
            'frontier_count': len(path) - i - 1,
            'visited_count': len(explored),
            'explored': [(e[0], e[1], e[2][-1] if e[2] else 'start') for e in explored[-12:]],
            'depth': i,
            'limit': len(moves),
            'iteration': 2,
        })


def ac3_steps(start, goal, goal_directed=True):
    steps = []
    explored = []

    if not is_reachable(start, goal):
        partial = assignment_to_state({})
        steps.append(make_step(
            'limit_reached', partial, {}, [], [partial], 9,
            explored, [], 0, 0, 0, limit=0,
        ))
        return steps

    domains = init_domains({}, goal, goal_directed=False)
    for var in VARIABLES:
        if var not in domains:
            domains[var] = set(range(9))

    ok, revisions = ac3_propagate(domains, goal, goal_directed)
    arc_count = 0

    for xi, xj, removed, snap in revisions:
        if len(steps) >= MAX_STEPS:
            break
        arc_count += 1
        state = domains_to_state(snap)
        explored.append((state, domain_size_sum(snap), [f'arc{arc_count}']))
        frontier = frontier_from_domains(snap, {}, goal)
        label = f'unary({xi})' if xj == 'unary' else f'({xi},{xj})'
        steps.append(make_step(
            'ac3_revise', state, {}, [], [state], domain_size_sum(snap),
            explored, frontier, len(snap), len(explored), arc_count,
            limit=len(removed), iteration=arc_count,
            added=[(state, label, len(removed))],
            domains=snap,
        ))

    if not ok:
        state = domains_to_state(domains)
        steps.append(make_step(
            'local_optimum', state, {}, [], [state], domain_size_sum(domains),
            explored, [], 0, len(explored), arc_count,
        ))
        return steps

    final_state = tuple(goal)
    explored.append((final_state, 0, ['ac3_done']))
    steps.append(make_step(
        'expand', final_state, {i: goal[i] for i in VARIABLES}, [], [final_state], 0,
        explored, [], 0, len(explored), 9,
        limit=arc_count, iteration=arc_count,
        domains={var: {goal[var]} for var in VARIABLES},
    ))

    if start != goal:
        path, move_list = bfs_moves(start, goal)
        if path and move_list:
            _append_path_steps(steps, explored, path, move_list)
        elif len(steps) < MAX_STEPS:
            steps.append(make_step(
                'goal', final_state, {i: goal[i] for i in VARIABLES}, [], [final_state], 0,
                explored, [], 0, len(explored), 9, limit=arc_count,
            ))
    elif steps[-1]['type'] != 'goal':
        steps.append(make_step(
            'goal', final_state, {i: goal[i] for i in VARIABLES}, [], [final_state], 0,
            explored, [], 0, len(explored), 9, limit=arc_count,
        ))

    return steps
