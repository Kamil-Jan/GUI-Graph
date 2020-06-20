import logging
from functools import partial
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from GUI_Graph.Menus.PageWindow import PageWindow
from GUI_Graph.Menus.ShortestPathMenu import ShortestPathUI
from GUI_Graph.Menus.AllPathsMenu import AllPathsUI


class GraphTableUI(PageWindow):
    def __init__(self, controller):
        logging.debug("GraphTableUI initialization")
        super().__init__()

        self.controller = controller
        self.shortestPathUI = ShortestPathUI(self.controller)
        self.allPathsUI = AllPathsUI(self.controller)

        self.__generalLayout = QGridLayout()
        self.__tableLayout = QGridLayout()
        self.__generalLayout.addLayout(self.__tableLayout, 1, 0)

        layoutFont = QFont("Arial", 10, QFont.Bold)
        self.__centralWidget = QWidget()
        self.__centralWidget.setFont(layoutFont)
        self.__centralWidget.setLayout(self.__generalLayout)
        self.setCentralWidget(self.__centralWidget)

        self.createView()
        self.createTable()
        self.__generalLayout.setSizeConstraint(self.__tableLayout.SetFixedSize)
        self.__centralWidget.adjustSize()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def createView(self):
        """
        Creates widgets of GraphTableUI.
        """
        logging.debug("GraphTableUI.createView function started")
        self.backButton = QPushButton("Back")
        self.backButton.setFixedWidth(40)
        self.backButton.clicked.connect(self.gotoVerticesInputMenu)
        self.__generalLayout.addWidget(self.backButton, 0, 0)

        bottomLayout = QHBoxLayout()
        self.OkButton = QPushButton("Ok")
        self.OkButton.setFixedWidth(40)
        self.OkButton.clicked.connect(self.generateGraphEdges)
        bottomLayout.addWidget(self.OkButton)

        self.clearButton = QPushButton("Clear")
        self.clearButton.setFixedWidth(40)
        self.clearButton.clicked.connect(self.clearTable)
        bottomLayout.addWidget(self.clearButton)

        self.drawButton = QPushButton("Draw")
        self.drawButton.setFixedWidth(40)
        self.drawButton.clicked.connect(self.controller.drawGraph)
        bottomLayout.addWidget(self.drawButton)
        self.__generalLayout.addLayout(bottomLayout, 2, 0, alignment=Qt.AlignLeft)

        functionsLayout = QVBoxLayout()
        functionsLayout.addWidget(QLabel(""))
        self.shortestPathButton = QPushButton("Find the\nshortest path")
        self.shortestPathButton.clicked.connect(self.shortestPathUI.show)
        functionsLayout.addWidget(self.shortestPathButton)

        self.allPathsButton = QPushButton("Find all paths")
        self.allPathsButton.clicked.connect(self.allPathsUI.show)
        functionsLayout.addWidget(self.allPathsButton)
        self.__generalLayout.addLayout(functionsLayout, 1, 1, alignment=Qt.AlignTop)
        logging.debug("GraphTableUI.createView function ended\n")

    def createTable(self):
        """
        Generates Table depending on numbers of vertices.
        """
        logging.debug("GraphTableUI.createTable function started")
        self.vertices = self.controller.getVertices()
        self.cellsDict = dict()
        verticesNum = len(self.vertices)
        for rowNum in range(1, verticesNum + 1):
            for colNum in range(1, verticesNum + 1):
                if colNum == 1:
                    vertexRowLabel = QLabel(self.vertices[rowNum - 1])
                    vertexColLabel = QLabel(self.vertices[rowNum - 1])
                    vertexRowLabel.setAlignment(Qt.AlignHCenter)
                    vertexColLabel.setAlignment(Qt.AlignHCenter)
                    self.__tableLayout.addWidget(vertexColLabel, 0, rowNum)
                    self.__tableLayout.addWidget(vertexRowLabel, rowNum, 0)
                    self.cellsDict[(0, rowNum)] = vertexColLabel
                    self.cellsDict[(rowNum, 0)] = vertexRowLabel
                lineEdit = QLineEdit()
                lineEdit.setFixedWidth(30)
                lineEdit.textChanged.connect(partial(self.__clearErrorInfo,
                                                     lineEdit, (rowNum, colNum)))
                lineEdit.setStyleSheet("""font: bold;
                                          font-size: 10pt;
                                          font-family: Arial""")
                if rowNum == colNum:
                    lineEdit.setReadOnly(True)
                    lineEdit.setStyleSheet("background: gray")
                self.__tableLayout.addWidget(lineEdit, rowNum, colNum)
                self.cellsDict[(rowNum, colNum)] = lineEdit

        logging.debug("GraphTableUI.createTable function ended\n")

    def removeTable(self):
        """
        Removes Table from generalLayout.
        """
        logging.debug("GraphTableUI.removeTable function started")
        for widget in self.cellsDict.values():
            self.__tableLayout.removeWidget(widget)
            widget.setParent(None)
        self.cellsDict = dict()
        self.__generalLayout.setSizeConstraint(self.__tableLayout.SetFixedSize)
        self.__centralWidget.adjustSize()
        logging.debug("GraphTableUI.removeTable function ended\n")

    def clearTable(self):
        """
        Clears a Table.
        """
        logging.debug("GraphTableUI.clearTable function started")
        for widget in self.cellsDict.values():
            if isinstance(widget, QLineEdit):
                widget.setText("")
        logging.debug("GraphTableUI.clearTable function ended\n")

    def createDisplay(self):
        """
        Creates a Table after going to Graph Table page.
        """
        logging.debug("GraphTableUI.createDisplay function started")
        self.createTable()
        logging.debug("GraphTableUI.createDisplay function ended\n")

    def getEdgesList(self):
        """
        Creates list of Edges based on a Table.
        """
        logging.debug("GraphTableUI.getEdgesList function started")
        edgesList = []
        error = False
        for gridPlace, widget in self.cellsDict.items():
            self.__clearErrorInfo(widget, gridPlace)
            if 0 in gridPlace or not widget.text():
                continue
            rowNum, colNum = gridPlace
            fromVertex = self.cellsDict[(rowNum, 0)].text()
            toVertex = self.cellsDict[(0, colNum)].text()
            try:
                weight = int(widget.text())
            except:
                self.__drawErrorInfo(widget)
                error = True
                continue
            edgesList.append((fromVertex, toVertex, weight))
        logging.debug("GraphTableUI.getEdgesList function ended\n")
        if not error:
            return edgesList

    def generateGraphEdges(self):
        """
        Makes Controller add edges to Graph.
        """
        logging.debug("GraphTableUI.generateGraphEdges function started")
        edgesList = self.getEdgesList()
        if edgesList:
            self.controller.addEdgesToGraph(edgesList)
        logging.debug("GraphTableUI.generateGraphEdges function ended\n")

    def gotoVerticesInputMenu(self):
        """
        Go to VerticesInputMenu page.
        """
        logging.debug("GraphTableUI.gotoVerticesInputMenu function started")
        self.getEdgesList()
        self.removeTable()
        self.controller.deleteVertices()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.goto("VerticesInput")
        logging.debug("GraphTableUI.gotoVerticesInputMenu function ended\n")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.generateGraphEdges()

    def __drawErrorInfo(self, widget):
        widget.setStyleSheet("""border: 1px solid red;
                                font-size: 10pt;
                                font-family: Arial""")

    def __clearErrorInfo(self, widget, gridPlace):
        if gridPlace[0] != gridPlace[1]:
            widget.setStyleSheet("""font: bold;
                                    font-size: 10pt;
                                    font-family: Arial""")

