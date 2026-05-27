from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import (
    BG2, BG3, BORDER, TEXT, TEXT_DIM, ACCENT, ACCENT2, GREEN, RED, ORANGE,
    PURPLE, PURPLE_BG, TILE_OK, TILE_WRONG, TILE_EMPTY, TILE_MOVED, GOAL
)

class BoardWidget(QWidget):
    def __init__(self, title="", size=50, parent=None):
        super().__init__(parent)
        self.size_tile = size
        vl = QVBoxLayout(self)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(6)
        if title:
            lbl = QLabel(title)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color:{TEXT_DIM};font-size:11px;font-family:'Segoe UI';font-weight:bold;letter-spacing:1px;text-transform:uppercase;")
            vl.addWidget(lbl)
        gw = QWidget()
        gl = QGridLayout(gw)
        gl.setSpacing(6)
        gl.setContentsMargins(0, 0, 0, 0)
        self.cells = []
        
        # font sizing based on tile size
        font_size = 20 if size >= 60 else (14 if size >= 48 else (11 if size >= 36 else 9))
        
        for i in range(9):
            c = QLabel()
            c.setFixedSize(size, size)
            c.setAlignment(Qt.AlignCenter)
            c.setFont(QFont("Segoe UI", font_size, QFont.Bold))
            c.setStyleSheet(self._style("empty"))
            self.cells.append(c)
            gl.addWidget(c, i//3, i%3)
        vl.addWidget(gw, 0, Qt.AlignHCenter)

    def _style(self, kind):
        base = "border-radius:10px;font-family:'Segoe UI',Consolas;font-weight:bold;"
        if kind == "empty":  return base + "background:#0c0e17;border:2px dashed #2a3352;color:transparent;"
        if kind == "ok":     return base + "background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 #065f46);border:1.5px solid #34d399;color:#ffffff;"
        if kind == "wrong":  return base + "background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ef4444, stop:1 #991b1b);border:1.5px solid #f87171;color:#ffffff;"
        if kind == "moved":  return base + "background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #3730a3);border:1.5px solid #818cf8;color:#ffffff;"
        if kind == "cutoff": return base + "background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f59e0b, stop:1 #92400e);border:1.5px solid #fbbf24;color:#ffffff;"
        if kind == "cycle":  return base + "background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8b5cf6, stop:1 #5b21b6);border:1.5px solid #a78bfa;color:#ffffff;"
        return base + "background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #334155, stop:1 #1e293b);border:1.5px solid #475569;color:#f8fafc;"

    def set_state(self, state, prev=None, goal_mode=False, special=None):
        for i, v in enumerate(state):
            c = self.cells[i]
            if v == 0:
                c.setText(""); c.setStyleSheet(self._style("empty"))
            else:
                c.setText(str(v))
                if special:         c.setStyleSheet(self._style(special))
                elif goal_mode:     c.setStyleSheet(self._style("ok"))
                elif prev and prev[i] != v: c.setStyleSheet(self._style("moved"))
                elif v == GOAL[i]:  c.setStyleSheet(self._style("ok"))
                else:               c.setStyleSheet(self._style("wrong"))


class MiniBoard(QWidget):
    """Mini board cho frontier / explored panels"""
    def __init__(self, state, label_top="", label_bot="",
                 border_col=None, bg_col=None, tag_col=None, tag_txt="", parent=None):
        super().__init__(parent)
        self.setFixedWidth(112)
        border_col = border_col or BORDER
        bg_col = bg_col or BG2
        self.setStyleSheet(f"QWidget{{background:{bg_col};border:1.5px solid {border_col};border-radius:10px;}}")
        vl = QVBoxLayout(self)
        vl.setContentsMargins(6, 6, 6, 6)
        vl.setSpacing(3)
        if label_top:
            lt = QLabel(label_top)
            lt.setAlignment(Qt.AlignCenter)
            lt.setStyleSheet(f"color:{tag_col or TEXT_DIM};font-size:10px;border:none;background:transparent;font-family:'Segoe UI';font-weight:bold;")
            vl.addWidget(lt)
        gw = QWidget(); gw.setStyleSheet("background:transparent;border:none;")
        gl = QGridLayout(gw); gl.setSpacing(2); gl.setContentsMargins(0, 0, 0, 0)
        for i, v in enumerate(state):
            lbl = QLabel("" if v==0 else str(v))
            lbl.setFixedSize(26, 26); lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
            if v == 0:   lbl.setStyleSheet("background:#0c0e17;border:1px dashed #2a3352;border-radius:5px;color:transparent;")
            elif v==GOAL[i]: lbl.setStyleSheet("background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 #065f46);border-radius:5px;color:#ffffff;")
            else:        lbl.setStyleSheet("background:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ef4444, stop:1 #991b1b);border-radius:5px;color:#ffffff;")
            gl.addWidget(lbl, i//3, i%3)
        vl.addWidget(gw, 0, Qt.AlignHCenter)
        if label_bot:
            lb = QLabel(label_bot)
            lb.setAlignment(Qt.AlignCenter)
            lb.setStyleSheet(f"color:{tag_col or TEXT_DIM};font-size:10px;font-weight:bold;border:none;background:transparent;font-family:'Segoe UI';")
            vl.addWidget(lb)
        if tag_txt:
            tt = QLabel(tag_txt)
            tt.setAlignment(Qt.AlignCenter)
            tt.setStyleSheet(f"color:{tag_col or TEXT_DIM};font-size:9px;font-weight:bold;border:none;background:transparent;font-family:'Segoe UI';")
            vl.addWidget(tt)
