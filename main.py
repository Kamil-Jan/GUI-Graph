import sys
import logging
from PyQt5.QtWidgets import QApplication
from GUI_Graph.MainWindow import MainWindow
from GUI_Graph.Controller import Controller
from GUI_Graph.Graph import Graph


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

