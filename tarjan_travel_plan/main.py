from tarjanplanner.graph_builder import GraphBuilder
from tarjanplanner.tsp_solver import TSPSolver
from tarjanplanner.visualizer import Visualizer
from geopy.distance import geodesic

# Data for relatives
relatives = {
    "Relative_1": {"lat": 37.4979, "lon": 127.0276},
    "Relative_2": {"lat": 37.4833, "lon": 127.0322},
    "Relative_3": {"lat": 37.5172, "lon": 127.0286},
    "Relative_4": {"lat": 37.5219, "lon": 127.0411},
    "Relative_5": {"lat": 37.5340, "lon": 127.0026},
    "Relative_6": {"lat": 37.5443, "lon": 127.0557},
    "Relative_7": {"lat": 37.5172, "lon": 127.0391},
    "Relative_8": {"lat": 37.5800, "lon": 126.9844},
    "Relative_9": {"lat": 37.5110, "lon": 127.0590},
    "Relative_10": {"lat": 37.5133, "lon": 127.1028},
}

# Transport modes
transport_modes = {
    "Bus": {"speed_kmh": 40, "cost_per_km": 2, "transfer_time_min": 5},
    "Train": {"speed_kmh": 80, "cost_per_km": 5, "transfer_time_min": 2},
    "Bicycle": {"speed_kmh": 15, "cost_per_km": 0, "transfer_time_min": 1},
    "Walking": {"speed_kmh": 5, "cost_per_km": 0, "transfer_time_min": 0},
}

# User selects optimization criteria
criteria = input("Optimize by 'time' or 'cost': ").strip().lower()
if criteria not in ["time", "cost"]:
    raise ValueError("Invalid input! Use 'time' or 'cost'.")

# Build the graph
builder = GraphBuilder(relatives, transport_modes)
graph = builder.build_graph()

# Connect nodes explicitly to ensure completeness
for u in graph.nodes:
    for v in graph.nodes:
        if u != v and not graph.has_edge(u, v):
            graph.add_edge(u, v, distance=geodesic(
                (relatives[u]["lat"], relatives[u]["lon"]),
                (relatives[v]["lat"], relatives[v]["lon"])
            ).kilometers)

# Apply decision rules
builder.apply_criteria_with_thresholds()

# Set the weight for optimization
for u, v, data in graph.edges(data=True):
    data["weight"] = data[criteria]

# Solve the TSP
solver = TSPSolver()
tsp_path, tsp_length = solver.solve_tsp(graph)

# Visualize the results
Visualizer.plot_graph(graph, tsp_path, title=f"TSP Path Optimized by {criteria.capitalize()}")

# Print the results
print(f"\nOptimal Path: {tsp_path}")
print(f"Total {criteria.capitalize()} Length: {tsp_length:.2f}")

# Breakdown of both time and cost
print("\nPath Breakdown (Both Time and Cost):")
total_time = 0
total_cost = 0
for i in range(len(tsp_path) - 1):
    u, v = tsp_path[i], tsp_path[i + 1]
    edge_data = graph[u][v]
    mode = edge_data["mode"]
    time = edge_data["time"]
    cost = edge_data["cost"]
    total_time += time
    total_cost += cost

    print(f"  {u} → {v}: Mode = {mode}, Time = {time:.2f} minutes, Cost = {cost:.2f} units")

print(f"\nTotal Time: {total_time:.2f} minutes")
print(f"Total Cost: {total_cost:.2f} currency units")
