from PyQt6.QtWidgets import QApplication
import sys
from TempusPugnus.gui.main_window import TimeFistGUI

def main():
    app = QApplication(sys.argv)
    gui = TimeFistGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 