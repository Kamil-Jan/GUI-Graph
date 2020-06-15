from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow


class PageWindow(QMainWindow):
    gotoSignal = pyqtSignal(str)

    def goto(self, pageName: str):
        self.gotoSignal.emit(pageName)

