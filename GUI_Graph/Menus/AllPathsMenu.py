import re
import logging
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel


class AllPathsUI(QMainWindow):
    def __init__(self, controller, width, height, fontSize):
        logging.debug("AllPathsUI initialization")
        super().__init__()
        self.setWindowTitle("Find all paths")

        self.controller = controller
        self.__generalLayout = QGridLayout()
        self.setFixedSize(width, height) # 300, 200

        self.fontSize = fontSize
        layoutFont = QFont("Arial", self.fontSize, QFont.Bold)
        self.__centralWidget = QWidget()
        self.__centralWidget.setFont(layoutFont)
        self.__centralWidget.setLayout(self.__generalLayout)
        self.setCentralWidget(self.__centralWidget)

        self.createView()

    def createView(self):
        """
        Creates widgets of AllPathsMenu
        """
        logging.debug("AllPathsUI.createView function started")
        formLayout = QFormLayout()

        self.fromLineEdit = QLineEdit()
        self.fromLineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                      self.fromLineEdit))
        formLayout.addRow("From: ", self.fromLineEdit)

        self.toLineEdit = QLineEdit()
        self.toLineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                    self.toLineEdit))
        formLayout.addRow("To: ", self.toLineEdit)

        self.ignoreLineEdit = QLineEdit()
        self.ignoreLineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                    self.ignoreLineEdit))
        formLayout.addRow("Ignore*: ", self.ignoreLineEdit)

        self.includeLineEdit = QLineEdit()
        self.includeLineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                    self.includeLineEdit))
        formLayout.addRow("Include*: ", self.includeLineEdit)

        self.pathsTextEdit = QTextEdit()
        self.pathsTextEdit.setReadOnly(True)
        self.pathsTextEdit.setFixedHeight(70)
        formLayout.addRow("Paths: ", self.pathsTextEdit)

        self.pathCountLabel = QLabel("")
        formLayout.addRow("Path count: ", self.pathCountLabel)
        self.__generalLayout.addLayout(formLayout, 0, 0)

        self.OkButton = QPushButton("Ok")
        self.OkButton.setFixedWidth(50)
        self.OkButton.clicked.connect(self.updatePaths)
        self.__generalLayout.addWidget(self.OkButton, 0, 1, alignment=Qt.AlignTop)

        logging.debug("AllPathsUI.createView function ended\n")

    def clearView(self):
        """
        Clears text from Line Edit widgets.
        """
        logging.debug("ShortestPathUI.clearView function started")
        self.fromLineEdit.setText("")
        self.toLineEdit.setText("")
        self.ignoreLineEdit.setText("")
        self.includeLineEdit.setText("")
        self.pathsTextEdit.setText("")
        self.pathCountLabel.setText("")
        logging.debug("ShortestPathUI.clearView function ended\n")

    def updatePaths(self):
        """
        Updates paths widget.
        """
        logging.debug("ShortestPathUI.updatePaths function started")
        error = False
        verticesList = self.controller.getVertices()

        fromVertex = self.fromLineEdit.text()
        if fromVertex not in verticesList:
            self.__drawErrorInfo(self.fromLineEdit)
            error = True

        toVertex = self.toLineEdit.text()
        if toVertex not in verticesList:
            self.__drawErrorInfo(self.toLineEdit)
            error = True

        ignoredVertices = self.__extractText(self.ignoreLineEdit,
                                             self.ignoreLineEdit.text(),
                                             verticesList)
        includedVertices = self.__extractText(self.includeLineEdit,
                                              self.includeLineEdit.text(),
                                              verticesList)
        if ignoredVertices == None:
            error = True
        if includedVertices == None:
            error = True

        if not error:
            paths = self.controller.calculateAllPaths(fromVertex, toVertex,
                                                      ignoredVertices, includedVertices)
            self.pathCountLabel.setText(f"{len(paths)}")
            paths = [" -- ".join(path) for path in paths]
            paths = "\n".join(paths)
            self.pathsTextEdit.setText(paths)

        logging.debug("ShortestPathUI.updatePaths function ended\n")

    def closeEvent(self, event):
        self.clearView()
        self.__clearErrorInfo(self.fromLineEdit)
        self.__clearErrorInfo(self.toLineEdit)
        self.__clearErrorInfo(self.ignoreLineEdit)
        self.__clearErrorInfo(self.includeLineEdit)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.updatePaths()

    def __extractText(self, widget, text, verticesList):
        if not text:
            return []
        else:
            text = re.sub(r"\s", "", text)
            text = text.split(",")
            for elem in text:
                if elem == "":
                    self.__drawErrorInfo(widget)
                    return
                if elem not in verticesList:
                    self.__drawErrorInfo(widget)
                    return
            return text

    def __drawErrorInfo(self, widget):
        widget.setStyleSheet(f"""border: 1px solid red;
                                 font-size: {self.fontSize}pt;
                                 font-family: Arial""")

    def __clearErrorInfo(self, widget):
        widget.setStyleSheet(f"""font: bold;
                                 font-size: {self.fontSize}pt;
                                 font-family: Arial""")

