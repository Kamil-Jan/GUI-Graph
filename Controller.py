import logging
from VerticesInputMenu import VerticesInputUI


class Controller():
    def __init__(self, model):
        logging.debug("Controller initialization")
        self.view = None
        self.model = model
        self.isGraphDirected = False

    def addVerticesToGraph(self, verticesList):
        """
        Adds Vertices to Graph model.
        """
        logging.debug("Controller.addVerticesToGraph function started")
        self.model.add_vertices_from(verticesList)
        logging.debug("Controller.addVerticesToGraph function ended\n")

    def addEdgesToGraph(self, edgesList):
        """
        Adds Edges to Graph model.
        """
        logging.debug("Controller.addEdgesToGraph function started")
        self.model.remove_edges()
        for vertexFrom, vertexTo, weight in edgesList:
            self.model.add_edge(vertexFrom, vertexTo, weight)
        logging.debug("Controller.addEdgesToGraph function ended\n")

    def calculateShortestPath(self, startVertex, endVertex):
        pass


