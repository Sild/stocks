from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Only needed for access to command line arguments
import sys


# Subclass QMainWindow to customise your application's main window
class TradeAppWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(TradeAppWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Trade App")

        layout = QVBoxLayout()
        horizontal_splitter = QSplitter(Qt.Horizontal)

        horizontal_splitter.addWidget(QTableWidget(2, 4))
        horizontal_splitter.addWidget(QSlider())

        layout.addWidget(horizontal_splitter)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
