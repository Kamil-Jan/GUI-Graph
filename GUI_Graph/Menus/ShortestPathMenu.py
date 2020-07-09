import logging
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel


class ShortestPathUI(QMainWindow):
    def __init__(self, controller, width, height, fontSize):
        logging.debug("ShortestPathUI initialization")
        super().__init__()
        self.setWindowTitle("Find the shortest path")

        self.controller = controller
        self.__generalLayout = QGridLayout()
        self.setFixedSize(width, height)

        self.fontSize = fontSize
        layoutFont = QFont("Arial", self.fontSize, QFont.Bold)
        self.__centralWidget = QWidget()
        self.__centralWidget.setFont(layoutFont)
        self.__centralWidget.setLayout(self.__generalLayout)
        self.setCentralWidget(self.__centralWidget)

        self.createView()

    def createView(self):
        """
        Creates widgets of ShortestPathMenu
        """
        logging.debug("ShortestPathUI.createView function started")
        formLayout = QFormLayout()

        self.fromLineEdit = QLineEdit()
        self.fromLineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                      self.fromLineEdit))
        formLayout.addRow("From: ", self.fromLineEdit)

        self.toLineEdit = QLineEdit()
        self.toLineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                    self.toLineEdit))
        formLayout.addRow("To: ", self.toLineEdit)

        self.pathLineEdit = QLineEdit()
        self.pathLineEdit.setReadOnly(True)
        formLayout.addRow("Path: ", self.pathLineEdit)

        self.lengthLabel = QLabel()
        formLayout.addRow("Length: ", self.lengthLabel)
        self.__generalLayout.addLayout(formLayout, 0, 0)

        self.OkButton = QPushButton("Ok")
        self.OkButton.setFixedWidth(50)
        self.OkButton.clicked.connect(self.updatePath)
        self.__generalLayout.addWidget(self.OkButton, 0, 1, alignment=Qt.AlignTop)

        logging.debug("ShortestPathUI.createView function ended\n")

    def clearView(self):
        """
        Clears text from Line Edit widgets.
        """
        logging.debug("ShortestPathUI.clearView function started")
        self.fromLineEdit.setText("")
        self.toLineEdit.setText("")
        self.pathLineEdit.setText("")
        self.lengthLabel.setText("")
        logging.debug("ShortestPathUI.clearView function ended\n")

    def updatePath(self):
        """
        Updates path and length widgets.
        """
        logging.debug("ShortestPathUI.updatePath function started")
        error = False
        fromVertex = self.fromLineEdit.text()
        toVertex = self.toLineEdit.text()
        graphVertices = self.controller.getVertices()
        if fromVertex not in graphVertices:
            self.__drawErrorInfo(self.fromLineEdit)
            error = True
        if toVertex not in graphVertices:
            self.__drawErrorInfo(self.toLineEdit)
            error = True
        if not error:
            self.pathLineEdit.setText("")
            self.lengthLabel.setText("")
            path, length = self.controller.calculateShortestPath(fromVertex, toVertex)
            path = " -- ".join(path)
            self.pathLineEdit.setText(f"{path}")
            self.lengthLabel.setText(f"{length}")

        logging.debug("ShortestPathUI.updatePath function ended\n")

    def closeEvent(self, event):
        self.clearView()
        self.__clearErrorInfo(self.fromLineEdit)
        self.__clearErrorInfo(self.toLineEdit)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.updatePath()

    def __drawErrorInfo(self, widget):
        widget.setStyleSheet(f"""border: 1px solid red;
                                 font-size: {self.fontSize}pt;
                                 font-family: Arial""")

    def __clearErrorInfo(self, widget):
        widget.setStyleSheet(f"""font: bold;
                                 font-size: {self.fontSize}pt;
                                 font-family: Arial""")

