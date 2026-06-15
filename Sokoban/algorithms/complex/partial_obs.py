from algorithms.utils import get_neighbors, manhattan

def run_astar_partial(start, goals, known_walls, known_boxes_set):
    """
    Hàm tìm kiếm A* nội bộ chạy trên bản đồ đã khám phá một phần.
    """
    import heapq
    counter = 0
    # State: (player_pos, boxes_tuple)
    start_boxes = tuple(sorted(list(known_boxes_set)))
    start_state = (start[0], start_boxes)
    h_start = manhattan(start_state, goals)
    
    pq = [(h_start, counter, start_state, [])]
    visited = {start_state}
    
    while pq:
        f, _, state, path_moves = heapq.heappop(pq)
        
        if set(state[1]) == goals:
            return path_moves
            
        nbrs = get_neighbors(state, known_walls, goals)
        for nb_state, d, is_push in nbrs:
            # Chỉ cho phép di chuyển trong các ô trống đã biết (không được đi xuyên qua ô chưa khám phá mà ta chưa chắc chắn)
            # Trong mô hình đơn giản này, ta giả định các ô chưa biết là trống, và nếu đâm vào tường thật thì ta sẽ replan.
            if nb_state not in visited:
                visited.add(nb_state)
                nb_h = manhattan(nb_state, goals)
                nb_f = len(path_moves) + 1 + nb_h
                counter += 1
                heapq.heappush(pq, (nb_f, counter, nb_state, path_moves + [d]))
                
    return None # Không tìm thấy đường đi trên bản đồ hiện tại

def partial_obs_steps(start, goals, walls):
    """
    Hiện thực thuật toán Online Replanning với Quan sát một phần (Partial Observation).
    Bản đồ ban đầu được che phủ bởi sương mù. Agent chỉ nhìn thấy các ô trong bán kính Manhattan <= 2.
    Khi di chuyển, Agent cập nhật bản đồ và lập kế hoạch lại (Replan) bằng A*.
    """
    steps = []
    MAX_STEPS = 1000
    
    # Bản đồ đã biết của Agent
    known_walls = set()
    known_goals = goals # Agent biết vị trí của đích
    
    # Vị trí thực tế của game
    current_state = start
    current_path = [start]
    current_moves = []
    
    # Ở mỗi bước, quét các ô xung quanh người chơi thực tế trong bán kính 2
    explored_global = []
    
    while True:
        pr, pc = current_state[0]
        # Quét xung quanh người chơi
        for r_offset in range(-2, 3):
            for c_offset in range(-2, 3):
                if abs(r_offset) + abs(c_offset) <= 2:
                    scan_r, scan_c = pr + r_offset, pc + c_offset
                    # Nếu có tường thực tế, đưa vào known_walls
                    if (scan_r, scan_c) in walls:
                        known_walls.add((scan_r, scan_c))
                        
        h_curr = manhattan(current_state, goals)
        explored_global.append((current_state, h_curr, current_moves))
        
        # Check Goal thực tế
        if set(current_state[1]) == goals:
            steps.append({
                'type': 'goal',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [], 'added': [], 'frontier': [], 'frontier_count': 0,
                'visited_count': len(explored_global),
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(current_moves), 'limit': None, 'iteration': None,
                'message': '✅ Đạt đến trạng thái Đích!'
            })
            break
            
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [], 'added': [], 'frontier': [], 'frontier_count': 0,
                'visited_count': len(explored_global),
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(current_moves), 'limit': None, 'iteration': None
            })
            break
            
        # Lập kế hoạch dựa trên những gì đã biết
        # Hộp đã biết: là vị trí các hộp thực tế nằm trong tầm nhìn của Agent
        # Trong bản demo này, để Agent không bị lạc, ta giả sử Agent biết vị trí các hộp nhưng chưa biết toàn bộ tường.
        known_boxes = set(current_state[1])
        
        path_moves = run_astar_partial(current_state, goals, known_walls, known_boxes)
        
        if not path_moves:
            # Bị kẹt do bản đồ đã biết không có lối đi
            steps.append({
                'type': 'local_optimum',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [], 'added': [], 'frontier': [], 'frontier_count': 0,
                'visited_count': len(explored_global),
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(current_moves), 'limit': None, 'iteration': None,
                'message': '⛰️ Kẹt do sương mù che phủ, không tìm thấy đường đi!'
            })
            break
            
        # Thực hiện nước đi đầu tiên trong kế hoạch đã tìm được
        next_d = path_moves[0]
        
        # Sinh các nước đi kế tiếp thực tế để thực thi nước đi này
        nbrs = get_neighbors(current_state, walls, goals)
        next_state = None
        for nb_s, d, is_push in nbrs:
            if d == next_d:
                next_state = nb_s
                break
                
        if next_state is None:
            # Nước đi không khả thi thực tế (ví dụ đâm vào tường chưa biết) -> Cập nhật bản đồ và lặp lại
            dr, dc = {"↑": (-1, 0), "↓": (1, 0), "←": (0, -1), "→": (0, 1)}[next_d]
            target_pos = (pr + dr, pc + dc)
            if target_pos in walls:
                known_walls.add(target_pos)
            if target_pos in known_boxes:
                next_box_pos = (pr + 2 * dr, pc + 2 * dc)
                if next_box_pos in walls:
                    known_walls.add(next_box_pos)
            
            steps.append({
                'type': 'skip',
                'state': current_state,
                'cost': h_curr,
                'moves': current_moves,
                'path': current_path,
                'neighbors': [ (n[0], n[1]) for n in nbrs ],
                'added': [],
                'frontier': [{'state': current_state, 'via': next_d, 'cost': h_curr}],
                'frontier_count': 1,
                'visited_count': len(explored_global),
                'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
                'depth': len(current_moves), 'limit': None, 'iteration': None,
                'message': f'🚧 Nước đi {next_d} bị chặn bởi tường ẩn! Phát hiện tường mới và lập kế hoạch lại.'
            })
            continue
            
        steps.append({
            'type': 'expand',
            'state': current_state,
            'cost': h_curr,
            'moves': current_moves,
            'path': current_path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ],
            'added': [(next_state, next_d, manhattan(next_state, goals))],
            'frontier': [{'state': next_state, 'via': next_d, 'cost': manhattan(next_state, goals)}],
            'frontier_count': 1,
            'visited_count': len(explored_global),
            'explored': [(exp[0], exp[1], exp[2][-1] if exp[2] else 'start') for exp in explored_global[-12:]],
            'depth': len(current_moves), 'limit': None, 'iteration': None,
            'message': f'👁️ Đang quan sát bán kính 2. Di chuyển theo hướng {next_d} và cập nhật bản đồ.'
        })
        
        current_state = next_state
        current_moves = current_moves + [next_d]
        current_path = current_path + [next_state]
        
    return steps
