from ..utils import get_neighbors

def ids_steps(start, goal):
    steps = []
    explored_global = []  # tích lũy qua các iteration
    MAX_STEPS = 3000

    for limit in range(0, 50):
        # ── DEPTH-LIMITED-SEARCH(problem, limit) ──
        # frontier ← LIFO queue (stack) with NODE(start)
        # mỗi phần tử: (state, path, moves, depth)
        frontier = [(start, [start], [], 0)]
        result = 'failure'

        if len(steps) >= MAX_STEPS:
            break

        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': f_node[3]}
            for f_node in list(reversed(frontier[-12:]))
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored_global[-12:]
        ]

        steps.append({
            'type': 'new_iteration',
            'state': start, 'cost': 0,
            'moves': [], 'frontier': frontier_render,
            'frontier_count': len(frontier),
            'visited_count': len(explored_global),
            'explored': explored_render,
            'depth': 0, 'limit': limit, 'iteration': limit,
            'added': [], 'neighbors': [],
            'message': f'🔄 Bắt đầu iteration mới: depth limit = {limit}',
        })

        while frontier:
            # node ← POP(frontier)
            state, path, moves, depth = frontier.pop()
            nbrs = get_neighbors(state)

            frontier_render = [
                {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': f_node[3]}
                for f_node in list(reversed(frontier[-12:]))
            ]
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
                for exp_node in explored_global[-12:]
            ]

            # check IS-CYCLE: nếu state đã có trong path hiện tại → bỏ qua
            is_cycle = state in path[:-1]
            if is_cycle:
                if len(steps) >= MAX_STEPS:
                    steps.append({
                        'type': 'limit_reached', 'state': state, 'cost': depth,
                        'moves': moves, 'frontier': frontier_render,
                        'frontier_count': len(frontier),
                        'visited_count': len(explored_global),
                        'explored': explored_render,
                        'depth': depth, 'limit': limit, 'iteration': limit,
                        'added': [], 'neighbors': [],
                        'message': f'🔁 IS-CYCLE=True, bỏ qua (depth={depth})',
                    })
                    return steps

                steps.append({
                    'type': 'cycle', 'state': state, 'cost': depth,
                    'moves': moves, 'frontier': frontier_render,
                    'frontier_count': len(frontier),
                    'visited_count': len(explored_global),
                    'explored': explored_render,
                    'depth': depth, 'limit': limit, 'iteration': limit,
                    'added': [], 'neighbors': [],
                    'message': f'🔁 IS-CYCLE=True, bỏ qua (depth={depth})',
                })
                continue

            # if IS-GOAL(node.STATE) → return node
            if state == goal:
                explored_global.append((state, depth, moves))
                explored_render = [
                    (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
                    for exp_node in explored_global[-12:]
                ]
                if len(steps) >= MAX_STEPS:
                    steps.append({
                        'type': 'limit_reached', 'state': state, 'cost': depth,
                        'moves': moves, 'path': path,
                        'frontier': frontier_render,
                        'frontier_count': len(frontier),
                        'visited_count': len(explored_global),
                        'explored': explored_render,
                        'depth': depth, 'limit': limit, 'iteration': limit,
                        'added': [], 'neighbors': nbrs,
                        'message': f'✅ GOAL tìm thấy! depth={depth}, limit={limit}',
                    })
                    return steps

                steps.append({
                    'type': 'goal', 'state': state, 'cost': depth,
                    'moves': moves, 'path': path,
                    'frontier': frontier_render,
                    'frontier_count': len(frontier),
                    'visited_count': len(explored_global),
                    'explored': explored_render,
                    'depth': depth, 'limit': limit, 'iteration': limit,
                    'added': [], 'neighbors': nbrs,
                    'message': f'✅ GOAL tìm thấy! depth={depth}, limit={limit}',
                })
                return steps

            # if DEPTH(node) >= l → result ← cutoff
            if depth >= limit:
                result = 'cutoff'
                if len(steps) >= MAX_STEPS:
                    steps.append({
                        'type': 'limit_reached', 'state': state, 'cost': depth,
                        'moves': moves, 'frontier': frontier_render,
                        'frontier_count': len(frontier),
                        'visited_count': len(explored_global),
                        'explored': explored_render,
                        'depth': depth, 'limit': limit, 'iteration': limit,
                        'added': [], 'neighbors': [],
                        'message': f'✂️ CUTOFF: depth={depth} >= limit={limit}',
                    })
                    return steps

                steps.append({
                    'type': 'cutoff', 'state': state, 'cost': depth,
                    'moves': moves, 'frontier': frontier_render,
                    'frontier_count': len(frontier),
                    'visited_count': len(explored_global),
                    'explored': explored_render,
                    'depth': depth, 'limit': limit, 'iteration': limit,
                    'added': [], 'neighbors': [],
                    'message': f'✂️ CUTOFF: depth={depth} >= limit={limit}',
                })
                continue

            # else if not IS-CYCLE(node) → expand
            added = []
            for nb, d in reversed(nbrs):  # reversed để LIFO ra đúng thứ tự
                frontier.append((nb, path+[nb], moves+[d], depth+1))
                added.append((nb, d, depth+1))

            explored_global.append((state, depth, moves))

            # Recompute frontier and explored render lists after queue additions
            frontier_render = [
                {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': f_node[3]}
                for f_node in list(reversed(frontier[-12:]))
            ]
            explored_render = [
                (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
                for exp_node in explored_global[-12:]
            ]

            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached', 'state': state, 'cost': depth,
                    'moves': moves, 'path': path,
                    'neighbors': nbrs, 'added': added,
                    'frontier': frontier_render,
                    'frontier_count': len(frontier),
                    'visited_count': len(explored_global),
                    'explored': explored_render,
                    'depth': depth, 'limit': limit, 'iteration': limit,
                    'message': f'🔍 Expand depth={depth}/{limit}, thêm {len(added)} con vào stack',
                })
                return steps

            steps.append({
                'type': 'expand', 'state': state, 'cost': depth,
                'moves': moves, 'path': path,
                'neighbors': nbrs, 'added': added,
                'frontier': frontier_render,
                'frontier_count': len(frontier),
                'visited_count': len(explored_global),
                'explored': explored_render,
                'depth': depth, 'limit': limit, 'iteration': limit,
                'message': f'🔍 Expand depth={depth}/{limit}, thêm {len(added)} con vào stack',
            })

        # if result ≠ cutoff → return result (failure)
        if result != 'cutoff':
            break

    return steps
