from pprint import pprint

import ant
import world


def algorithm():
    vertices = {i for i in range(0, 12)}
    edges = [(0, 10), (0, 2), (1, 2), (1, 7), (1, 10), (2, 9), (3, 4), (3, 6), (3, 11), (4, 8), (4, 10), (5, 8), (5, 10), (6, 10), (6, 11), (7, 9), (7, 11), (0, 5)]
    w = world.World(vertices, edges, 0.1)
    iterations = 200
    number_of_ants = 50
    goals = [(i, j) for i in range(0, 12) for j in range(i + 1, 12)]
    solutions = {}
    for goal in goals:
        global_best_solution = None
        ants = []

        for _ in range(0, number_of_ants):
            ants.append(ant.Ant(w, goal[0], goal[1]))

        for _ in range(0, iterations):
            for a in ants:
                # print(a.find_solution())
                a.find_solution()
            local_best_ant = ant.find_best_ant(ants)
            if local_best_ant is not None:
                if global_best_solution is None:
                    global_best_solution = local_best_ant.solution
                elif len(local_best_ant.solution) < len(global_best_solution):
                    global_best_solution = local_best_ant.solution

            w.update_pheromone()
            for a in ants:
                a.update_path()
                a.reset()
            # pprint(w.edges)
            # print(f"best solution {global_best_solution}")
        w.reset_edges()
        solutions[goal] = global_best_solution
        print(f"{goal} - {global_best_solution}")
    pprint(solutions)


if __name__ == "__main__":
    algorithm()

