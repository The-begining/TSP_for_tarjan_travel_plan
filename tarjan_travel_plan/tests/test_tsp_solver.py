import pytest
import networkx as nx
from tarjanplanner.tsp_solver import TSPSolver

def test_tsp_solver():
    graph = nx.Graph()
    graph.add_edge("A", "B", weight=10)
    graph.add_edge("B", "C", weight=15)
    graph.add_edge("C", "A", weight=20)

    solver = TSPSolver()
    tsp_path, tsp_length = solver.solve_tsp(graph)

    assert len(tsp_path) == 4  # Includes the return to the starting point
    assert tsp_length == 45   # Sum of weights
