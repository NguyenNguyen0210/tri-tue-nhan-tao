from collections import deque
from algorithms.utils import get_neighbors

def can_reach_any_goal(box, goals, walls):
    """
    Hàm kiểm tra xem một thùng từ vị trí `box` có thể di chuyển (theo luật đẩy cơ bản)
    đến bất kỳ điểm đích nào không (bỏ qua vị trí người chơi và các thùng khác).
    Đây là kiểm tra khả năng gán giá trị (domain) cho biến trong CSP.
    """
    if box in goals:
        return True
        
    # BFS đơn giản từ vị trí của thùng
    q = deque([box])
    visited = {box}
    
    while q:
        r, c = q.popleft()
        if (r, c) in goals:
            return True
            
        # Các nước đi có thể của thùng (nếu có lực đẩy từ hướng đối diện)
        # Để đơn giản, ta chỉ cần check xem thùng có thể di chuyển đi đâu mà không đâm vào tường
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in walls and (nr, nc) not in visited:
                # Kiểm tra hướng đẩy tương ứng có phải là tường không
                # e.g., để đi đến (nr, nc), người chơi phải đứng ở (r - dr, c - dc)
                opposite = (r - dr, c - dc)
                if opposite not in walls:
                    visited.add((nr, nc))
                    q.append((nr, nc))
                    
    return False

def forward_checking_steps(start, goals, walls):
    """
    Hiện thực thuật toán Backtracking với Forward Checking cho Sokoban.
    Tại mỗi bước, kiểm tra trước xem có thùng nào có domain rỗng (không thể chạm tới bất kỳ đích nào) hay không.
    Nếu có, lập tức cắt tỉa (prune) nhánh đó.
    """
    steps = []
    MAX_STEPS = 3000
    
    # LIFO stack: (state, path, moves)
    stack = [(start, [start], [])]
    visited = set()
    explored = []
    
    while stack:
        state, path, moves = stack.pop()
        
        frontier_render = [
            {'state': f_node[0], 'via': f_node[2][-1] if f_node[2] else 'start', 'depth': len(f_node[2])}
            for f_node in list(reversed(stack[-12:]))
        ]
        explored_render = [
            (exp_node[0], exp_node[1], exp_node[2][-1] if exp_node[2] else 'start')
            for exp_node in explored[-12:]
        ]
        
        if state in visited:
            if len(steps) >= MAX_STEPS:
                steps.append({
                    'type': 'limit_reached', 'state': state, 'moves': moves, 'path': path,
                    'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(stack),
                    'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                    'limit': None, 'iteration': None
                })
                break
            steps.append({
                'type': 'skip', 'state': state, 'moves': moves, 'path': path,
                'frontier': frontier_render, 'frontier_count': len(stack),
                'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                'limit': None, 'iteration': None
            })
            continue
            
        # ── FORWARD CHECKING ──
        # Kiểm tra xem có bất kỳ thùng nào có domain rỗng không (không thể đạt bất kỳ goal nào)
        has_empty_domain = False
        for box in state[1]:
            if not can_reach_any_goal(box, goals, walls):
                has_empty_domain = True
                break
                
        if has_empty_domain:
            # Lập tức cắt tỉa nhánh này (pruning)
            steps.append({
                'type': 'skip', # Ghi nhận là skip do bị cắt tỉa bởi Forward Checking
                'state': state, 'moves': moves, 'path': path,
                'frontier': frontier_render, 'frontier_count': len(stack),
                'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                'limit': None, 'iteration': None,
                'message': '✂️ Forward Checking: Cắt tỉa nhánh do phát hiện thùng không thể về đích!'
            })
            continue
            
        visited.add(state)
        explored.append((state, len(moves), moves))
        
        # Goal check
        if set(state[1]) == goals:
            steps.append({
                'type': 'goal', 'state': state, 'moves': moves, 'path': path,
                'neighbors': [], 'added': [], 'frontier': frontier_render, 'frontier_count': len(stack),
                'visited_count': len(visited), 'explored': explored_render, 'depth': len(moves),
                'limit': None, 'iteration': None
            })
            break
            
        nbrs = get_neighbors(state, walls, goals)
        added = []
        for nb_state, d, is_push in nbrs:
            if nb_state not in visited:
                stack.append((nb_state, path + [nb_state], moves + [d]))
                added.append((nb_state, d, len(moves) + 1))
                
        if len(steps) >= MAX_STEPS:
            steps.append({
                'type': 'limit_reached', 'state': state, 'moves': moves, 'path': path,
                'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added, 'frontier': frontier_render,
                'frontier_count': len(stack), 'visited_count': len(visited), 'explored': explored_render,
                'depth': len(moves), 'limit': None, 'iteration': None
            })
            break
            
        steps.append({
            'type': 'expand', 'state': state, 'moves': moves, 'path': path,
            'neighbors': [ (n[0], n[1]) for n in nbrs ], 'added': added, 'frontier': frontier_render,
            'frontier_count': len(stack), 'visited_count': len(visited), 'explored': explored_render,
            'depth': len(moves), 'limit': None, 'iteration': None
        })
        
    return steps
