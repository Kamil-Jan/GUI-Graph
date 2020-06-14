import random
from Heap import MinHeap
from collections import deque


class Vertex(object):
    def __init__(self, id, val=None):
        self.id = id
        self.val = val
        self.adjacent = dict()

    def add_neighbor(self, neighbour, weight=1):
        self.adjacent[neighbour] = weight

    def get_connections(self):
        return list(self.adjacent.keys())

    def get_weighted_connections(self):
        return list(self.adjacent.items())

    def get_weight(self, neighbour):
        return self.adjacent[neighbour]

    def __str__(self):
        string = f"Vertex: id={self.id}, val={self.val}"
        return string


class Graph(object):
    def __init__(self, graph_dict=None, directed=False, weighted=False):
        self.__graph_dict = dict()
        self.directed = directed
        self.weighted = weighted
        if graph_dict:
            self.__generate_dict(graph_dict)

    def vertices(self):
        """
        Returns the vertices of a graph.
        """
        return list(self.__graph_dict.keys())

    def add_vertex(self, vertex, val=None):
        """
        If the vertex is not in self.__graph_dict,
        an instance of a class Vertex is added to the dictionary.
        Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            new_vertex = Vertex(vertex, val)
            self.__graph_dict[vertex] = new_vertex
            return vertex

    def add_vertices_from(self, vertices_list):
        for vertex in vertices_list:
            self.add_vertex(vertex)

    def get_vertex(self, vertex):
        """
        Returns Vertex class instance of a given vertex.
        """
        if vertex in self.__graph_dict:
            return self.__graph_dict[vertex]

    def delete_vertices(self):
        self.__graph_dict = dict()

    def edges(self):
        """
        Returns the edges of a graph.
        """
        return self.__generate_edges()

    def add_edge(self, frm, to, weight=1):
        """
        Adds an edge into a graph.
        """
        if frm not in self.__graph_dict:
            frm = self.add_vertex(frm)
        if to not in self.__graph_dict:
            to = self.add_vertex(to)

        self.__graph_dict[frm].add_neighbor(to, weight)
        if not self.directed:
            self.__graph_dict[to].add_neighbor(frm, weight)

    def remove_edges(self):
        for vertex in self.__graph_dict.values():
            vertex.adjacent = dict()

    def find_all_paths(self, start, end, path=[]):
        """
        Finds all possible paths from 'start' to 'end'.
        """
        path = path + [start]
        if start == end:
            return [path]
        if not self.__graph_dict[start]:
            return []
        paths = []
        for node in self.__graph_dict[start].get_connections():
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_all_paths_except(self, start, end, ignore, path=[]):
        """
        Finds all possible paths from 'start' to 'end' except a given vertex.
        """
        path = path + [start]
        if start == end:
            return [path]
        if not self.__graph_dict[start]:
            return []
        paths = []
        for node in self.__graph_dict[start].get_connections():
            if node not in path and node != ignore:
                newpaths = self.find_all_paths_except(node, end, ignore, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_all_paths_include(self, start, end, include):
        """
        Finds all possible paths from 'start' to 'end'
        going through a given vertex.
        """
        paths = self.find_all_paths(start, end)
        for key, path in enumerate(paths):
            if include not in path:
                del paths[key]
        return paths

    def find_shortest_path(self, start, end):
        """
        Finds shortest path from 'start' to 'end'
        using Dijkstra algorithm. May not work with
        negative weight edges.
        """
        inf = float("inf")
        # Function with compares distances of two Vertices.
        com_func = lambda x, y: distances[x.id][0] < distances[y.id][0]

        # Creates dictionary which contains vertex's distance and previous
        # vertex.
        distances = {vertex: (inf, None) for vertex in self.vertices()}
        distances[start] = (0, None)
        vertices = [vertex for vertex in self.__graph_dict.values()]
        MinHeap.build(vertices, com_func)

        # Finds shortest path from 'start' to all vertices.
        while vertices:
            cur_vertex = MinHeap.extract_root(vertices, com_func)

            if distances[cur_vertex.id][0] == inf:
                break

            for neighbor, weight in cur_vertex.adjacent.items():
                alternative_rout = distances[cur_vertex.id][0] + weight
                if alternative_rout < distances[neighbor][0]:
                    distances[neighbor] = (alternative_rout, cur_vertex.id)
            MinHeap.build(vertices, com_func)

        # Creates a shortest rout to 'end' vertex.
        path = deque()
        cur_vertex = end
        while cur_vertex:
            path.appendleft(cur_vertex)
            cur_vertex = distances[cur_vertex][1]
        return list(path), distances[end][0]

    def bellman_ford(self, start, end):
        """
        Finds shortest path from 'start' to 'end'
        using Bellman Ford algorithm. May not work with
        negative weight cycles.
        """
        # Creates dictionary which contains vertex's distance and previous
        # vertex.
        distances = {vertex: (float("inf"), None) for vertex in self.vertices()}
        distances[start] = (0, None)
        edges = self.edges()
        n = len(self.vertices())
        for _ in range(n - 1):
            change_num = 0
            for edge, weight in edges.items():
                from_vertex = edge[0]
                to_vertex = edge[1]
                new_cost = distances[from_vertex][0] + weight
                if new_cost < distances[to_vertex][0]:
                    change_num += 1
                    distances[to_vertex] = (new_cost, from_vertex)
            if change_num == 0:
                break

        # Creates a shortest rout to 'end' vertex.
        path = deque()
        cur_vertex = end
        while cur_vertex:
            path.appendleft(cur_vertex)
            cur_vertex = distances[cur_vertex][1]
        return list(path), distances[end][0]

    def __generate_dict(self, graph_dict):
        """
        Generates self.__graph_dict from 'graph_dict'.
        """
        if self.weighted:
            for vertex in graph_dict:
                self.add_vertex(vertex)
                for neighbor, weight in graph_dict[vertex]:
                    self.add_edge(vertex, neighbor, weight)
        else:
            for vertex in graph_dict:
                self.add_vertex(vertex)
                for neighbor in graph_dict[vertex]:
                    self.add_edge(vertex, neighbor)

    def __generate_edges(self):
        """
        Generates the edges of the graph.
        Edges are represented as tuples
        with one or two vertices.
        """
        edges = dict()
        for vertex in self.__graph_dict:
            for neighbour, w in self.__graph_dict[vertex].get_weighted_connections():
                edges[(vertex, neighbour)] = w
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += f"{k} "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += f"{edge} "
        return res


def main():
    g = {"A": [("B",5),("C",3)],
         "B": [("A",5),("C",1),("D",4)],
         "C": [("A",3),("B",1),("D",6)],
         "D": [("B",4),("C",6),("E",1)],
         "E": [("D",1)]}

    G = Graph(g, directed=True, weighted=True)

if __name__ == "__main__":
    main()

