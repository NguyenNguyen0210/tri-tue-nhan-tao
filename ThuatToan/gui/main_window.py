from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QScrollArea,
    QLineEdit, QGroupBox, QComboBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from config import (
    BG, BG2, BG3, BORDER, ACCENT, ACCENT2, GREEN, RED, ORANGE, TEAL,
    TEXT, TEXT_DIM, PURPLE, PURPLE_BG, GOAL
)
from gui.widgets import BoardWidget, MiniBoard
from algorithms import astar_steps, idastar_steps, hillclimbing_steps, steepest_hillclimbing_steps, ucs_steps, bfs_steps, dfs_steps, ids_steps

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8-Puzzle Solver & Visualizer")
        self.setMinimumSize(1520, 780)
        self.steps = []
        self.current_step = -1
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.next_step)
        self._build_ui()
        self._apply_style()
        self.run_algorithm()

    # ── Style ────────────────────────────────────────────────────
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
            QPushButton:pressed {{
                background-color: {ACCENT2};
                border-color: {ACCENT2};
            }}
            QPushButton:disabled {{
                background-color: {BG2};
                color: {TEXT_DIM};
                border-color: {BORDER};
            }}
            QPushButton#btn_prev {{
                background-color: #1E293B;
                color: #E2E8F0;
                border: 1px solid #334155;
            }}
            QPushButton#btn_prev:hover {{
                background-color: #334155;
                border-color: #475569;
            }}
            QPushButton#btn_next {{
                background-color: #4F46E5;
                color: #FFFFFF;
                border: 1px solid #6366F1;
            }}
            QPushButton#btn_next:hover {{
                background-color: #6366F1;
                border-color: #818CF8;
            }}
            QPushButton#btn_auto {{
                background-color: #059669;
                color: #FFFFFF;
                border: 1px solid #10B981;
            }}
            QPushButton#btn_auto:hover {{
                background-color: #10B981;
                border-color: #34D399;
            }}
            QPushButton#btn_reset {{
                background-color: #DC2626;
                color: #FFFFFF;
                border: 1px solid #EF4444;
            }}
            QPushButton#btn_reset:hover {{
                background-color: #EF4444;
                border-color: #F87171;
            }}
            QLineEdit {{
                background-color: {BG2};
                color: {TEXT};
                border: 1.5px solid {BORDER};
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                font-family: 'JetBrains Mono', Consolas, monospace;
            }}
            QLineEdit:focus {{
                border-color: {ACCENT};
                background-color: {BG3};
            }}
            QComboBox {{
                background-color: {BG2};
                color: {TEXT};
                border: 1.5px solid {BORDER};
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: bold;
            }}
            QComboBox:hover {{
                border-color: {ACCENT};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG2};
                color: {TEXT};
                selection-background-color: {ACCENT};
                border: 1px solid {BORDER};
                outline: none;
            }}
            QListWidget {{
                background-color: {BG2};
                color: {TEXT};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
                outline: none;
                padding: 4px;
            }}
            QListWidget::item {{
                padding: 8px 12px;
                border-bottom: 1px solid {BG3};
                border-radius: 6px;
                margin: 2px 4px;
            }}
            QListWidget::item:selected {{
                background-color: {ACCENT};
                color: #FFFFFF;
            }}
            QListWidget::item:hover {{
                background-color: {BG3};
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: {BG};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {ACCENT};
            }}
            QGroupBox {{
                border: 1.5px solid {BORDER};
                border-radius: 12px;
                margin-top: 18px;
                padding: 18px 12px 12px 12px;
                background-color: {BG2};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 14px;
                color: {ACCENT2};
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """)

    # ── Build UI ─────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # ── Custom Title Bar ──────────────────────────────────────────
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet(f"background-color: {BG2}; border-bottom: 1.5px solid {BORDER};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title_lbl = QLabel("8-PUZZLE VISUALIZER")
        title_lbl.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT}; letter-spacing: 2px;")
        header_layout.addWidget(title_lbl)

        header_layout.addStretch()

        subtitle_lbl = QLabel("AI SEARCH SOLVER")
        subtitle_lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        subtitle_lbl.setStyleSheet(f"color: {ACCENT2}; background: {BG3}; padding: 6px 14px; border-radius: 12px; border: 1px solid {BORDER};")
        header_layout.addWidget(subtitle_lbl)
        
        main_layout.addWidget(header)

        # Content Panel
        content = QWidget()
        main_layout.addWidget(content)
        root = QHBoxLayout(content)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # ══ Cột trái (Control Panel - 380px) ════════════════════════
        left = QWidget()
        left.setFixedWidth(380)
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0,0,0,0)
        lv.setSpacing(12)

        # Algorithm selector
        algo_box = QGroupBox("THUẬT TOÁN")
        ahl = QVBoxLayout(algo_box)
        ahl.setSpacing(8)
        self.algo_combo = QComboBox()
        self.algo_combo.addItem("A*  —  A* Search")
        self.algo_combo.addItem("IDA*  —  Iterative Deepening A*")
        self.algo_combo.addItem("Simple Hill Climbing  —  Local Search")
        self.algo_combo.addItem("Steepest-Ascent Hill Climbing  —  Local Search")
        self.algo_combo.addItem("UCS  —  Uniform Cost Search")
        self.algo_combo.addItem("IDS  —  Iterative Deepening Search")
        self.algo_combo.addItem("BFS  —  Breadth First Search")
        self.algo_combo.addItem("DFS  —  Depth First Search")
        self.algo_combo.currentIndexChanged.connect(self._on_algo_change)
        ahl.addWidget(self.algo_combo)
        self.algo_desc = QLabel("f(n) = g(n) + h(n) với g(n) là khoảng cách Manhattan, h(n) là số ô sai vị trí")
        self.algo_desc.setWordWrap(True)
        self.algo_desc.setStyleSheet(f"color:{ACCENT2};font-size:11px;font-weight:bold;")
        ahl.addWidget(self.algo_desc)
        lv.addWidget(algo_box)

        # Input
        inp_box = QGroupBox("INPUT  (0 = ô trống)")
        ihl = QVBoxLayout(inp_box)
        ihl.setSpacing(6)
        row_i = QHBoxLayout()
        self.inp_edit = QLineEdit("1 2 3 4 0 6 7 5 8")
        row_i.addWidget(self.inp_edit)
        btn_run = QPushButton("Submit ➔")
        btn_run.setMinimumWidth(100)
        btn_run.clicked.connect(self.run_algorithm)
        row_i.addWidget(btn_run)
        ihl.addLayout(row_i)
        lv.addWidget(inp_box)

        # Stats
        stats_box = QGroupBox("THỐNG KÊ CHI TIẾT")
        sg = QGridLayout(stats_box)
        sg.setSpacing(10)
        
        def mkstat(lbl, val_color="#F8FAFC"):
            card = QWidget()
            card.setStyleSheet(f"""
                QWidget {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #161B2E, stop:1 #0D111F);
                    border: 1px solid #252B44;
                    border-radius: 10px;
                }}
                QWidget:hover {{
                    border-color: #38BDF8;
                }}
                QLabel {{
                    border: none;
                    background: transparent;
                }}
            """)
            cv = QVBoxLayout(card)
            cv.setContentsMargins(12, 10, 12, 10)
            cv.setSpacing(4)
            
            l = QLabel(lbl)
            l.setStyleSheet(f"color: {TEXT_DIM}; font-size: 10px; font-weight: bold; text-transform: uppercase; font-family: 'Segoe UI';")
            
            v = QLabel("—")
            v.setStyleSheet(f"color: {val_color}; font-size: 18px; font-weight: bold; font-family: 'JetBrains Mono', Consolas, monospace;")
            
            cv.addWidget(l)
            cv.addWidget(v)
            return card, l, v

        card_step, _, self.lbl_step = mkstat("Bước / Lần pop", "#10B981")
        card_cost, self.lbl_cost_title, self.lbl_cost = mkstat("Cost", "#38BDF8")
        card_visited, _, self.lbl_visited = mkstat("Đã xét (explored)", "#A78BFA")
        card_frontier, _, self.lbl_frontier = mkstat("Frontier size", "#06B6D4")
        card_iter, _, self.lbl_iter = mkstat("Iteration (IDS)", "#F59E0B")
        card_limit, _, self.lbl_limit = mkstat("Depth limit (IDS)", "#EF4444")

        sg.addWidget(card_step, 0, 0)
        sg.addWidget(card_cost, 0, 1)
        sg.addWidget(card_visited, 1, 0)
        sg.addWidget(card_frontier, 1, 1)
        sg.addWidget(card_iter, 2, 0)
        sg.addWidget(card_limit, 2, 1)
        lv.addWidget(stats_box)
        
        lv.addStretch()
        root.addWidget(left)

        # ══ Cột giữa (Hero Visualizer Column) ════════════════════════
        mid_col = QWidget()
        mv = QVBoxLayout(mid_col)
        mv.setContentsMargins(0, 0, 0, 0)
        mv.setSpacing(14)

        # Info Box / Alert
        self.info_box = QLabel("Nhấn ▶ để bắt đầu.")
        self.info_box.setWordWrap(True)
        self.info_box.setTextFormat(Qt.RichText)
        self.info_box.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1A1E2F, stop:1 #111420);
            border: 1px solid #252B44;
            border-left: 4px solid #6366F1;
            border-radius: 8px;
            padding: 14px 18px;
            font-size: 13px;
            font-weight: 500;
        """)
        self.info_box.setMinimumHeight(60)
        mv.addWidget(self.info_box)

        # Boards Frame
        boards_container = QWidget()
        boards_container.setStyleSheet(f"background: {BG2}; border: 1.5px solid {BORDER}; border-radius: 16px;")
        bvl = QVBoxLayout(boards_container)
        bvl.setContentsMargins(20, 20, 20, 20)
        bvl.setSpacing(16)

        # Current board (Đang xét) - Centered & Large
        self.board_current = BoardWidget("TRẠNG THÁI ĐANG XÉT", 60)
        bvl.addWidget(self.board_current)
        
        # Divider line
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background: {BORDER};")
        bvl.addWidget(divider)

        # Horizontal row for reference boards
        ref_row = QWidget()
        ref_row.setStyleSheet("background: transparent; border: none;")
        r_layout = QHBoxLayout(ref_row)
        r_layout.setContentsMargins(0, 0, 0, 0)
        r_layout.setSpacing(24)
        
        self.board_start = BoardWidget("TRẠNG THÁI ĐẦU", 38)
        self.board_goal  = BoardWidget("TRẠNG THÁI ĐÍCH", 38)
        r_layout.addWidget(self.board_start)
        r_layout.addWidget(self.board_goal)
        bvl.addWidget(ref_row)
        
        mv.addWidget(boards_container)

        # Controls Row
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(8)
        self.btn_prev  = QPushButton("◀ Prev")
        self.btn_next  = QPushButton("Next ▶")
        self.btn_auto  = QPushButton("▷ Auto")
        self.btn_reset = QPushButton("↺ Reset")
        self.btn_prev.setObjectName("btn_prev")
        self.btn_next.setObjectName("btn_next")
        self.btn_auto.setObjectName("btn_auto")
        self.btn_reset.setObjectName("btn_reset")
        for b in [self.btn_prev, self.btn_next, self.btn_auto, self.btn_reset]:
            ctrl_layout.addWidget(b)
        self.btn_prev.clicked.connect(self.prev_step)
        self.btn_next.clicked.connect(self.next_step)
        self.btn_auto.clicked.connect(self.toggle_auto)
        self.btn_reset.clicked.connect(self.reset)
        
        mv.addLayout(ctrl_layout)
        mv.addStretch()
        root.addWidget(mid_col, 1)

        # ══ Cột phải (Frontier, Explored, Logs) ════════════════════
        right_col = QWidget()
        rv = QVBoxLayout(right_col)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(14)

        # Upper container: Frontier and Explored side-by-side
        fe_container = QWidget()
        fe_layout = QHBoxLayout(fe_container)
        fe_layout.setContentsMargins(0, 0, 0, 0)
        fe_layout.setSpacing(12)

        # Frontier sub-panel
        frontier_panel = QGroupBox("FRONTIER LIST")
        fp_v = QVBoxLayout(frontier_panel)
        fp_v.setContentsMargins(8, 14, 8, 8)
        fp_v.setSpacing(6)
        
        self.frontier_label = QLabel("<span style='color:#38BDF8;'>■</span> FRONTIER")
        self.frontier_label.setStyleSheet(f"color:{TEXT_DIM};font-size:10px;font-weight:bold;text-transform:uppercase;")
        fp_v.addWidget(self.frontier_label)

        self.frontier_scroll = QScrollArea()
        self.frontier_scroll.setWidgetResizable(True)
        self.frontier_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frontier_content = QWidget()
        self.frontier_layout = QVBoxLayout(self.frontier_content)
        self.frontier_layout.setAlignment(Qt.AlignTop)
        self.frontier_layout.setSpacing(8)
        self.frontier_layout.setContentsMargins(4, 4, 4, 4)
        self.frontier_scroll.setWidget(self.frontier_content)
        fp_v.addWidget(self.frontier_scroll)
        fe_layout.addWidget(frontier_panel)

        # Explored sub-panel
        explored_panel = QGroupBox("EXPLORED LIST")
        ep_v = QVBoxLayout(explored_panel)
        ep_v.setContentsMargins(8, 14, 8, 8)
        ep_v.setSpacing(6)

        self.explored_label = QLabel("<span style='color:#A78BFA;'>■</span> EXPLORED")
        self.explored_label.setStyleSheet(f"color:{TEXT_DIM};font-size:10px;font-weight:bold;text-transform:uppercase;")
        ep_v.addWidget(self.explored_label)
        
        self.explored_sub = QLabel("Các node đã pop & mở rộng")
        self.explored_sub.setStyleSheet(f"color:{PURPLE};font-size:10px;")
        ep_v.addWidget(self.explored_sub)

        self.explored_scroll = QScrollArea()
        self.explored_scroll.setWidgetResizable(True)
        self.explored_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.explored_content = QWidget()
        self.explored_layout = QVBoxLayout(self.explored_content)
        self.explored_layout.setAlignment(Qt.AlignTop)
        self.explored_layout.setSpacing(8)
        self.explored_layout.setContentsMargins(4, 4, 4, 4)
        self.explored_scroll.setWidget(self.explored_content)
        ep_v.addWidget(self.explored_scroll)
        fe_layout.addWidget(explored_panel)

        rv.addWidget(fe_container, 3) # Expand ratio 3

        # Lower container: Log List
        log_panel = QGroupBox("LOG CÁC BƯỚC DUYỆT")
        lp_v = QVBoxLayout(log_panel)
        lp_v.setContentsMargins(8, 14, 8, 8)
        lp_v.setSpacing(6)
        
        self.log_list = QListWidget()
        self.log_list.setFont(QFont("Consolas", 10))
        self.log_list.itemClicked.connect(self.on_log_click)
        lp_v.addWidget(self.log_list)
        
        rv.addWidget(log_panel, 2) # Expand ratio 2
        root.addWidget(right_col, 1)

    # ── Algorithm selector ───────────────────────────────────────
    def _on_algo_change(self, idx):
        if idx == 0:
            self.algo_desc.setText("f(n) = g(n) + h(n) với g(n) là khoảng cách Manhattan, h(n) là số ô sai vị trí")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> FRONTIER  (priority queue — min-heap theo f_score)")
            self.lbl_cost_title.setText("f = g + h")
        elif idx == 1:
            self.algo_desc.setText("IDA*: f(n) = g(n) + h(n) với giới hạn ngưỡng f_limit tăng dần (DFS Stack)")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> FRONTIER  (LIFO stack — đỉnh stack sẽ pop tiếp)")
            self.lbl_cost_title.setText("f = g + h")
        elif idx == 2:
            self.algo_desc.setText("Simple Hill Climbing: di chuyển tới trạng thái lân cận tốt hơn đầu tiên dựa trên khoảng cách Manhattan")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> LÂN CẬN  (các trạng thái lân cận đang được đánh giá)")
            self.lbl_cost_title.setText("Heuristic h")
        elif idx == 3:
            self.algo_desc.setText("Steepest-Ascent Hill Climbing: di chuyển tới trạng thái lân cận tốt nhất (heuristic tối ưu nhất)")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> LÂN CẬN  (các trạng thái lân cận đang được đánh giá)")
            self.lbl_cost_title.setText("Heuristic h")
        elif idx == 4:
            self.algo_desc.setText("Cost = số ô sai vị trí (misplaced tiles)")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> FRONTIER  (priority queue — min-heap theo cost)")
            self.lbl_cost_title.setText("Cost")
        elif idx == 5:
            self.algo_desc.setText("Lặp DFS có giới hạn độ sâu từ 0 → ∞ (LIFO stack)")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> FRONTIER  (LIFO stack — đỉnh stack sẽ pop tiếp)")
            self.lbl_cost_title.setText("Depth")
        elif idx == 6:
            self.algo_desc.setText("Duyệt theo chiều rộng dùng hàng đợi FIFO (queue)")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> FRONTIER  (FIFO queue — đầu queue sẽ pop tiếp)")
            self.lbl_cost_title.setText("—")
        else:
            self.algo_desc.setText("Duyệt theo chiều sâu dùng ngăn xếp LIFO (stack)")
            self.frontier_label.setText("<span style='color:#38BDF8;'>■</span> FRONTIER  (LIFO stack — đỉnh stack sẽ pop tiếp)")
            self.lbl_cost_title.setText("—")
        self.run_algorithm()


    # ── Run ─────────────────────────────────────────────────────
    def run_algorithm(self):
        self.auto_timer.stop()
        self.btn_auto.setText("▷ Auto")
        try:
            nums = list(map(int, self.inp_edit.text().strip().split()))
            assert len(nums)==9 and sorted(nums)==list(range(9))
            start = tuple(nums)
        except:
            self.info_box.setText("❌ Input không hợp lệ! Nhập đúng 9 số 0–8.")
            return
        algo = self.algo_combo.currentIndex()
        if algo == 0:
            self.steps = astar_steps(start, GOAL)
            algo_name = "A*"
        elif algo == 1:
            self.steps = idastar_steps(start, GOAL)
            algo_name = "IDA*"
        elif algo == 2:
            self.steps = hillclimbing_steps(start, GOAL)
            algo_name = "Simple Hill Climbing"
        elif algo == 3:
            self.steps = steepest_hillclimbing_steps(start, GOAL)
            algo_name = "Steepest-Ascent Hill Climbing"
        elif algo == 4:
            self.steps = ucs_steps(start, GOAL)
            algo_name = "UCS"
        elif algo == 5:
            self.steps = ids_steps(start, GOAL)
            algo_name = "IDS"
        elif algo == 6:
            self.steps = bfs_steps(start, GOAL)
            algo_name = "BFS"
        else:
            self.steps = dfs_steps(start, GOAL)
            algo_name = "DFS"
        self.current_step = -1
        self.log_list.clear()
        self.board_start.set_state(start)
        self.board_current.set_state(start)
        self.board_goal.set_state(GOAL, goal_mode=True)
        self._clear_panel(self.frontier_layout)
        self._clear_panel(self.explored_layout)
        self.info_box.setText(f"✅ <b>{algo_name}</b> tính xong <b>{len(self.steps)}</b> bước. Nhấn <b>▶</b> để xem.")
        self._update_stats(0, 0, 0, 0, None, None)
        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(True)

    def reset(self):
        self.auto_timer.stop()
        self.btn_auto.setText("▷ Auto")
        self.current_step = -1
        self.log_list.clear()
        self._clear_panel(self.frontier_layout)
        self._clear_panel(self.explored_layout)
        try:
            start = tuple(map(int, self.inp_edit.text().strip().split()))
            self.board_start.set_state(start)
            self.board_current.set_state(start)
        except: pass
        self.info_box.setText("Nhấn <b>▶</b> để bắt đầu.")
        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(True)

    # ── Navigation ───────────────────────────────────────────────
    def next_step(self):
        if self.current_step >= len(self.steps)-1:
            self.auto_timer.stop(); self.btn_auto.setText("▷ Auto")
            self.btn_next.setEnabled(False); return
        self.current_step += 1
        self._render_step(self.current_step)
        self.btn_prev.setEnabled(True)
        self.btn_next.setEnabled(self.current_step < len(self.steps)-1)

    def prev_step(self):
        if self.current_step <= 0: return
        self.current_step -= 1
        self._render_step(self.current_step)
        self.btn_prev.setEnabled(self.current_step > 0)
        self.btn_next.setEnabled(True)

    def toggle_auto(self):
        if self.auto_timer.isActive():
            self.auto_timer.stop(); self.btn_auto.setText("▷ Auto")
        else:
            self.auto_timer.start(500); self.btn_auto.setText("◼ Stop")

    def on_log_click(self, item):
        idx = item.data(Qt.UserRole)
        if idx is not None:
            self.current_step = idx
            self._render_step(idx)
            self.btn_prev.setEnabled(idx > 0)
            self.btn_next.setEnabled(idx < len(self.steps)-1)

    # ── Render step ──────────────────────────────────────────────
    def _render_step(self, idx):
        s = self.steps[idx]
        prev_state = self.steps[idx-1]['state'] if idx > 0 else None
        t = s['type']
        algo = self.algo_combo.currentIndex()

        # Board
        special = None
        if t == 'cutoff': special = 'cutoff'
        elif t == 'cycle': special = 'cycle'
        elif t == 'local_optimum': special = 'cycle'
        goal_mode = (t == 'goal')
        self.board_current.set_state(s['state'], prev_state, goal_mode=goal_mode, special=special)

        # Info & log
        via = s['moves'][-1] if s['moves'] else 'start'
        dir_names = {'↑': 'Lên ↑', '↓': 'Xuống ↓', '←': 'Trái ←', '→': 'Phải →', 'start': 'Bắt đầu'}
        via_vn = dir_names.get(via, via)

        if t == 'new_iteration':
            if algo == 1:
                msg = f"🔄 <b>Vòng lặp mới (IDA*) - Lần {s['iteration']}</b>: Thiết lập ngưỡng f_limit = <b>{s['limit']}</b>. Khởi tạo lại ngăn xếp từ trạng thái bắt đầu."
                self._add_log(idx, f"🔄 [IDA*] Vòng lặp {s['iteration']} (Ngưỡng f={s['limit']})", TEAL)
            else:
                msg = f"🔄 <b>Vòng lặp mới (IDS) - Lần {s['iteration']}</b>: Thiết lập giới hạn độ sâu tối đa l = <b>{s['limit']}</b>. Khởi tạo lại ngăn xếp (LIFO stack) từ trạng thái bắt đầu."
                self._add_log(idx, f"🔄 [IDS] Vòng lặp {s['iteration']} (Giới hạn độ sâu l={s['limit']})", TEAL)
        elif t == 'cutoff':
            if algo == 1:
                msg = f"✂️ <b>VƯỢT NGƯỠNG (CUTOFF)</b>: Trạng thái hiện tại có chi phí f = <b>{s['cost']}</b> vượt quá ngưỡng f_limit = <b>{s['limit']}</b>. Dừng mở rộng nhánh này."
                self._add_log(idx, f"✂️ Vượt ngưỡng: Chi phí f={s['cost']} > ngưỡng f_limit={s['limit']}", ORANGE)
            else:
                msg = f"✂️ <b>CẮT NHÁNH (CUTOFF)</b>: Trạng thái hiện tại ở độ sâu <b>{s['depth']}</b> đã đạt tới giới hạn <b>{s['limit']}</b>. Dừng mở rộng thêm nhánh này."
                self._add_log(idx, f"✂️ Cắt nhánh: Độ sâu d={s['depth']} đạt giới hạn l={s['limit']}", ORANGE)
        elif t == 'local_optimum':
            msg = f"⛰️ <b>LOCAL OPTIMUM / PLATEAU REACHED</b>: Không tìm thấy trạng thái lân cận nào có chi phí tốt hơn trạng thái hiện tại (h = <b>{s['cost']}</b>). Thuật toán dừng lại tại độ sâu <b>{s['depth']}</b>."
            self._add_log(idx, f"⛰️ Kẹt tại cực trị: h={s['cost']} ở độ sâu d={s['depth']}", ORANGE)
        elif t == 'cycle':
            msg = f"🔁 <b>PHÁT HIỆN CHU KỲ</b>: Trạng thái này trùng với một trạng thái có sẵn trong nhánh hiện tại (độ sâu <b>{s['depth']}</b>). Bỏ qua để tránh lặp vô hạn."
            self._add_log(idx, f"🔁 Trùng lặp chu kỳ ở độ sâu d={s['depth']}", PURPLE)
        elif t == 'skip':
            if algo in (0, 1):
                msg = f"⏭ <b>BỎ QUA (ĐÃ XÉT)</b>: Trạng thái đi theo hướng <b>'{via_vn}'</b> có chi phí f = <b>{s['cost']}</b> nhưng đã được duyệt qua trước đó."
                self._add_log(idx, f"⏭ Bỏ qua (đã xét): Hướng {via_vn}, chi phí f={s['cost']}", TEXT_DIM)
            elif algo == 4:
                msg = f"⏭ <b>BỎ QUA (ĐÃ XÉT)</b>: Trạng thái đi theo hướng <b>'{via_vn}'</b> có chi phí g = <b>{s['cost']}</b> nhưng đã được duyệt qua trước đó."
                self._add_log(idx, f"⏭ Bỏ qua (đã xét): Hướng {via_vn}, chi phí g={s['cost']}", TEXT_DIM)
            else:
                msg = f"⏭ <b>BỎ QUA (ĐÃ XÉT)</b>: Trạng thái đi theo hướng <b>'{via_vn}'</b> đã được duyệt qua trước đó."
                self._add_log(idx, f"⏭ Bỏ qua (đã xét): Hướng {via_vn}", TEXT_DIM)
        elif t == 'limit_reached':
            msg = f"<span style='color:{RED};'><b>⚠️ ĐẠT GIỚI HẠN TỐI ĐA {idx+1} BƯỚC DUYỆT!</b></span> Tiến trình tự động dừng để tránh quá tải bộ nhớ."
            self._add_log(idx, f"⚠️ Dừng duyệt: Đạt giới hạn tối đa {idx+1} bước", RED)
            self.auto_timer.stop(); self.btn_auto.setText("▷ Auto")
        elif t == 'goal':
            if algo == 0:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (A*)!</b></span> "
                       f"Chi phí tối ưu f = <b>{s['cost']}</b> (độ dài đường đi = {s['depth']} bước), hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích có chi phí f={s['cost']} (nước đi {via_vn})", GREEN)
            elif algo == 1:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (IDA*)!</b></span> "
                       f"Chi phí tối ưu f = <b>{s['cost']}</b> (đường đi = {s['depth']} bước, ngưỡng l = {s['limit']}), hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích có chi phí f={s['cost']} (nước đi {via_vn})", GREEN)
            elif algo == 2:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (Hill Climbing)!</b></span> "
                       f"Độ dài đường đi = {s['depth']} bước, hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích ở độ sâu d={s['depth']} (nước đi {via_vn})", GREEN)
            elif algo == 3:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (Steepest-Ascent Hill Climbing)!</b></span> "
                       f"Độ dài đường đi = {s['depth']} bước, hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích ở độ sâu d={s['depth']} (nước đi {via_vn})", GREEN)
            elif algo == 4:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (UCS)!</b></span> "
                       f"Chi phí tối ưu g = <b>{s['cost']}</b>, hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích có chi phí g={s['cost']} (nước đi {via_vn})", GREEN)
            elif algo == 5:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (IDS)!</b></span> "
                       f"Độ sâu lời giải d = <b>{s['depth']}</b> (giới hạn l = {s['limit']}), hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét qua các vòng lặp: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích ở độ sâu d={s['depth']} (nước đi {via_vn})", GREEN)
            elif algo == 6:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (BFS)!</b></span> "
                       f"Độ sâu lời giải d = <b>{s['depth']}</b>, hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích ở độ sâu d={s['depth']} (nước đi {via_vn})", GREEN)
            else:
                msg = (f"<span style='color:{GREEN};'><b>✅ ĐÃ TÌM THẤY TRẠNG THÁI ĐÍCH (DFS)!</b></span> "
                       f"Độ sâu lời giải d = <b>{s['depth']}</b>, hướng di chuyển <b>'{via_vn}'</b>. "
                       f"Tổng số trạng thái đã xét: <b>{s['visited_count']}</b>.")
                self._add_log(idx, f"✅ THÀNH CÔNG! Đích ở độ sâu d={s['depth']} (nước đi {via_vn})", GREEN)
            self.auto_timer.stop(); self.btn_auto.setText("▷ Auto")
        else:
            if algo == 0:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (chi phí f={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [A*]: Lấy ra trạng thái có chi phí f = <b>{s['cost']}</b> (nước đi <b>'{via_vn}'</b>, độ sâu d = <b>{s['depth']}</b>). "
                       f"Mở rộng thêm <b>{len(s.get('added',[]))}</b> trạng thái con vào hàng đợi ưu tiên (min-heap): {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Mở rộng trạng thái chi phí f={s['cost']} (hướng {via_vn}) ➔ Thêm {len(s.get('added',[]))} con", TEXT)
            elif algo == 1:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (chi phí f={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [IDA*, ngưỡng f_limit={s['limit']}]: Lấy ra trạng thái có chi phí f = <b>{s['cost']}</b> (nước đi <b>'{via_vn}'</b>, độ sâu d = <b>{s['depth']}</b>). "
                       f"Mở rộng thêm <b>{len(s.get('added',[]))}</b> trạng thái con vào ngăn xếp (stack): {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Mở rộng trạng thái f={s['cost']}/{s['limit']} (hướng {via_vn}) ➔ Thêm {len(s.get('added',[]))} con", TEXT)
            elif algo == 2:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (h={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [Simple Hill Climbing]: Lấy ra trạng thái có chi phí h = <b>{s['cost']}</b> (nước đi <b>'{via_vn}'</b>, độ sâu d = <b>{s['depth']}</b>). "
                       f"Di chuyển sang trạng thái tốt hơn đầu tiên tìm thấy: {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Di chuyển sang trạng thái tốt hơn (hướng {via_vn}, h={s['cost']})", TEXT)
            elif algo == 3:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (h={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [Steepest-Ascent Hill Climbing]: Lấy ra trạng thái có chi phí h = <b>{s['cost']}</b> (nước đi <b>'{via_vn}'</b>, độ sâu d = <b>{s['depth']}</b>). "
                       f"Di chuyển sang trạng thái tốt nhất: {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Di chuyển sang trạng thái tốt nhất (hướng {via_vn}, h={s['cost']})", TEXT)
            elif algo == 4:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (chi phí g={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [UCS]: Lấy ra trạng thái có chi phí g = <b>{s['cost']}</b> (nước đi <b>'{via_vn}'</b>). "
                       f"Mở rộng thêm <b>{len(s.get('added',[]))}</b> trạng thái con vào hàng đợi ưu tiên (min-heap): {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Mở rộng trạng thái chi phí g={s['cost']} (hướng {via_vn}) ➔ Thêm {len(s.get('added',[]))} con", TEXT)
            elif algo == 5:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (độ sâu d={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [IDS, giới hạn l={s['limit']}]: Lấy ra trạng thái ở độ sâu d = <b>{s['depth']}</b> (nước đi <b>'{via_vn}'</b>). "
                       f"Mở rộng thêm <b>{len(s.get('added',[]))}</b> trạng thái con vào ngăn xếp (stack): {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Mở rộng độ sâu d={s['depth']}/{s['limit']} (hướng {via_vn}) ➔ Thêm {len(s.get('added',[]))} con", TEXT)
            elif algo == 6:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (độ sâu d={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [BFS]: Lấy ra trạng thái đầu hàng đợi (nước đi <b>'{via_vn}'</b>, độ sâu d = <b>{s['depth']}</b>). "
                       f"Mở rộng thêm <b>{len(s.get('added',[]))}</b> trạng thái con vào hàng đợi (queue): {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Mở rộng (hướng {via_vn}, độ sâu d={s['depth']}) ➔ Thêm {len(s.get('added',[]))} con vào queue", TEXT)
            else:
                added_str = ", ".join([f"hướng {dir_names.get(d, d)} (độ sâu d={c})" for _,d,c in s.get('added',[])]) or "không có"
                msg = (f"<b>Bước {idx+1}</b> [DFS]: Lấy ra trạng thái đỉnh ngăn xếp (nước đi <b>'{via_vn}'</b>, độ sâu d = <b>{s['depth']}</b>). "
                       f"Mở rộng thêm <b>{len(s.get('added',[]))}</b> trạng thái con vào ngăn xếp (stack): {added_str}.")
                self._add_log(idx, f"Bước {idx+1}: Mở rộng (hướng {via_vn}, độ sâu d={s['depth']}) ➔ Thêm {len(s.get('added',[]))} con vào stack", TEXT)

        self.info_box.setText(msg)
        self._update_stats(
            idx+1, s['cost'] if algo in (0, 1, 2, 3, 4) else (s['depth'] if algo == 5 else None), s['visited_count'], s['frontier_count'],
            s.get('iteration'), s.get('limit'),
            s.get('g') if algo in (0, 1) else None,
            s.get('h') if algo in (0, 1) else None
        )
        
        self._render_frontier(s['frontier'], algo, s['frontier_count'])
        self._render_explored(s.get('explored', []), s['state'], s['visited_count'])

        # highlight log
        for i in range(self.log_list.count()):
            item = self.log_list.item(i)
            if item.data(Qt.UserRole) == idx:
                self.log_list.setCurrentItem(item)
                self.log_list.scrollToItem(item)
                break

    # ── Frontier render ──────────────────────────────────────────
    def _render_frontier(self, frontier, algo, total_count):
        self._clear_panel(self.frontier_layout)
        if not frontier:
            self._panel_empty(self.frontier_layout, "Danh sách Frontier trống")
            return

        dir_names = {'↑': 'Lên ↑', '↓': 'Xuống ↓', '←': 'Trái ←', '→': 'Phải →', 'start': 'Bắt đầu'}

        if algo in (0, 1, 2, 3, 4):
            if algo == 1:
                hdr = QLabel(f"📚 {total_count} trạng thái (IDA* LIFO stack — đỉnh stack sẽ pop tiếp):")
            elif algo == 2:
                hdr = QLabel(f"📋 {total_count} trạng thái lân cận (di chuyển sang trạng thái tốt hơn đầu tiên):")
            elif algo == 3:
                hdr = QLabel(f"📋 {total_count} trạng thái lân cận (được sắp xếp, di chuyển sang tốt nhất):")
            else:
                hdr = QLabel(f"📋 {total_count} trạng thái (↑ chi phí thấp nhất = pop tiếp):")
            hdr.setStyleSheet(f"color:{TEXT_DIM};font-size:11px;")
            self.frontier_layout.addWidget(hdr)
            batch = []
            for rank, item in enumerate(frontier):
                state = item['state']
                cost = item['cost']
                d = item['via']
                if algo in (0, 1):
                    label_bot_text = f"f: {cost}={item['g']}+{item['h']}"
                elif algo in (2, 3):
                    label_bot_text = f"h = {cost}"
                else:
                    label_bot_text = f"g = {cost}"
                mini = MiniBoard(state,
                    label_top=f"Đi: {dir_names.get(d, d)}", label_bot=label_bot_text,
                    border_col=ACCENT if rank==0 else BORDER,
                    bg_col="#151B2E" if rank==0 else BG2,
                    tag_col=ACCENT2 if rank==0 else TEXT_DIM,
                    tag_txt="▲ pop tiếp" if rank==0 and algo not in (2, 3) else ("▲ chọn" if rank==0 and algo in (2, 3) else ""))
                batch.append(mini)
                if len(batch)==2: self._add_mini_row(self.frontier_layout, batch); batch=[]
            if batch: self._add_mini_row(self.frontier_layout, batch)
            if total_count > 16:
                self.frontier_layout.addWidget(self._more_lbl(total_count - 16))
        elif algo in (5, 7):
            algo_type = "IDS LIFO stack" if algo == 5 else "DFS LIFO stack"
            hdr = QLabel(f"📚 {total_count} trạng thái ({algo_type} — đỉnh stack sẽ pop tiếp):")
            hdr.setStyleSheet(f"color:{TEXT_DIM};font-size:11px;")
            self.frontier_layout.addWidget(hdr)
            batch = []
            for rank, item in enumerate(frontier):
                state = item['state']
                d = item['via']
                depth = item.get('depth', 0)
                mini = MiniBoard(state,
                    label_top=f"Đi: {dir_names.get(d, d)}", label_bot=f"Độ sâu: {depth}",
                    border_col=TEAL if rank==0 else BORDER,
                    bg_col="#0A1E1E" if rank==0 else BG2,
                    tag_col=TEAL if rank==0 else TEXT_DIM,
                    tag_txt="▲ pop tiếp" if rank==0 else "")
                batch.append(mini)
                if len(batch)==2: self._add_mini_row(self.frontier_layout, batch); batch=[]
            if batch: self._add_mini_row(self.frontier_layout, batch)
            if total_count > 12:
                self.frontier_layout.addWidget(self._more_lbl(total_count - 12))
        else:
            hdr = QLabel(f"📋 {total_count} trạng thái (BFS FIFO queue — đầu queue sẽ pop tiếp):")
            hdr.setStyleSheet(f"color:{TEXT_DIM};font-size:11px;")
            self.frontier_layout.addWidget(hdr)
            batch = []
            for rank, item in enumerate(frontier):
                state = item['state']
                d = item['via']
                depth = item.get('depth', 0)
                mini = MiniBoard(state,
                    label_top=f"Đi: {dir_names.get(d, d)}", label_bot=f"Độ sâu: {depth}",
                    border_col=TEAL if rank==0 else BORDER,
                    bg_col="#0A1E1E" if rank==0 else BG2,
                    tag_col=TEAL if rank==0 else TEXT_DIM,
                    tag_txt="▲ pop tiếp" if rank==0 else "")
                batch.append(mini)
                if len(batch)==2: self._add_mini_row(self.frontier_layout, batch); batch=[]
            if batch: self._add_mini_row(self.frontier_layout, batch)
            if total_count > 12:
                self.frontier_layout.addWidget(self._more_lbl(total_count - 12))

    # ── Explored render ──────────────────────────────────────────
    def _render_explored(self, explored, current_state, total_count):
        self._clear_panel(self.explored_layout)
        if not explored:
            self._panel_empty(self.explored_layout, "Chưa có trạng thái nào được xét (Explored trống)")
            return
        hdr = QLabel(f"✅ {total_count} trạng thái đã xét (mới nhất trước):")
        hdr.setStyleSheet(f"color:{PURPLE};font-size:11px;")
        self.explored_layout.addWidget(hdr)
        show = list(reversed(explored))
        batch = []
        algo = self.algo_combo.currentIndex()
        dir_names = {'↑': 'Lên ↑', '↓': 'Xuống ↓', '←': 'Trái ←', '→': 'Phải →', 'start': 'Bắt đầu'}
        for item in show:
            state = item[0]
            cost_or_depth = item[1]
            d = item[2]
            is_cur = (state == current_state)
            if algo in (0, 1):
                g = item[3]
                h = item[4]
                lbl_bot = f"f: {cost_or_depth}={g}+{h}"
            elif algo in (2, 3):
                lbl_bot = f"h = {cost_or_depth}"
            elif algo == 4:
                lbl_bot = f"Chi phí: {cost_or_depth}"
            else:
                lbl_bot = f"Độ sâu: {cost_or_depth}"
            mini = MiniBoard(state,
                label_top=f"Đi: {dir_names.get(d, d)}", label_bot=lbl_bot,
                border_col=ORANGE if is_cur else PURPLE,
                bg_col="#1E1A0A" if is_cur else PURPLE_BG,
                tag_col=ORANGE if is_cur else PURPLE,
                tag_txt="◀ vừa xét" if is_cur else "")
            batch.append(mini)
            if len(batch)==2: self._add_mini_row(self.explored_layout, batch); batch=[]
        if batch: self._add_mini_row(self.explored_layout, batch)
        if total_count > 12:
            self.explored_layout.addWidget(self._more_lbl(total_count - 12))

    # ── Helpers ─────────────────────────────────────────────────
    def _add_mini_row(self, layout, widgets):
        row = QWidget(); row.setStyleSheet("background:transparent;")
        hl = QHBoxLayout(row); hl.setContentsMargins(0,0,0,0); hl.setSpacing(6)
        for w in widgets: hl.addWidget(w)
        hl.addStretch()
        layout.addWidget(row)

    def _clear_panel(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def _panel_empty(self, layout, txt):
        lbl = QLabel(txt)
        lbl.setStyleSheet(f"color:{TEXT_DIM};font-size:12px;padding:10px;")
        layout.addWidget(lbl)

    def _more_lbl(self, n):
        lbl = QLabel(f"... và {n} trạng thái khác")
        lbl.setStyleSheet(f"color:{TEXT_DIM};font-size:11px;padding:4px;")
        return lbl

    def _add_log(self, idx, text, color=TEXT):
        # tránh duplicate khi navigate back/forward
        for i in range(self.log_list.count()):
            if self.log_list.item(i).data(Qt.UserRole) == idx:
                return
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, idx)
        item.setForeground(QColor(color))
        self.log_list.addItem(item)
        self.log_list.scrollToBottom()

    def _update_stats(self, step, cost, visited, frontier, iteration, limit, g=None, h=None):
        self.lbl_step.setText(str(step))
        if g is not None and h is not None:
            self.lbl_cost.setText(f"{cost} = {g} + {h}")
        else:
            self.lbl_cost.setText(str(cost) if cost is not None else "—")
        self.lbl_visited.setText(str(visited))
        self.lbl_frontier.setText(str(frontier))
        self.lbl_iter.setText(str(iteration) if iteration is not None else "—")
        self.lbl_limit.setText(str(limit) if limit is not None else "—")
