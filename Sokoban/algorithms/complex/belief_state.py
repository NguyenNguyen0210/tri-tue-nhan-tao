from collections import deque
from algorithms.utils import get_neighbors, manhattan

def transition_belief(belief_state, d, walls, goals):
    """
    Chuyển đổi trạng thái niềm tin (Belief State) qua hướng đi d.
    Trả về một frozenset chứa các trạng thái kế tiếp có thể có.
    """
    next_states = []
    for state in belief_state:
        nbrs = get_neighbors(state, walls, goals)
        moved = False
        for nb_s, nb_d, is_push in nbrs:
            if nb_d == d:
                next_states.append(nb_s)
                moved = True
                break
        if not moved:
            # Nếu trong thế giới này, nước đi d bị chặn bởi tường -> người chơi không di chuyển được
            next_states.append(state)
            
    return frozenset(next_states)

def belief_state_steps(start, goals, walls):
    """
    Hiện thực thuật toán Belief State Search cho Sokoban.
    Mô phỏng trường hợp ban đầu ta KHÔNG chắc chắn vị trí của chiếc hộp thứ nhất
    (có 2 vị trí khả nghi). Thuật toán tìm đường đi giải cho CẢ HAI cấu hình này.
    """
    steps = []
    MAX_STEPS = 2000
    
    # Tạo cấu hình giả định thứ 2 để khởi tạo Trạng thái niềm tin (size = 2)
    player, boxes = start
    start_alt = None
    if len(boxes) > 0:
        # Lấy chiếc hộp đầu tiên và thử dịch chuyển nó sang phải hoặc xuống dưới 1 ô để làm cấu hình thay thế
        box = boxes[0]
        br, bc = box
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            alt_box = (br + dr, bc + dc)
            if alt_box not in walls and alt_box not in goals and alt_box not in boxes:
                # Tạo danh sách hộp thay thế
                alt_boxes = list(boxes)
                alt_boxes[0] = alt_box
                alt_boxes.sort()
                start_alt = (player, tuple(alt_boxes))
                break
                
    # Tập hợp niềm tin ban đầu
    if start_alt is not None:
        initial_belief = frozenset([start, start_alt])
    else:
        initial_belief = frozenset([start])
        
    # BFS trên không gian trạng thái niềm tin (Belief States Space)
    # Hàng đợi chứa: (belief_state, moves, path_of_beliefs)
    frontier_q = deque([(initial_belief, [], [initial_belief])])
    visited = {initial_belief}
    
    explored = []
    
    while frontier_q:
        belief, moves, path = frontier_q.popleft()
        
        # Chọn đại diện 1 trạng thái để hiển thị lên GUI vẽ bàn cờ
        repr_state = list(belief)[0]
        h_repr = manhattan(repr_state, goals)
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
                'moves': moves,
                'path': [list(b)[0] for b in path],
                'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(frontier_q),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': len(belief), 'iteration': None
            })
            break
            
        # Goal check: Tất cả các thế giới trong Belief State đều phải hoàn thành
        is_goal = all(set(s[1]) == goals for s in belief)
        
        if is_goal:
            steps.append({
                'type': 'goal',
                'state': repr_state,
                'moves': moves,
                'path': [list(b)[0] for b in path],
                'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(frontier_q),
                'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': len(belief), 'iteration': None,
                'message': f'✅ Trạng thái niềm tin đạt GOAL! Số lượng thế giới được giải cùng lúc: {len(belief)}'
            })
            break
            
        # Thử 4 hướng di chuyển cho toàn bộ Belief State
        added = []
        for d in ['↑', '↓', '←', '→']:
            next_belief = transition_belief(belief, d, walls, goals)
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
            'moves': moves,
            'path': [list(b)[0] for b in path],
            'neighbors': [], 'added': added, 'frontier': frontier_render, 'frontier_count': len(frontier_q),
            'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': len(belief), 'iteration': None,
            'message': f'🔮 Đang giải song song {len(belief)} thế giới khác nhau. Đang mở rộng biên tìm kiếm niềm tin.'
        })
        
    return steps
