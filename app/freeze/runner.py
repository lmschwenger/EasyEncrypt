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
    window.setWindowIcon(QIcon(os.path.join(window.resource_folder, 'key_icon.png')))
    window.setWindowTitle('EasyEncrypt')
    # Show the main window
    window.show()

    # Run the event loop
    sys.exit(app.exec())
