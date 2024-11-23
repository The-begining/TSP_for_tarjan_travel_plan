from networkx.algorithms.approximation import traveling_salesman_problem


class TSPSolver:
    @staticmethod
    def solve_tsp(graph, weight="weight"):
        tsp_path = traveling_salesman_problem(graph, cycle=True, weight=weight)
        tsp_length = sum(
            graph[tsp_path[i]][tsp_path[i + 1]][weight] for i in range(len(tsp_path) - 1)
        )
        return tsp_path, tsp_length
