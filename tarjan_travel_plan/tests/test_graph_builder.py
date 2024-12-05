import pytest
from tarjan_travel_plan.tarjanplanner.graph_builder import GraphBuilder

@pytest.fixture
def sample_data():
    relatives = {
        "A": {"lat": 0, "lon": 0},
        "B": {"lat": 1, "lon": 1},
    }
    transport_modes = {
        "Bus": {"speed_kmh": 40, "cost_per_km": 2, "transfer_time_min": 5},
        "Train": {"speed_kmh": 80, "cost_per_km": 5, "transfer_time_min": 2},
    }
    return relatives, transport_modes

def test_graph_building(sample_data):
    relatives, transport_modes = sample_data
    builder = GraphBuilder(relatives, transport_modes)
    graph = builder.build_graph()

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert graph["A"]["B"]["distance"] > 0

def test_criteria_with_thresholds(sample_data):
    relatives, transport_modes = sample_data
    builder = GraphBuilder(relatives, transport_modes)
    graph = builder.build_graph()

    builder.apply_criteria_with_thresholds(optimize_by="time")
    for _, _, data in graph.edges(data=True):
        assert "mode" in data
        assert "time" in data
        assert "cost" in data
