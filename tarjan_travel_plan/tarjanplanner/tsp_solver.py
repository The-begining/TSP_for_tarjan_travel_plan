# import networkx as nx
# from networkx.algorithms.approximation import traveling_salesman_problem as tsp
# from tarjanplanner.utils import add_logging_to_methods

# @add_logging_to_methods
# class TSPSolver:
#     def solve_tsp(self, graph):
#         """
#         Solves the Traveling Salesman Problem on the provided graph.
#         """
#         if not isinstance(graph, nx.Graph):
#             raise ValueError("The provided graph is not a valid NetworkX graph.")

#         # Solve the TSP
#         tsp_path = tsp(graph, cycle=True)  # Returns an approximate solution
#         tsp_length = sum(graph[u][v]["weight"] for u, v in zip(tsp_path, tsp_path[1:]))

#         return tsp_path, tsp_length

import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem as tsp
from tarjanplanner.utils import add_logging_to_methods


@add_logging_to_methods
class TSPSolver:
    def solve_tsp(self, graph, method="greedy"):
        """
        Solves the Traveling Salesman Problem on the provided graph.
        
        Parameters:
            graph (nx.Graph): The graph to solve TSP on.
            method (str): The solving method to use ("approximation" or "greedy").
        
        Returns:
            tuple: (tsp_path, tsp_length)
        """
        if not isinstance(graph, nx.Graph):
            raise ValueError("The provided graph is not a valid NetworkX graph.")

        if method == "approximation":
            return self._solve_tsp_approximation(graph)
        elif method == "greedy":
            return self._solve_tsp_nearest_neighbor(graph)
        else:
            raise ValueError(f"Unknown method '{method}'. Use 'approximation' or 'greedy'.")

    def _solve_tsp_approximation(self, graph):
        """
        Solves TSP using NetworkX's approximation algorithm.
        
        Parameters:
            graph (nx.Graph): The graph to solve TSP on.
        
        Returns:
            tuple: (tsp_path, tsp_length)
        """
        print("approximation")
        tsp_path = tsp(graph, cycle=True)  # Returns an approximate solution
        tsp_length = sum(graph[u][v]["weight"] for u, v in zip(tsp_path, tsp_path[1:]))

        return tsp_path, tsp_length

    def _solve_tsp_nearest_neighbor(self, graph):
        """
        Solves TSP using the nearest neighbor heuristic.
        
        Parameters:
            graph (nx.Graph): The graph to solve TSP on.
        
        Returns:
            tuple: (tsp_path, tsp_length)
        """
        # Start at an arbitrary node (e.g., the first node in the graph)
        print("nearest neighbour")
        start_node = list(graph.nodes)[0]
        path = [start_node]
        current_node = start_node
        visited = {start_node}

        while len(visited) < len(graph.nodes):
            # Find the nearest unvisited neighbor
            neighbors = graph[current_node]
            nearest_node = None
            nearest_distance = float("inf")
            for neighbor, attributes in neighbors.items():
                if neighbor not in visited and attributes["weight"] < nearest_distance:
                    nearest_node = neighbor
                    nearest_distance = attributes["weight"]

            if nearest_node is None:
                break  # No unvisited neighbors left
            path.append(nearest_node)
            visited.add(nearest_node)
            current_node = nearest_node

        # Return to the start node to complete the cycle
        path.append(start_node)
        tsp_length = sum(graph[u][v]["weight"] for u, v in zip(path, path[1:]))
        return path, tsp_length
