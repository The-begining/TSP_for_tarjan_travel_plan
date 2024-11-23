import pytest
from tarjanplanner.graph_builder import GraphBuilder


def test_graph_builder():
    relatives = {
        "Relative_1": {"lat": 37.4979, "lon": 127.0276},
        "Relative_2": {"lat": 37.4833, "lon": 127.0322},
    }
    transport_modes = {"Bus": {"speed_kmh": 40, "cost_per_km": 2, "transfer_time_min": 5}}
    builder = GraphBuilder(relatives, transport_modes)
    graph = builder.build_graph()
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
