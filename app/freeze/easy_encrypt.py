import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from app.mainwin import MainWin

if __name__ == '__main__':
    # Create the application object
    app = QApplication(sys.argv)

    # Create the main window object
    window = MainWin()
    icon_path = os.path.join(os.path.dirname(__file__), os.pardir, 'resources', 'key_icon.png')
    window.setWindowIcon(QIcon('D:\\Udvikling\\EasyEncrypt\\app\\resources\\key_icon.png'))
    window.setWindowTitle('EasyEncrypt')
    # Show the main window
    window.show()

    # Run the event loop
    sys.exit(app.exec())
