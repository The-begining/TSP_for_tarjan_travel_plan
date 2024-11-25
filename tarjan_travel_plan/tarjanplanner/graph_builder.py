import logging  # Add this at the top of the file
import networkx as nx
from geopy.distance import geodesic
from tarjanplanner.utils import add_logging_to_methods

@add_logging_to_methods
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

    def apply_criteria_with_thresholds(self, optimize_by="time"):
        """
        Apply weights to edges based on decision rules for transport mode selection.
        Optimize by 'time' or 'cost'. Transfer time is included.
        """
        if optimize_by not in ["time", "cost"]:
            raise ValueError("Invalid optimization criteria! Use 'time' or 'cost'.")

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

            # Calculate time and cost (including transfer time)
            speed_kmh = self.transport_modes[mode]["speed_kmh"]
            cost_per_km = self.transport_modes[mode]["cost_per_km"]
            transfer_time_min = self.transport_modes[mode]["transfer_time_min"]

            time_minutes = (distance_km / speed_kmh) * 60 + transfer_time_min
            cost_units = distance_km * cost_per_km

            # Store details in the edge
            data["mode"] = mode
            data["time"] = time_minutes
            data["cost"] = cost_units
            data["weight"] = time_minutes if optimize_by == "time" else cost_units

            # Log the decision
            logging.info(
                f"{u} -> {v}: Distance = {distance_km:.2f} km, Mode = {mode}, "
                f"Time = {time_minutes:.2f} minutes, Cost = {cost_units:.2f} units"
            )

    def apply_criteria(self, criteria="distance", transport_mode=None, w_time=0.5, w_cost=0.5):
        """
        Apply weights to edges based on specific criteria (distance, time, cost, or mixed).
        If a specific transport_mode is provided, calculate weights only for that mode.
        """
        if criteria not in ["distance", "time", "cost", "mixed"]:
            raise ValueError("Invalid criteria! Use 'distance', 'time', 'cost', or 'mixed'.")

        for u, v, data in self.graph.edges(data=True):
            distance_km = data["distance"]

            if transport_mode:  # If a single transport mode is specified
                details = self.transport_modes[transport_mode]
                speed_kmh = details["speed_kmh"]
                cost_per_km = details["cost_per_km"]
                transfer_time_min = details["transfer_time_min"]

                # Calculate time and cost for the specified mode
                time = (distance_km / speed_kmh) * 60 + transfer_time_min
                cost = distance_km * cost_per_km

                data["mode"] = transport_mode
                data["time"] = time
                data["cost"] = cost
                data["weight"] = time if criteria == "time" else cost

            elif criteria == "distance":
                data["weight"] = distance_km

            elif criteria == "time":
                # Choose the fastest mode for this edge
                best_time = float("inf")
                for mode, details in self.transport_modes.items():
                    speed_kmh = details["speed_kmh"]
                    transfer_time_min = details["transfer_time_min"]
                    time = (distance_km / speed_kmh) * 60 + transfer_time_min
                    if time < best_time:
                        best_time = time
                        data["mode"] = mode
                data["weight"] = best_time
                data["time"] = best_time

            elif criteria == "cost":
                # Choose the cheapest mode for this edge
                best_cost = float("inf")
                for mode, details in self.transport_modes.items():
                    cost = distance_km * details["cost_per_km"]
                    if cost < best_cost:
                        best_cost = cost
                        data["mode"] = mode
                data["weight"] = best_cost
                data["cost"] = best_cost

            elif criteria == "mixed":
                # Precompute max time and cost for normalization
                best_combined = float("inf")
                max_time = max((distance_km / details["speed_kmh"]) * 60 + details["transfer_time_min"]
                            for mode, details in self.transport_modes.items())
                max_cost = max(distance_km * details["cost_per_km"]
                            for mode, details in self.transport_modes.items())

                for mode, details in self.transport_modes.items():
                    cost = distance_km * details["cost_per_km"]
                    time = (distance_km / details["speed_kmh"]) * 60 + details["transfer_time_min"]

                    # Normalize time and cost
                    normalized_time = time / max_time
                    normalized_cost = cost / max_cost

                    # Weighted combination
                    combined_weight = w_time * normalized_time + w_cost * normalized_cost
                    if combined_weight < best_combined:
                        best_combined = combined_weight
                        data["mode"] = mode
                        data["cost"] = cost
                        data["time"] = time
                data["weight"] = best_combined


            # Log the applied criteria
            logging.info(
                f"{u} -> {v}: Distance = {distance_km:.2f} km, Mode = {data.get('mode', 'N/A')}, "
                f"Time = {data.get('time', 0):.2f} minutes, Cost = {data.get('cost', 0):.2f} units"
            )
