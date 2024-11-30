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
import logging

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

  # Remove redundancy
def remove_redundancy(path):
    seen = set()
    unique_path = []
    for node in path:
        if node not in seen:
            unique_path.append(node)
            seen.add(node)
    return unique_path

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
        elif method == "evolutionary":
            return self.solve_tsp_evolutionary(graph)
        else:
            raise ValueError(f"Unknown method '{method}'. Use 'approximation', 'greedy', or 'evolutionary'.")

    def _solve_tsp_approximation(self, graph):
        """
        Solves TSP using NetworkX's approximation algorithm.

        Parameters:
            graph (nx.Graph): The graph to solve TSP on.

        Returns:
            tuple: (tsp_path, tsp_length)
        """
        tsp_path = tsp(graph, cycle=True)  # Returns an approximate solution

    
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

    def solve_tsp_evolutionary(self, graph, population_size=50, generations=100):
        from deap import base, creator, tools
        import random

        def evaluate(individual):
            node_list = list(graph.nodes)
            path = [node_list[i] for i in individual]
            path.append(path[0])  # Ensure it forms a cycle

            # Penalize invalid paths
            if len(set(path[:-1])) != len(graph.nodes):
                return 1e6,  # Large penalty

            fitness = 0
            for u, v in zip(path, path[1:]):
                if graph.has_edge(u, v):
                    fitness += graph[u][v]['distance']
                else:
                    fitness += 1e6  # Heavy penalty
            return fitness,

        def repair_individual(individual, num_nodes):
            from collections import Counter
            logging.info(f"Original individual: {individual}")

            node_counts = Counter(individual)
            duplicates = [node for node, count in node_counts.items() if count > 1]
            missing_nodes = list(set(range(num_nodes)) - set(individual))
            logging.info(f"Duplicates: {duplicates}, Missing nodes: {missing_nodes}")

            repaired_individual = []
            for node in individual:
                if node_counts[node] > 1:
                    if missing_nodes:
                        repaired_individual.append(missing_nodes.pop())
                        node_counts[node] -= 1
                    else:
                        repaired_individual.append(node)
                else:
                    repaired_individual.append(node)

            logging.info(f"Repaired individual: {repaired_individual}")
            assert len(set(repaired_individual)) == num_nodes, "Repaired individual is invalid."
            return repaired_individual


        # DEAP setup
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()
        toolbox.register("indices", random.sample, range(len(graph.nodes)), len(graph.nodes))
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        pop = toolbox.population(n=population_size)
        for gen in range(generations):
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < 0.2:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

                # Repair invalid individuals
                if len(set(mutant)) != len(graph.nodes):
                    mutant[:] = repair_individual(mutant, len(graph.nodes))



            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            pop[:] = offspring

        best = tools.selBest(pop, 1)[0]
        tsp_path = [list(graph.nodes)[i] for i in best]
        tsp_path = repair_individual(tsp_path, len(graph.nodes))  # Ensure it's valid
        tsp_length = evaluate(best)[0]

        return tsp_path, tsp_length
