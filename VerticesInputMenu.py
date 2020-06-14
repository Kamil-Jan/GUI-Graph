import re
import logging
from PageWindow import PageWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
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
    def __init__(self, controller):
        logging.debug("VerticesInputUI initialization")
        super().__init__()
        self.setFixedSize(200, 100)

        self.controller = controller

        layoutFont = QFont("Arial", 10, QFont.Bold)
        self.__generalLayout = QVBoxLayout()
        self.__centralWidget = QWidget(self)
        self.__centralWidget.setLayout(self.__generalLayout)
        self.__centralWidget.setFont(layoutFont)
        self.setCentralWidget(self.__centralWidget)

        self.createView()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def createView(self):
        """
        Creates widgets of VerticesInputUI.
        """
        logging.debug("VerticesInputUI.createView function started")
        verticesFormLayout = QFormLayout()
        bottomLayout = QHBoxLayout()

        # Top widgets.
        self.verticesInputLine = QLineEdit()
        self.verticesInputLine.setFixedHeight(25)
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
                                           font-size: 10pt;
                                           font-family: Arial""")
        bottomLayout.addWidget(self.__errorLabel)

        self.OkButton = QPushButton("Ok")
        self.OkButton.setFixedWidth(50)
        self.OkButton.clicked.connect(self.gotoTableUI)
        bottomLayout.addWidget(self.OkButton)
        self.__generalLayout.addLayout(bottomLayout)
        logging.debug("VerticesInputUI.createView function ended\n")

    def clearDisplay(self):
        logging.debug("VerticesInputUI.clearDisplay function started")
        self.verticesInputLine.setText("")
        self.isDirectedRButton.setChecked(False)
        logging.debug("VerticesInputUI.clearDisplay function ended\n")

    def createDisplay(self):
        pass

    def isDirected(self):
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
            self.controller.model.directed = self.isDirected()
            self.controller.addVerticesToGraph(verticesList)
            self.clearDisplay()
            self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.goto("GraphTable")
            logging.debug("VerticesInputUI.gotoTableUI function ended\n")

    def __clearErrorInfo(self):
        self.verticesInputLine.setStyleSheet("""font: bold;
                                                font-size: 10pt;
                                                font-family: Arial
                                                """)
        self.__errorLabel.setText("")

    def __drawErrorInfo(self):
        self.verticesInputLine.setStyleSheet("border: 1px solid red;")
        self.__errorLabel.setText("Invalid input!")

