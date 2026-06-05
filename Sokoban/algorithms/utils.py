def parse_level(grid):
    """
    Phân tích màn chơi từ mảng các chuỗi ký tự.
    Trả về:
      walls: set of (row, col)
      goals: set of (row, col)
      player_pos: (row, col)
      boxes: tuple of (row, col) (đã được sắp xếp)
    """
    walls = set()
    goals = set()
    boxes = []
    player_pos = None

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == '#':
                walls.add((r, c))
            elif char == '.':
                goals.add((r, c))
            elif char == '$':
                boxes.append((r, c))
            elif char == '@':
                player_pos = (r, c)
            elif char == '*':
                goals.add((r, c))
                boxes.append((r, c))
            elif char == '+':
                goals.add((r, c))
                player_pos = (r, c)
                
    return walls, goals, player_pos, tuple(sorted(boxes))

def is_deadlock(box, walls, goals):
    """
    Kiểm tra xem một chiếc thùng ở tọa độ `box` có bị kẹt chết (deadlock) hay không.
    Kẹt góc: Một chiếc thùng không nằm ở ô đích, và có tường bao bọc ở 2 hướng vuông góc.
    """
    if box in goals:
        return False
        
    r, c = box
    # Kiểm tra các hướng xung quanh xem có tường không
    up = (r - 1, c) in walls
    down = (r + 1, c) in walls
    left = (r, c - 1) in walls
    right = (r, c + 1) in walls
    
    # Kẹt góc:
    # 1. Trên và Trái
    if up and left:
        return True
    # 2. Trên và Phải
    if up and right:
        return True
    # 3. Dưới và Trái
    if down and left:
        return True
    # 4. Dưới và Phải
    if down and right:
        return True
        
    return False

def get_neighbors(state, walls, goals):
    """
    Sinh các trạng thái kế tiếp từ trạng thái hiện tại.
    Mỗi phần tử trả về: (new_state, direction_symbol, is_push)
    new_state: ((player_r, player_c), (box1, box2, ...))
    """
    player_pos, boxes = state
    pr, pc = player_pos
    boxes_set = set(boxes)
    neighbors = []
    
    # Hướng đi: (d_row, d_col, ký hiệu)
    dirs = [
        (-1, 0, '↑'),
        (1, 0, '↓'),
        (0, -1, '←'),
        (0, 1, '→')
    ]
    
    for dr, dc, sym in dirs:
        nr, nc = pr + dr, pc + dc
        new_player = (nr, nc)
        
        # 1. Đi vào tường -> không hợp lệ
        if new_player in walls:
            continue
            
        # 2. Đi vào ô có thùng -> người chơi đẩy thùng
        if new_player in boxes_set:
            # Vị trí mới của thùng sau khi đẩy
            br, bc = nr + dr, nc + dc
            new_box = (br, bc)
            
            # Nếu vị trí mới của thùng là tường hoặc có thùng khác đè lên -> không đẩy được
            if new_box in walls or new_box in boxes_set:
                continue
                
            # Kiểm tra xem đẩy vào vị trí này có tạo ra deadlock không
            if is_deadlock(new_box, walls, goals):
                continue
                
            # Tạo danh sách thùng mới, sắp xếp lại để trạng thái là duy nhất
            new_boxes = list(boxes)
            new_boxes.remove(new_player)
            new_boxes.append(new_box)
            new_boxes.sort()
            
            new_state = (new_player, tuple(new_boxes))
            neighbors.append((new_state, sym, True)) # True nghĩa là có đẩy thùng
            
        # 3. Đi vào sàn trống
        else:
            new_state = (new_player, boxes)
            neighbors.append((new_state, sym, False)) # False nghĩa là chỉ di chuyển thường
            
    return neighbors

def manhattan(state, goals):
    """
    Hàm Heuristic Manhattan cho Sokoban.
    Tính tổng khoảng cách Manhattan từ mỗi thùng đến ô đích gần nhất của nó.
    """
    _, boxes = state
    total_dist = 0
    for box in boxes:
        # Tìm khoảng cách ngắn nhất từ chiếc thùng này đến bất kỳ ô đích nào
        min_dist = float('inf')
        for goal in goals:
            dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
            if dist < min_dist:
                min_dist = dist
        total_dist += min_dist if min_dist != float('inf') else 0
    return total_dist
