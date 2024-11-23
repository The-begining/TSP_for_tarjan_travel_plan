import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem as tsp
from tarjanplanner.utils import add_logging_to_methods

@add_logging_to_methods
class TSPSolver:
    def solve_tsp(self, graph):
        """
        Solves the Traveling Salesman Problem on the provided graph.
        """
        if not isinstance(graph, nx.Graph):
            raise ValueError("The provided graph is not a valid NetworkX graph.")

        # Solve the TSP
        tsp_path = tsp(graph, cycle=True)  # Returns an approximate solution
        tsp_length = sum(graph[u][v]["weight"] for u, v in zip(tsp_path, tsp_path[1:]))

        return tsp_path, tsp_length
