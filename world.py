class World:
    # graph node(1,(lat, long))
    # edge  begin, end, weight, distance

    """
    :param vertices iterable containing all vertices in graph
    :param edges iterable containing 2-element tuple (begin_node, end_node)
    """

    def __init__(self, vertices: set, edges: iter, starting_pheromone_level=0.1, evaporation_level=0.1):
        self.vertices = vertices
        self.edges = self.create_edges(edges, pheromone_level=starting_pheromone_level)
        self.evaporation_level = evaporation_level

    def create_edges(self, edges, pheromone_level=0.1):
        new_edges = {}
        for edge in edges:
            new_edge = Edge(start=edge[0], end=edge[1], pheromone_level=pheromone_level)
            self.add_edge(new_edges, new_edge)
            new_edge = Edge(start=edge[1], end=edge[0], pheromone_level=pheromone_level)
            self.add_edge(new_edges, new_edge)
        return new_edges

    def add_edge(self, edges_dict, edge):
        if edges_dict.get(edge.begin) is None:
            edges_dict[edge.begin] = [edge]
        else:
            edges_dict[edge.begin].append(edge)

    def update_pheromone(self):
        for value in self.edges.values():
            for edge in value:
                edge.pheromone = (1 - self.evaporation_level) * edge.pheromone

    def reset_edges(self):
        for list_of_edges in self.edges.values():
            for edge in list_of_edges:
                edge.reset_pheromone()


class Edge:
    def __init__(self, start, end, pheromone_level=None, distance=1, alpha=1, beta=3, Q=1):
        self.begin = start
        self.end = end
        self.pheromone = pheromone_level
        self.basic_pheromone_level = pheromone_level
        self.distance = distance
        self.alpha = alpha
        self.beta = beta
        self.Q = Q

    def reset_pheromone(self):
        self.pheromone = self.basic_pheromone_level

    def update_pheromone(self, solution_score):
        self.pheromone += self.Q / solution_score

    @property
    def weigh(self):
        return pow(self.pheromone, self.alpha) * pow(1 / self.distance, self.beta)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.begin},{self.end}) - {self.pheromone}"
