import networkx as nx
from geopy.distance import geodesic


class GraphBuilder:
    def __init__(self, relatives, transport_modes):
        self.relatives = relatives
        self.transport_modes = transport_modes
        self.graph = nx.Graph()

    def build_graph(self):
        # Add nodes
        for name, coords in self.relatives.items():
            self.graph.add_node(name, pos=(coords["lon"], coords["lat"]))

        # Add edges between nodes
        for node_a in self.graph.nodes:
            for node_b in self.graph.nodes:
                if node_a != node_b:
                    coord_a = (self.relatives[node_a]['lat'], self.relatives[node_a]['lon'])
                    coord_b = (self.relatives[node_b]['lat'], self.relatives[node_b]['lon'])
                    distance_km = geodesic(coord_a, coord_b).kilometers
                    self.graph.add_edge(node_a, node_b, distance=distance_km)
        return self.graph

    def apply_criteria(self, criteria="distance", transport_mode=None):
        if criteria not in ["distance", "time", "cost", "mixed"]:
            raise ValueError("Invalid criteria! Use 'distance', 'time', 'cost', or 'mixed'.")

        for u, v, data in self.graph.edges(data=True):
            distance_km = data["distance"]

            if criteria == "distance":
                data["weight"] = distance_km

            elif criteria == "time" and transport_mode:
                speed_kmh = self.transport_modes[transport_mode]["speed_kmh"]
                data["weight"] = (distance_km / speed_kmh) * 60  # Time in minutes

            elif criteria == "cost" and transport_mode:
                cost_per_km = self.transport_modes[transport_mode]["cost_per_km"]
                data["weight"] = distance_km * cost_per_km

            elif criteria == "mixed":
                best_weight = float("inf")
                best_mode = None
                best_cost = None
                best_time = None

                for mode, details in self.transport_modes.items():
                    cost = distance_km * details["cost_per_km"]
                    time = (distance_km / details["speed_kmh"]) * 60
                    combined_weight = cost + time  # Combine cost and time

                    if combined_weight < best_weight:
                        best_weight = combined_weight
                        best_mode = mode
                        best_cost = cost
                        best_time = time

                data["weight"] = best_weight
                data["mode"] = best_mode
                data["cost"] = best_cost
                data["time"] = best_time

    def apply_criteria_with_thresholds(self):
        """
        Apply weights to edges based on decision rules for transport mode selection.
        Always calculate both time and cost for reporting.
        """
        for u, v, data in self.graph.edges(data=True):
            distance_km = data["distance"]

            # Determine transport mode based on distance thresholds
            if distance_km < 1:
                mode = "Walking"
            elif 1 <= distance_km <= 3:
                mode = "Bicycle"
            elif 3 < distance_km <= 20:
                mode = "Bus"
            else:
                mode = "Train"

            # Calculate time and cost
            speed_kmh = self.transport_modes[mode]["speed_kmh"]
            cost_per_km = self.transport_modes[mode]["cost_per_km"]

            time_minutes = (distance_km / speed_kmh) * 60
            cost_units = distance_km * cost_per_km

            # Store details in the edge
            data["mode"] = mode
            data["time"] = time_minutes
            data["cost"] = cost_units
            data["weight"] = time_minutes  # Default to time for optimization


