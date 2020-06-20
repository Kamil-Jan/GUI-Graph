import logging
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStackedWidget
from GUI_Graph.Menus.PageWindow import PageWindow
from GUI_Graph.Menus.VerticesInputMenu import VerticesInputUI
from GUI_Graph.Menus.GraphTableMenu import GraphTableUI


class MainWindow(QMainWindow):
    def __init__(self, controller):
        logging.debug("MainWindow initialization")
        super().__init__()

        self.controller = controller
        self.controller.view = self

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        self.setWindowTitle("GUI Graph")
        self.setFixedSize(self.minimumSizeHint())

        self.pages = dict()
        self.register(GraphTableUI(self.controller), "GraphTable")
        self.register(VerticesInputUI(self.controller), "VerticesInput")
        self.goto("VerticesInput")

    def register(self, page, pageName: str):
        """
        Connects gotoSignal of a page with self.goto.
        """
        self.pages[pageName] = page
        self.stackedWidget.addWidget(page)
        if isinstance(page, PageWindow):
            page.gotoSignal.connect(self.goto)

    @pyqtSlot(str)
    def goto(self, pageName: str):
        """
        Changes current page.
        """
        if pageName in self.pages:
            page = self.pages[pageName]
            page.createDisplay()
            page.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.stackedWidget.setCurrentWidget(page)
            self.stackedWidget.adjustSize()
            self.adjustSize()

