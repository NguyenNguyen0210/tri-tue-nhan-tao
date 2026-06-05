import random
from algorithms.utils import get_neighbors, manhattan, is_deadlock

def get_best_action_q(q_table, state, valid_actions):
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

def q_learning_steps(start, goals, walls):
    """
    Hiện thực thuật toán Q-Learning cho Sokoban.
    Huấn luyện AI tự học cách đẩy thùng qua các episodes, sau đó chạy thử nghiệm (greedy)
    và trả về danh sách các bước chạy để phục vụ giao diện trực quan hóa.
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
    
    # Hướng đi tương ứng với ký hiệu hành động
    dir_symbols = ['↑', '↓', '←', '→']
    
    # ── VÒNG LẶP HUẤN LUYỆN (TRAINING LOOP) ──
    for ep in range(episodes):
        state = start
        path = [start]
        moves = []
        
        for step in range(max_steps_per_episode):
            # Kiểm tra trạng thái hiện tại đạt đích chưa
            if set(state[1]) == goals:
                if not best_moves or len(moves) < len(best_moves):
                    best_path = list(path)
                    best_moves = list(moves)
                break
                
            nbrs = get_neighbors(state, walls, goals)
            if not nbrs:
                break
                
            valid_actions = [n[1] for n in nbrs]
            action_map = {n[1]: n[0] for n in nbrs} # Hướng -> Trạng thái kế
            
            # Chọn hành động bằng Epsilon-Greedy
            if random.random() < epsilon:
                action = random.choice(valid_actions)
            else:
                action = get_best_action_q(q_table, state, valid_actions)
                
            next_state = action_map[action]
            
            # Tính phần thưởng (Reward)
            reward = -1 # Phạt nhẹ mỗi bước đi để tìm đường ngắn nhất
            
            # Kiểm tra xem có đẩy thùng vào đích không
            old_boxes = set(state[1])
            new_boxes = set(next_state[1])
            moved_box = list(new_boxes - old_boxes)
            if moved_box:
                box_pos = moved_box[0]
                if box_pos in goals:
                    reward += 30 # Thưởng lớn nếu đẩy được thùng vào đích
                else:
                    reward += 5 # Thưởng nhỏ nếu di chuyển thùng sang vị trí thường
                    
            if set(next_state[1]) == goals:
                reward += 100 # Thưởng cực lớn khi hoàn thành màn chơi
                
            # Cập nhật Q-Table bằng công thức Q-Learning
            next_nbrs = get_neighbors(next_state, walls, goals)
            next_actions = [n[1] for n in next_nbrs] if next_nbrs else []
            
            max_next_q = 0.0
            if next_actions:
                max_next_q = max(q_table.get((next_state, na), 0.0) for na in next_actions)
                
            old_q = q_table.get((state, action), 0.0)
            q_table[(state, action)] = old_q + alpha * (reward + gamma * max_next_q - old_q)
            
            state = next_state
            path.append(state)
            moves.append(action)
            
    # ── VÒNG LẶP CHẠY THỬ NGHIỆM (TEST LOOP GREEDY) ──
    # Sau khi huấn luyện, ta dùng Q-table tốt nhất để xuất danh sách các bước chạy cho GUI.
    steps = []
    state = start
    path = [start]
    moves = []
    explored = []
    
    MAX_STEPS = 3000
    step_count = 0
    
    # Nếu trong huấn luyện không tìm thấy đường đi, ta trả về danh sách trống hoặc chạy đến khi kẹt
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
        frontier_render.sort(key=lambda x: x['cost'], reverse=True) # Hiện giá trị Q lớn nhất lên trước
        
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
        
        # Chọn hành động tốt nhất tuyệt đối theo Q-Table học được
        action = get_best_action_q(q_table, state, valid_actions)
        next_state = action_map[action]
        
        steps.append({
            'type': 'expand', 'state': state, 'cost': h_curr, 'moves': moves, 'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ],
            'added': [(next_state, action, q_table.get((state, action), 0.0))],
            'frontier': frontier_render, 'frontier_count': len(nbrs),
            'visited_count': len(explored), 'explored': explored_render,
            'depth': len(moves), 'limit': episodes, 'iteration': None,
            'message': f'🤖 Q-Learning Action: Chọn {action} (Q={q_table.get((state, action), 0.0):.2f})'
        })
        
        state = next_state
        path.append(state)
        moves.append(action)
        step_count += 1
        
    # Trường hợp kẹt/không tìm được đường đi, thay thế bằng best_path tìm được trong lúc train để tránh lỗi giao diện trống
    if steps and steps[-1]['type'] != 'goal' and best_path:
        # Tái cấu trúc các bước đi dựa trên best_path của lúc train
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
                'message': f'🤖 Q-Learning: Chạy nước đi tốt nhất học được trong lúc huấn luyện (Bước {idx})'
            })
            
    return steps
