import numpy as np


class Ant:
    def __init__(self, world, start_node: int, goal_node: int):
        self.solution = []
        self.used_edges = []
        self.start_node = start_node
        self.current_node = start_node
        self.destination = goal_node
        self.world = world
        self.visited_nodes = set()

    @property
    def remaining_nodes(self):
        return self.world.vertices - self.visited_nodes

    @property
    def edges_available(self):
        return [edge for edge in self.world.edges[self.current_node] if edge.end not in self.visited_nodes]

    # @property
    # def solution_without_cycles(self):
    #     if self.solution is None:
    #         return None
    #     solution = self.solution
    #     pos = len(solution) - 1
    #     while pos != 0:
    #         el = solution[pos]
    #         another_pos = solution.index(el)
    #         if another_pos != pos:
    #             solution = solution[:another_pos] + solution[pos:]
    #             self.used_edges = self.used_edges[:another_pos] + self.used_edges[pos:]
    #             pos = another_pos
    #         pos = pos - 1
    #     return solution

    def reset(self):
        self.solution = []
        self.used_edges = []
        self.current_node = self.start_node
        self.visited_nodes = set()

    def choose_edge(self):
        total_pheromones = sum(edge.weigh for edge in self.edges_available)
        probability = [edge.weigh / total_pheromones for edge in self.edges_available]
        return np.random.choice(self.edges_available, 1, p=probability)[0]

    def move(self, edge):
        if self.current_node != edge.begin:
            raise ValueError(f"Wrong edge used - current edge begin {edge.begin}, current node {self.current_node}")
        self.visited_nodes.add(self.current_node)
        self.solution.append(self.current_node)
        self.used_edges.append(edge)
        self.current_node = edge.end

    def find_solution(self):
        while self.current_node != self.destination:
            if self.edges_available:
                edge = self.choose_edge()
                self.move(edge)
            else:
                self.solution = None
                break
        return self.solution

    def update_path(self):
        if self.solution is not None:
            for edge in self.used_edges:
                edge.update_pheromone(len(self.solution))


def find_best_ant(ants):
    ants_with_solutions = [ant for ant in ants if ant.solution is not None]
    if len(ants_with_solutions) == 0:
        return None
    return min(ants_with_solutions, key=lambda ant: len(ant.solution))
