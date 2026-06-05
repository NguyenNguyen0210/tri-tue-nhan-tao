# ─── Màu sắc Giao diện Sokoban ────────────────────────────────────
BG             = "#090B10" # Deepest dark blue-black
BG2            = "#111420" # Sleek panel background
BG3            = "#1A1E2F" # Interactive elements background
BORDER         = "#252B44" # Subtle border
ACCENT         = "#6366F1" # Indigo blue-purple
ACCENT2        = "#06B6D4" # Sky-blue / Cyan
TEXT           = "#F8FAFC" # White text
TEXT_DIM       = "#94A3B8" # Dim slate text

# Màu sắc vẽ các ô trong game Sokoban
COLOR_WALL     = "#475569" # Slate gray for wall
COLOR_FLOOR    = "#1E293B" # Darker gray-blue for empty floor
COLOR_TARGET   = "#EF4444" # Crimson red dot for target goal
COLOR_BOX      = "#D97706" # Dark amber brown for box
COLOR_BOX_OK   = "#10B981" # Emerald green for box successfully on target
COLOR_PLAYER   = "#38BDF8" # Cyan blue for player

# ─── Định nghĩa Hướng đi ──────────────────────────────────────────
# Mỗi hướng: (d_row, d_col, ký hiệu hiển thị)
DIRS = {
    "↑": (-1, 0),
    "↓": (1, 0),
    "←": (0, -1),
    "→": (0, 1)
}

# ─── Màn chơi Mẫu (Sokoban Levels) ────────────────────────────────
# Ký tự chuẩn:
# '#' : Tường (Wall)
# ' ' : Sàn trống (Floor)
# '.' : Điểm đích (Target)
# '$' : Hộp/Thùng (Box)
# '@' : Người chơi (Player)
# '*' : Hộp đã ở điểm đích (Box on Target)
# '+' : Người chơi đứng ở điểm đích (Player on Target)

LEVELS = [
    # Level 1: Rất dễ (1 Hộp, dùng để test chạy nhanh)
    [
        "######",
        "#@  .#",
        "#  $ #",
        "######"
    ],
    
    # Level 2: Dễ (2 Hộp)
    [
        "########",
        "#   .. #",
        "# @$$  #",
        "#      #",
        "########"
    ],
    
    # Level 3: Trung bình (3 Hộp)
    [
        "#######",
        "# ..  #",
        "# @$  #",
        "# $$  #",
        "#  .  #",
        "#######"
    ]
]
