import logging


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

    def getVertices(self):
        """
        Returns list of vertices in a Graph.
        """
        logging.debug("Controller.getVertices function started")
        logging.debug("Controller.getVertices function ended\n")
        return self.model.vertices()

    def deleteVertices(self):
        logging.debug("Controller.deleteVertices function started")
        self.model.delete_vertices()
        logging.debug("Controller.deleteVertices function ended\n")

    def addEdgesToGraph(self, edgesList):
        """
        Adds Edges to Graph model.
        """
        logging.debug("Controller.addEdgesToGraph function started")
        self.model.remove_edges()
        for vertexFrom, vertexTo, weight in edgesList:
            self.model.add_edge(vertexFrom, vertexTo, weight)
        logging.debug("Controller.addEdgesToGraph function ended\n")

    def setDirected(self, boolValue):
        """
        Sets Graph.directed to True or False.
        """
        logging.debug("Controller.setDirected function started")
        self.model.directed = boolValue
        logging.debug("Controller.setDirected function ended\n")

    def drawGraph(self):
        """
        Draws Graph.
        """
        logging.debug("Controller.drawGraph function started")
        self.model.draw()
        logging.debug("Controller.drawGraph function ended\n")

    def calculateShortestPath(self, startVertex, endVertex):
        """
        Calculates the Shortest path
        from startVertex to endVertex.
        """
        logging.debug("Controller.calculateShortestPath function started")
        logging.debug("Controller.calculateShortestPath function ended\n")
        return self.model.find_shortest_path(startVertex, endVertex)

    def calculateAllPaths(self, startVertex, endVertex,
                          ignoredVertices, includedVertices):
        logging.debug("Controller.calculateAllPaths function started")
        logging.debug("Controller.calculateAllPaths function ended\n")
        return self.model.find_all_paths(startVertex, endVertex,
                                         ignoredVertices, includedVertices)

