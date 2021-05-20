from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect, QLabel, QGridLayout, QLineEdit, QPushButton, QFrame, QWidget
from PyQt5.QtCore import Qt
from typing import Callable, Any


class SearchFrame(QFrame):
    def __init__(self, text_changed_handler: Callable[[str], Any]):
        super().__init__()
        self.search = QLineEdit()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.search)
        self.search.setPlaceholderText('Find room by owner email')
        self.setObjectName('search')

        self.search.textChanged.connect(text_changed_handler)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setOffset(5)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)
