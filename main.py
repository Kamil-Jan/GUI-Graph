import sys
import logging
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
from VerticesInputMenu import VerticesInputUI
from Controller import Controller
from Graph import Graph


def main():
    loggingFormat = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=loggingFormat, level=logging.INFO)
    app = QApplication([])
    model = Graph()
    controller = Controller(model=model)
    mainWindow = MainWindow(controller)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

