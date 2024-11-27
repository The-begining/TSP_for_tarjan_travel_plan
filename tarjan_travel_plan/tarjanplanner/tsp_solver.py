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

def validate_tsp_path(graph, tsp_path):
    """
    Validates the TSP path to ensure it visits each node once.
    
    Parameters:
        graph (nx.Graph): The graph used for TSP.
        tsp_path (list): The TSP path to validate.

    Raises:
        ValueError: If the path is invalid.
    """
    unique_nodes = set(tsp_path[:-1])  # Exclude the last node (should be the same as the first)
    if len(unique_nodes) != len(graph.nodes):
        raise ValueError("TSP path does not visit all nodes exactly once.")
    if tsp_path[0] != tsp_path[-1]:
        raise ValueError("TSP path does not form a cycle.")

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
        tsp_path = tsp(graph, cycle=True)  # Returns an approximate solution

        # Remove redundancy
        def remove_redundancy(path):
            seen = set()
            unique_path = []
            for node in path:
                if node not in seen:
                    unique_path.append(node)
                    seen.add(node)
            return unique_path

        tsp_path = remove_redundancy(tsp_path)

        # Ensure the cycle is complete
        if tsp_path[0] != tsp_path[-1]:
            tsp_path.append(tsp_path[0])

        # Validate path
        validate_tsp_path(graph, tsp_path)

        # Calculate length
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
                raise ValueError("Disconnected graph: Unable to find unvisited neighbors.")
            
            path.append(nearest_node)
            visited.add(nearest_node)
            current_node = nearest_node

        # Return to the start node to complete the cycle
        path.append(start_node)
        tsp_length = sum(graph[u][v]["weight"] for u, v in zip(path, path[1:]))
        return path, tsp_length


   