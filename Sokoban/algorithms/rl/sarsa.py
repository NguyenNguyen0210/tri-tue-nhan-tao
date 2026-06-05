import random
from algorithms.utils import get_neighbors, manhattan

def get_best_action_sarsa(q_table, state, valid_actions):
    """
    Lấy hành động tốt nhất từ Q-table cho trạng thái s.
    Nếu chưa có trong Q-table, chọn ngẫu nhiên.
    """
    best_val = -float('inf')
    best_actions = []
    
    for a in valid_actions:
        val = q_table.get((state, a), 0.0)
        if val > best_val:
            best_val = val
            best_actions = [a]
        elif val == best_val:
            best_actions.append(a)
            
    return random.choice(best_actions)

def choose_action_epsilon_greedy(q_table, state, valid_actions, epsilon):
    """
    Chọn hành động theo chiến lược Epsilon-Greedy.
    """
    if random.random() < epsilon:
        return random.choice(valid_actions)
    else:
        return get_best_action_sarsa(q_table, state, valid_actions)

def sarsa_steps(start, goals, walls):
    """
    Hiện thực thuật toán SARSA cho Sokoban.
    Huấn luyện AI tự học thông qua chính sách On-policy (SARSA), 
    sau đó chạy kiểm thử và xuất danh sách các bước chạy cho GUI.
    """
    # Các tham số RL
    alpha = 0.2  # Tốc độ học (learning rate)
    gamma = 0.9  # Hệ số chiết khấu (discount factor)
    epsilon = 0.2  # Tỷ lệ khám phá (exploration rate)
    episodes = 200 # Số tập huấn luyện
    max_steps_per_episode = 100
    
    q_table = {}
    best_path = []
    best_moves = []
    
    # ── VÒNG LẶP HUẤN LUYỆN (TRAINING LOOP) ──
    for ep in range(episodes):
        state = start
        path = [start]
        moves = []
        
        nbrs = get_neighbors(state, walls, goals)
        if not nbrs:
            continue
            
        valid_actions = [n[1] for n in nbrs]
        action_map = {n[1]: n[0] for n in nbrs}
        
        # Chọn hành động ban đầu a
        action = choose_action_epsilon_greedy(q_table, state, valid_actions, epsilon)
        
        for step in range(max_steps_per_episode):
            # Kiểm tra trạng thái hiện tại đạt đích chưa
            if set(state[1]) == goals:
                if not best_moves or len(moves) < len(best_moves):
                    best_path = list(path)
                    best_moves = list(moves)
                break
                
            next_state = action_map[action]
            
            # Tính phần thưởng (Reward)
            reward = -1 # Phạt nhẹ mỗi bước đi
            
            # Kiểm tra xem có đẩy thùng vào đích không
            old_boxes = set(state[1])
            new_boxes = set(next_state[1])
            moved_box = list(new_boxes - old_boxes)
            if moved_box:
                box_pos = moved_box[0]
                if box_pos in goals:
                    reward += 30
                else:
                    reward += 5
                    
            if set(next_state[1]) == goals:
                reward += 100
                
            # Chọn hành động tiếp theo a' từ s' (On-policy)
            next_nbrs = get_neighbors(next_state, walls, goals)
            next_actions = [n[1] for n in next_nbrs] if next_nbrs else []
            next_action_map = {n[1]: n[0] for n in next_nbrs} if next_nbrs else {}
            
            next_action = None
            next_q = 0.0
            
            if next_actions:
                next_action = choose_action_epsilon_greedy(q_table, next_state, next_actions, epsilon)
                next_q = q_table.get((next_state, next_action), 0.0)
                
            # Cập nhật Q-Table bằng công thức SARSA (dựa trên next_q của hành động tiếp theo thực sự được chọn)
            old_q = q_table.get((state, action), 0.0)
            q_table[(state, action)] = old_q + alpha * (reward + gamma * next_q - old_q)
            
            # Di chuyển sang trạng thái tiếp theo
            state = next_state
            path.append(state)
            moves.append(action)
            
            # Cập nhật hành động hiện tại cho bước kế
            action = next_action
            action_map = next_action_map
            if not action:
                break
                
    # ── VÒNG LẶP CHẠY THỬ NGHIỆM (TEST LOOP GREEDY) ──
    steps = []
    state = start
    path = [start]
    moves = []
    explored = []
    
    MAX_STEPS = 3000
    step_count = 0
    
    while step_count < 100:
        h_curr = manhattan(state, goals)
        explored.append((state, h_curr, moves))
        
        frontier_render = []
        nbrs = get_neighbors(state, walls, goals)
        for nb_s, d, is_push in nbrs:
            q_val = q_table.get((state, d), 0.0)
            frontier_render.append({
                'state': nb_s[0], 'cost': q_val, 'via': d
            })
        frontier_render.sort(key=lambda x: x['cost'], reverse=True)
        
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored[-12:]
        ]
        
        # Check Goal
        if set(state[1]) == goals:
            steps.append({
                'type': 'goal', 'state': state, 'cost': h_curr, 'moves': moves, 'path': path,
                'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(nbrs),
                'visited_count': len(explored), 'explored': explored_render,
                'depth': len(moves), 'limit': episodes, 'iteration': None,
                'message': f'✅ Đạt GOAL sau khi huấn luyện! Tổng số trạng thái Q-table: {len(q_table)}'
            })
            break
            
        if not nbrs:
            steps.append({
                'type': 'local_optimum', 'state': state, 'cost': h_curr, 'moves': moves, 'path': path,
                'neighbors': [], 'added': [], 'frontier': [], 'frontier_count': 0,
                'visited_count': len(explored), 'explored': explored_render,
                'depth': len(moves), 'limit': episodes, 'iteration': None,
                'message': '⛰️ Kẹt do AI không biết đi tiếp đi đâu (Q-table trống)'
            })
            break
            
        valid_actions = [n[1] for n in nbrs]
        action_map = {n[1]: n[0] for n in nbrs}
        
        # Chọn hành động tốt nhất tuyệt đối theo Q-Table
        action = get_best_action_sarsa(q_table, state, valid_actions)
        next_state = action_map[action]
        
        steps.append({
            'type': 'expand', 'state': state, 'cost': h_curr, 'moves': moves, 'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ],
            'added': [(next_state, action, q_table.get((state, action), 0.0))],
            'frontier': frontier_render, 'frontier_count': len(nbrs),
            'visited_count': len(explored), 'explored': explored_render,
            'depth': len(moves), 'limit': episodes, 'iteration': None,
            'message': f'🤖 SARSA Action: Chọn {action} (Q={q_table.get((state, action), 0.0):.2f})'
        })
        
        state = next_state
        path.append(state)
        moves.append(action)
        step_count += 1
        
    # Thay thế bằng best_path tìm được trong lúc train nếu test bị kẹt
    if steps and steps[-1]['type'] != 'goal' and best_path:
        steps = []
        path_states = best_path
        path_moves = best_moves
        
        for idx in range(len(path_states)):
            curr_s = path_states[idx]
            curr_moves = path_moves[:idx]
            curr_path = path_states[:idx+1]
            
            is_last = (idx == len(path_states) - 1)
            steps.append({
                'type': 'goal' if is_last else 'expand',
                'state': curr_s,
                'cost': manhattan(curr_s, goals),
                'moves': curr_moves,
                'path': curr_path,
                'neighbors': [], 'added': [], 'frontier': [], 'frontier_count': 0,
                'visited_count': idx + 1,
                'explored': [(s, manhattan(s, goals), 'move') for s in curr_path[-12:]],
                'depth': idx, 'limit': episodes, 'iteration': None,
                'message': f'🤖 SARSA: Chạy nước đi tốt nhất học được trong lúc huấn luyện (Bước {idx})'
            })
            
    return steps
