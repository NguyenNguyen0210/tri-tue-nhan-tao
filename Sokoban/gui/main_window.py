import time
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QListWidget, QListWidgetItem, QScrollArea, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush

from config import (
    BG, BG2, BG3, BORDER, ACCENT, ACCENT2, TEXT, TEXT_DIM,
    COLOR_WALL, COLOR_FLOOR, COLOR_TARGET, COLOR_BOX, COLOR_BOX_OK, COLOR_PLAYER, LEVELS
)
from algorithms import (
    bfs_steps, dfs_steps, greedy_steps, astar_steps,
    hillclimbing_steps, steepest_hillclimbing_steps,
    backtracking_steps, forward_checking_steps,
    belief_state_steps, partial_obs_steps,
    q_learning_steps, sarsa_steps, parse_level
)

class SokobanBoard(QWidget):
    """
    Widget chính dùng để vẽ bàn cờ Sokoban động bằng QPainter.
    Có chế độ sương mù (Fog of War) cho thuật toán quan sát một phần.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = []
        self.walls = set()
        self.goals = set()
        self.player_pos = (0, 0)
        self.boxes = set()
        
        self.tile_size = 50
        self.partial_obs_mode = False
        
    def set_map(self, walls, goals, state, partial_obs_mode=False):
        self.walls = walls
        self.goals = goals
        self.player_pos, self.boxes = state[0], set(state[1])
        self.partial_obs_mode = partial_obs_mode
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Nếu chưa có bản đồ, thoát
        if not self.walls and not self.goals:
            return
            
        # Tìm kích thước bao quanh bản đồ để vẽ căn giữa
        all_coords = self.walls | self.goals | self.boxes | {self.player_pos}
        max_r = max(c[0] for c in all_coords) + 1
        max_c = max(c[1] for c in all_coords) + 1
        
        # Căn lề giữa widget
        offset_x = max(0, (self.width() - max_c * self.tile_size) // 2)
        offset_y = max(0, (self.height() - max_r * self.tile_size) // 2)
        
        # Tầm nhìn cho Partial Observation (khoảng cách Manhattan <= 2)
        pr, pc = self.player_pos
        
        for r in range(max_r):
            for c in range(max_c):
                x = offset_x + c * self.tile_size
                y = offset_y + r * self.tile_size
                
                # Check chế độ sương mù
                in_sight = True
                if self.partial_obs_mode:
                    if abs(r - pr) + abs(c - pc) > 2:
                        in_sight = False
                        
                # 1. Vẽ ô sương mù (Chưa khám phá)
                if not in_sight:
                    painter.fillRect(x, y, self.tile_size, self.tile_size, QColor("#05070A"))
                    # Vẽ lưới mờ cho sương mù
                    painter.setPen(QPen(QColor("#0E1118"), 1))
                    painter.drawRect(x, y, self.tile_size, self.tile_size)
                    continue
                    
                # 2. Vẽ ô trống / sàn
                painter.fillRect(x, y, self.tile_size, self.tile_size, QColor(COLOR_FLOOR))
                painter.setPen(QPen(QColor(BORDER), 1))
                painter.drawRect(x, y, self.tile_size, self.tile_size)
                
                # 3. Vẽ tường
                if (r, c) in self.walls:
                    painter.fillRect(x + 2, y + 2, self.tile_size - 4, self.tile_size - 4, QColor(COLOR_WALL))
                    painter.setPen(QPen(QColor("#64748B"), 1))
                    painter.drawRect(x + 2, y + 2, self.tile_size - 4, self.tile_size - 4)
                    
                # 4. Vẽ điểm đích (Goal)
                if (r, c) in self.goals:
                    painter.setBrush(QBrush(QColor(COLOR_TARGET)))
                    painter.setPen(Qt.NoPen)
                    # Vẽ chấm tròn đích ở giữa ô
                    r_dot = self.tile_size // 4
                    painter.drawEllipse(x + (self.tile_size - r_dot) // 2, y + (self.tile_size - r_dot) // 2, r_dot, r_dot)
                    
                # 5. Vẽ thùng (Box)
                if (r, c) in self.boxes:
                    on_goal = (r, c) in self.goals
                    color = COLOR_BOX_OK if on_goal else COLOR_BOX
                    border_color = "#34D399" if on_goal else "#F59E0B"
                    
                    # Vẽ hộp bo góc nhẹ
                    painter.setBrush(QBrush(QColor(color)))
                    painter.setPen(QPen(QColor(border_color), 2))
                    painter.drawRoundedRect(x + 4, y + 4, self.tile_size - 8, self.tile_size - 8, 6.0, 6.0)
                    
                    # Vẽ hình chéo "X" trên hộp cho thêm phong cách
                    painter.setPen(QPen(QColor(border_color), 1))
                    painter.drawLine(x + 8, y + 8, x + self.tile_size - 8, y + self.tile_size - 8)
                    painter.drawLine(x + self.tile_size - 8, y + 8, x + 8, y + self.tile_size - 8)
                    
                # 6. Vẽ người chơi (Player)
                if (r, c) == self.player_pos:
                    painter.setBrush(QBrush(QColor(COLOR_PLAYER)))
                    painter.setPen(QPen(QColor("#FFFFFF"), 2))
                    # Vẽ hình tròn biểu diễn người chơi
                    r_player = self.tile_size * 2 // 3
                    painter.drawEllipse(x + (self.tile_size - r_player) // 2, y + (self.tile_size - r_player) // 2, r_player, r_player)
                    
                    # Vẽ mắt người chơi cho dễ thương
                    painter.setBrush(QBrush(QColor("#000000")))
                    painter.setPen(Qt.NoPen)
                    eye_size = self.tile_size // 8
                    painter.drawEllipse(x + self.tile_size // 3 - eye_size // 2, y + self.tile_size // 3, eye_size, eye_size)
                    painter.drawEllipse(x + self.tile_size * 2 // 3 - eye_size // 2, y + self.tile_size // 3, eye_size, eye_size)


class MiniSokobanBoard(QWidget):
    """
    Widget vẽ bản đồ nhỏ hiển thị trạng thái trong danh sách Frontier và Explored.
    """
    def __init__(self, walls, goals, state, parent=None):
        super().__init__(parent)
        self.walls = walls
        self.goals = goals
        self.player_pos, self.boxes = state[0], set(state[1])
        
        self.tile_size = 10
        self.setFixedSize(100, 100)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        all_coords = self.walls | self.goals | self.boxes | {self.player_pos}
        max_r = max(c[0] for c in all_coords) + 1
        max_c = max(c[1] for c in all_coords) + 1
        
        offset_x = max(0, (self.width() - max_c * self.tile_size) // 2)
        offset_y = max(0, (self.height() - max_r * self.tile_size) // 2)
        
        # Vẽ nền mini
        painter.fillRect(self.rect(), QColor(BG2))
        
        for r in range(max_r):
            for c in range(max_c):
                x = offset_x + c * self.tile_size
                y = offset_y + r * self.tile_size
                
                painter.fillRect(x, y, self.tile_size, self.tile_size, QColor(COLOR_FLOOR))
                
                if (r, c) in self.walls:
                    painter.fillRect(x, y, self.tile_size, self.tile_size, QColor(COLOR_WALL))
                if (r, c) in self.goals:
                    painter.setBrush(QBrush(QColor(COLOR_TARGET)))
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(x + self.tile_size // 3, y + self.tile_size // 3, self.tile_size // 3, self.tile_size // 3)
                if (r, c) in self.boxes:
                    on_goal = (r, c) in self.goals
                    color = COLOR_BOX_OK if on_goal else COLOR_BOX
                    painter.fillRect(x + 1, y + 1, self.tile_size - 2, self.tile_size - 2, QColor(color))
                if (r, c) == self.player_pos:
                    painter.setBrush(QBrush(QColor(COLOR_PLAYER)))
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(x + 1, y + 1, self.tile_size - 2, self.tile_size - 2)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sokoban AI Solver & Visualizer")
        self.setMinimumSize(1550, 820)
        
        self.steps = []
        self.current_step = -1
        
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.next_step)
        
        # Load màn chơi mặc định
        self.current_level_idx = 0
        self._load_level(self.current_level_idx)
        
        self._build_ui()
        self._apply_style()
        self.run_algorithm()
        
    def _load_level(self, idx):
        grid = LEVELS[idx]
        self.walls, self.goals, self.initial_player, self.initial_boxes = parse_level(grid)
        self.initial_state = (self.initial_player, self.initial_boxes)
        
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # ── CỘT TRÁI: Nhật ký & Thông tin trạng thái ──────────────────────
        left_col = QVBoxLayout()
        left_col.setSpacing(10)
        
        log_group = QGroupBox("Lịch sử giải thuật (History Logs)")
        log_layout = QVBoxLayout(log_group)
        self.log_list = QListWidget()
        self.log_list.itemClicked.connect(self._on_log_clicked)
        log_layout.addWidget(self.log_list)
        
        left_col.addWidget(log_group, 3)
        
        # ── CỘT GIỮA: Màn hình vẽ chính & Control panel ───────────────────
        mid_col = QVBoxLayout()
        mid_col.setSpacing(12)
        
        # Màn hình vẽ game
        self.board = SokobanBoard()
        mid_col.addWidget(self.board, 5)
        
        # Thanh điều khiển
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(10)
        
        # Lựa chọn màn chơi
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Level 1: Rất dễ (1 Hộp)", "Level 2: Dễ (2 Hộp)", "Level 3: Trung bình (3 Hộp)"])
        self.level_combo.currentIndexChanged.connect(self.change_level)
        
        # Lựa chọn thuật toán (12 thuật toán)
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            "BFS (Breadth-First Search)  —  Uninformed",
            "DFS (Depth-First Search)  —  Uninformed",
            "Greedy Best-First Search  —  Informed",
            "A* Search  —  Informed",
            "Simple Hill Climbing  —  Local Search",
            "Steepest-Ascent Hill Climbing  —  Local Search",
            "Backtracking Search  —  CSP Group",
            "Forward Checking  —  CSP Group",
            "Belief State Search  —  Complex Search",
            "Search with Partial Observation  —  Complex",
            "Q-Learning  —  Reinforcement Learning",
            "SARSA  —  Reinforcement Learning"
        ])
        self.algo_combo.currentIndexChanged.connect(self._on_algo_change)
        
        self.btn_solve = QPushButton("🔍 Solve (AI)")
        self.btn_solve.clicked.connect(self.run_algorithm)
        
        self.btn_prev = QPushButton("◀ Prev")
        self.btn_prev.setObjectName("btn_prev")
        self.btn_prev.clicked.connect(self.prev_step)
        
        self.btn_next = QPushButton("Next ▶")
        self.btn_next.setObjectName("btn_next")
        self.btn_next.clicked.connect(self.next_step)
        
        self.btn_auto = QPushButton("▶ Auto")
        self.btn_auto.setObjectName("btn_auto")
        self.btn_auto.clicked.connect(self.toggle_auto)
        
        self.btn_reset = QPushButton("🔄 Reset")
        self.btn_reset.setObjectName("btn_reset")
        self.btn_reset.clicked.connect(self.reset_game)
        
        control_layout.addWidget(QLabel("Màn chơi:"))
        control_layout.addWidget(self.level_combo)
        control_layout.addWidget(QLabel("Thuật toán:"))
        control_layout.addWidget(self.algo_combo)
        control_layout.addWidget(self.btn_solve)
        control_layout.addWidget(self.btn_prev)
        control_layout.addWidget(self.btn_next)
        control_layout.addWidget(self.btn_auto)
        control_layout.addWidget(self.btn_reset)
        
        mid_col.addWidget(control_panel, 0)
        
        # ── CỘT PHẢI: Bảng chỉ số (Metrics) & Frontier/Explored ────────────
        right_col = QVBoxLayout()
        right_col.setSpacing(10)
        
        # Cards chỉ số
        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(8)
        
        self.card_status = self._create_card("STATUS", "Idle", ACCENT)
        self.card_time = self._create_card("EXEC TIME (ms)", "0.0", ACCENT2)
        self.card_frontier = self._create_card("FRONTIER SIZE", "0", ACCENT)
        self.card_visited = self._create_card("VISITED NODES", "0", ACCENT2)
        self.card_depth = self._create_card("PATH DEPTH", "0", ACCENT)
        
        metrics_layout.addWidget(self.card_status, 0, 0)
        metrics_layout.addWidget(self.card_time, 0, 1)
        metrics_layout.addWidget(self.card_frontier, 1, 0)
        metrics_layout.addWidget(self.card_visited, 1, 1)
        metrics_layout.addWidget(self.card_depth, 2, 0, 1, 2)
        
        right_col.addLayout(metrics_layout, 1)
        
        # Frontier list panel
        front_group = QGroupBox("Biên tìm kiếm (Frontier list)")
        front_layout = QVBoxLayout(front_group)
        self.front_scroll = QScrollArea()
        self.front_scroll.setWidgetResizable(True)
        self.front_scroll_content = QWidget()
        self.front_scroll_layout = QHBoxLayout(self.front_scroll_content)
        self.front_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.front_scroll_layout.setSpacing(8)
        self.front_scroll.setWidget(self.front_scroll_content)
        front_layout.addWidget(self.front_scroll)
        
        # Explored list panel
        exp_group = QGroupBox("Danh sách đã duyệt (Explored list)")
        exp_layout = QVBoxLayout(exp_group)
        self.exp_scroll = QScrollArea()
        self.exp_scroll.setWidgetResizable(True)
        self.exp_scroll_content = QWidget()
        self.exp_scroll_layout = QHBoxLayout(self.exp_scroll_content)
        self.exp_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.exp_scroll_layout.setSpacing(8)
        self.exp_scroll.setWidget(self.exp_scroll_content)
        exp_layout.addWidget(self.exp_scroll)
        
        right_col.addWidget(front_group, 2)
        right_col.addWidget(exp_group, 2)
        
        # Đưa các cột vào layout chính
        main_layout.addLayout(left_col, 1)
        main_layout.addLayout(mid_col, 3)
        main_layout.addLayout(right_col, 1)
        
    def _create_card(self, title, val, color):
        w = QWidget()
        w.setStyleSheet(f"QWidget{{background:{BG2}; border:1.5px solid {BORDER}; border-radius:10px;}}")
        vl = QVBoxLayout(w)
        vl.setContentsMargins(8, 8, 8, 8)
        vl.setSpacing(2)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"color:{TEXT_DIM}; font-size:10px; font-weight:bold; letter-spacing:1px; border:none;")
        t_lbl.setAlignment(Qt.AlignLeft)
        
        v_lbl = QLabel(val)
        v_lbl.setStyleSheet(f"color:{color}; font-size:16px; font-weight:bold; border:none;")
        v_lbl.setAlignment(Qt.AlignLeft)
        
        vl.addWidget(t_lbl)
        vl.addWidget(v_lbl)
        w.v_lbl = v_lbl # Lưu tham chiếu để cập nhật
        return w
        
    def _apply_style(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {BG};
                color: {TEXT};
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }}
            QLabel {{
                color: {TEXT};
                border: none;
                background: transparent;
            }}
            QGroupBox {{
                border: 1.5px solid {BORDER};
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: 600;
                font-size: 13px;
                color: {TEXT_DIM};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }}
            QListWidget {{
                background-color: {BG2};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 5px;
                color: {TEXT};
            }}
            QListWidget::item {{
                background-color: {BG3};
                border: 1px solid {BORDER};
                border-radius: 6px;
                margin-bottom: 4px;
                padding: 8px;
            }}
            QListWidget::item:hover {{
                background-color: {ACCENT};
                color: #FFFFFF;
            }}
            QListWidget::item:selected {{
                background-color: {ACCENT2};
                color: #FFFFFF;
            }}
            QComboBox {{
                background-color: {BG3};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 6px 12px;
                color: {TEXT};
                min-width: 150px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QPushButton {{
                background-color: {BG3};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {ACCENT};
                border-color: {ACCENT};
                color: #FFFFFF;
            }}
            QPushButton#btn_prev {{
                background-color: #1E293B;
                border: 1px solid #334155;
            }}
            QPushButton#btn_prev:hover {{
                background-color: #334155;
            }}
            QPushButton#btn_next {{
                background-color: #4F46E5;
                border: 1px solid #6366F1;
            }}
            QPushButton#btn_next:hover {{
                background-color: #6366F1;
            }}
            QPushButton#btn_auto {{
                background-color: #059669;
                border: 1px solid #10B981;
            }}
            QPushButton#btn_auto:hover {{
                background-color: #10B981;
            }}
            QPushButton#btn_reset {{
                background-color: #DC2626;
                border: 1px solid #EF4444;
            }}
            QPushButton#btn_reset:hover {{
                background-color: #EF4444;
            }}
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
        """)
        
    def change_level(self, idx):
        self.current_level_idx = idx
        self.reset_game()
        
    def reset_game(self):
        self.auto_timer.stop()
        self.btn_auto.setText("▶ Auto")
        self._load_level(self.current_level_idx)
        self.board.set_map(self.walls, self.goals, self.initial_state, False)
        self.steps = []
        self.current_step = -1
        self.log_list.clear()
        
        # Reset cards
        self.card_status.v_lbl.setText("Reset")
        self.card_time.v_lbl.setText("0.0")
        self.card_frontier.v_lbl.setText("0")
        self.card_visited.v_lbl.setText("0")
        self.card_depth.v_lbl.setText("0")
        
        # Clear Frontier / Explored
        self._clear_layout(self.front_scroll_layout)
        self._clear_layout(self.exp_scroll_layout)
        
        # Tự động giải lại với thuật toán đang chọn
        self.run_algorithm()
        
    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def _on_algo_change(self, idx):
        self.reset_game()
        
    def run_algorithm(self):
        self.auto_timer.stop()
        self.btn_auto.setText("▶ Auto")
        self.log_list.clear()
        
        algo_idx = self.algo_combo.currentIndex()
        
        # Cấu hình title cho card dựa trên thuật toán
        if algo_idx in [4, 5]: # Local Search
            self.card_depth.layout().itemAt(0).widget().setText("HEURISTIC h")
        elif algo_idx in [10, 11]: # RL (Q-learning, SARSA)
            self.card_depth.layout().itemAt(0).widget().setText("Q-VALUE / DỰ ĐOÁN")
        else:
            self.card_depth.layout().itemAt(0).widget().setText("ĐỘ SÂU (DEPTH)")
            
        # Thực thi thuật toán
        start_time = time.perf_counter()
        
        if algo_idx == 0:
            self.steps = bfs_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 1:
            self.steps = dfs_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 2:
            self.steps = greedy_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 3:
            self.steps = astar_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 4:
            self.steps = hillclimbing_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 5:
            self.steps = steepest_hillclimbing_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 6:
            self.steps = backtracking_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 7:
            self.steps = forward_checking_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 8:
            self.steps = belief_state_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 9:
            self.steps = partial_obs_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 10:
            self.steps = q_learning_steps(self.initial_state, self.goals, self.walls)
        elif algo_idx == 11:
            self.steps = sarsa_steps(self.initial_state, self.goals, self.walls)
            
        elapsed_time = (time.perf_counter() - start_time) * 1000
        self.card_time.v_lbl.setText(f"{elapsed_time:.2f}")
        
        if not self.steps:
            self.card_status.v_lbl.setText("Failed")
            return
            
        self.current_step = 0
        self._populate_logs()
        self._render_step(0)
        
    def _populate_logs(self):
        for idx, step in enumerate(self.steps):
            t = step['type']
            depth = step.get('depth', 0)
            
            # Format text log hiển thị
            if t == 'goal':
                txt = f"🏆 [GOAL] Đã tìm ra đích ở bước {depth}!"
            elif t == 'limit_reached':
                txt = f"⚠️ [LIMIT] Đạt giới hạn tìm kiếm tối đa!"
            elif t == 'local_optimum':
                txt = f"⛰️ [STUCK] Kẹt tại cực trị cục bộ (h = {step.get('cost', 0)})"
            elif t == 'skip':
                msg = step.get('message', 'Bỏ qua do đã duyệt đường ngắn hơn')
                txt = f"⏭️ [SKIP] {msg}"
            elif t == 'new_iteration':
                msg = step.get('message', 'Vòng lặp mới')
                txt = f"🔁 {msg}"
            elif t == 'restart':
                txt = f"🔄 KHỞI ĐỘNG LẠI từ trạng thái ngẫu nhiên"
            else:
                txt = f"Step {idx:03d} (depth={depth}): Đi theo hướng {step['moves'][-1] if step['moves'] else 'Start'}"
                
            item = QListWidgetItem(txt)
            self.log_list.addItem(item)
            
        self.log_list.setCurrentRow(0)
        
    def _on_log_clicked(self, item):
        row = self.log_list.row(item)
        if 0 <= row < len(self.steps):
            self.current_step = row
            self._render_step(row)
            
    def _render_step(self, idx):
        if not self.steps or not (0 <= idx < len(self.steps)):
            return
            
        self.log_list.setCurrentRow(idx)
        step = self.steps[idx]
        
        # Cập nhật trạng thái sương mù nếu là thuật toán Partial Observation
        algo_idx = self.algo_combo.currentIndex()
        is_partial = (algo_idx == 9)
        
        # Cập nhật bản đồ game
        self.board.set_map(self.walls, self.goals, step['state'], is_partial)
        
        # Cập nhật card chỉ số
        t = step['type']
        if t == 'goal':
            self.card_status.v_lbl.setText("Goal Found")
            self.card_status.v_lbl.setStyleSheet(f"color:#10B981; font-size:16px; font-weight:bold; border:none;")
        elif t == 'local_optimum':
            self.card_status.v_lbl.setText("Stuck")
            self.card_status.v_lbl.setStyleSheet(f"color:#EF4444; font-size:16px; font-weight:bold; border:none;")
        elif t == 'limit_reached':
            self.card_status.v_lbl.setText("Limit Reached")
            self.card_status.v_lbl.setStyleSheet(f"color:#F59E0B; font-size:16px; font-weight:bold; border:none;")
        else:
            self.card_status.v_lbl.setText("Running")
            self.card_status.v_lbl.setStyleSheet(f"color:{ACCENT2}; font-size:16px; font-weight:bold; border:none;")
            
        self.card_frontier.v_lbl.setText(str(step.get('frontier_count', 0)))
        self.card_visited.v_lbl.setText(str(step.get('visited_count', 0)))
        
        # Cập nhật card cuối cùng (HEURISTIC h hoặc DEPTH)
        if algo_idx in [4, 5]: # Local Search
            self.card_depth.v_lbl.setText(f"h = {step.get('cost', 0)}")
        elif algo_idx in [10, 11]: # RL (Q-learning, SARSA)
            # Hiện message action
            self.card_depth.v_lbl.setText(f"{step.get('message', 'Learn')}")
        else:
            self.card_depth.v_lbl.setText(str(step.get('depth', 0)))
            
        # Vẽ các mini boards cho Frontier
        self._clear_layout(self.front_scroll_layout)
        for fn_node in step.get('frontier', [])[:10]:
            # fn_node là dict chứa state
            # Tạo mini board
            fn_state = fn_node['state']
            mb = MiniSokobanBoard(self.walls, self.goals, fn_state)
            self.front_scroll_layout.addWidget(mb)
            
        # Vẽ các mini boards cho Explored
        self._clear_layout(self.exp_scroll_layout)
        for exp_node in step.get('explored', [])[:10]:
            # exp_node là tuple (state, cost, via)
            exp_state = exp_node[0]
            mb = MiniSokobanBoard(self.walls, self.goals, exp_state)
            self.exp_scroll_layout.addWidget(mb)
            
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._render_step(self.current_step)
            
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._render_step(self.current_step)
        else:
            self.auto_timer.stop()
            self.btn_auto.setText("▶ Auto")
            
    def toggle_auto(self):
        if self.auto_timer.isActive():
            self.auto_timer.stop()
            self.btn_auto.setText("▶ Auto")
        else:
            self.auto_timer.start(150) # 150ms mỗi bước
            self.btn_auto.setText("⏸ Pause")
            
    def keyPressEvent(self, event):
        # Hỗ trợ phím tắt điều khiển
        if event.key() == Qt.Key_Left:
            self.prev_step()
        elif event.key() == Qt.Key_Right:
            self.next_step()
        elif event.key() == Qt.Key_Space:
            self.toggle_auto()
        else:
            super().keyPressEvent(event)
