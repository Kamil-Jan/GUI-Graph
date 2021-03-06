import re
import logging
from GUI_Graph.Menus.PageWindow import PageWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel


class VerticesInputUI(PageWindow):
    def __init__(self, controller, width, height, fontSize):
        logging.debug("VerticesInputUI initialization")
        super().__init__()
        self.setFixedSize(width, height)

        self.controller = controller

        self.fontSize = fontSize
        layoutFont = QFont("Arial", self.fontSize, QFont.Bold)
        self.__generalLayout = QVBoxLayout()
        self.__centralWidget = QWidget(self)
        self.__centralWidget.setLayout(self.__generalLayout)
        self.__centralWidget.setFont(layoutFont)
        self.setCentralWidget(self.__centralWidget)

        self.createView(buttonWidth=50)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def createView(self, buttonWidth):
        """
        Creates widgets of VerticesInputUI.
        """
        logging.debug("VerticesInputUI.createView function started")
        verticesFormLayout = QFormLayout()
        bottomLayout = QHBoxLayout()

        # Top widgets.
        self.verticesInputLine = QLineEdit()
        self.verticesInputLine.textChanged.connect(self.__clearErrorInfo)
        verticesFormLayout.addRow("Vertices: ", self.verticesInputLine)
        self.__generalLayout.addLayout(verticesFormLayout)

        # Center widgets.
        self.isDirectedRButton = QRadioButton("Directed")
        self.__generalLayout.addWidget(self.isDirectedRButton)

        # Bottom widgets.
        self.__errorLabel = QLabel("")
        self.__errorLabel.setStyleSheet("""color: red;
                                           font: bold;
                                           font-size: {self.fontSize}pt;
                                           font-family: Arial""")
        bottomLayout.addWidget(self.__errorLabel)

        self.OkButton = QPushButton("Ok")
        self.OkButton.setFixedWidth(buttonWidth)
        self.OkButton.clicked.connect(self.gotoTableUI)
        bottomLayout.addWidget(self.OkButton)
        self.__generalLayout.addLayout(bottomLayout)
        logging.debug("VerticesInputUI.createView function ended\n")

    def clearDisplay(self):
        """
        Clears text from Line Edit and unchecks
        Radio button.
        """
        logging.debug("VerticesInputUI.clearDisplay function started")
        self.verticesInputLine.setText("")
        self.isDirectedRButton.setChecked(False)
        logging.debug("VerticesInputUI.clearDisplay function ended\n")

    def createDisplay(self):
        pass

    def isDirected(self):
        """
        Returns boolean value which tells
        whether a graph directed or not.
        """
        logging.debug("VerticesInputUI.isDirected function started")
        logging.debug(f"isDirected = {self.isDirectedRButton.isChecked()}")
        logging.debug("VerticesInputUI.isDirected function ended\n")
        return self.isDirectedRButton.isChecked()

    def getVerticesList(self):
        """
        Extracts vertices from Line Edit and returns
        list with these vertices.
        """
        logging.debug("VerticesInputUI.getVerticesList function started")
        inputString = self.verticesInputLine.text()
        # Substitute spaces from string.
        inputString = re.sub(r"\s", "", inputString)
        verticesList = inputString.split(",")
        if "" in verticesList:
            logging.info(f"Invalid input - {verticesList}")
            logging.debug("VerticesInputUI.getVerticesList function ended\n")
            return self.__drawErrorInfo()
        logging.debug(f"verticesList = {verticesList}")
        logging.debug("VerticesInputUI.getVerticesList function ended\n")
        return verticesList

    def gotoTableUI(self):
        """
        Go to GraphTable page.
        """
        verticesList = self.getVerticesList()
        if verticesList:
            logging.debug("VerticesInputUI.gotoTableUI function started")
            self.controller.setDirected(self.isDirected())
            self.controller.addVerticesToGraph(verticesList)
            self.clearDisplay()
            self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.goto("GraphTable")
            logging.debug("VerticesInputUI.gotoTableUI function ended\n")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.gotoTableUI()

    def __clearErrorInfo(self):
        self.verticesInputLine.setStyleSheet(f"""font: bold;
                                                 font-size: {self.fontSize}pt;
                                                 font-family: Arial
                                                 """)
        self.__errorLabel.setText("")

    def __drawErrorInfo(self):
        self.verticesInputLine.setStyleSheet(f"""border: 1px solid red;
                                                 font-size: {self.fontSize}pt;
                                                 font-family: Arial
                                                 """)
        self.__errorLabel.setText("Invalid input!")

