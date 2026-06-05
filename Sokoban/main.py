import sys
import os
from PyQt5.QtWidgets import QApplication

# Đảm bảo thư mục Sokoban nằm trong sys.path để import tương đối hoạt động chính xác
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
