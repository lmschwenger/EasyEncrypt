from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QBrush, QPainterPath, QColor
from PyQt6.QtWidgets import QWidget


class RoundLamp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(20, 20)
        self.setMaximumSize(20, 20)

        self.color = QColor(255, 0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        # Create a circular shape using QPainterPath
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, 20, 20))
        painter.drawPath(path)

    def setGreen(self):
        self.color = QColor(0, 255, 0)
        self.update()

    def setRed(self):
        self.color = QColor(255, 0, 0)
        self.update()
