import logging
import re
import os
from fileorganizer.file_manager import FileManager
from fileorganizer.file_classifier import FileClassifier
from tarjanplanner.graph_builder import GraphBuilder
from tarjanplanner.tsp_solver import TSPSolver
#from tarjanplanner.tsp_solver import validate_graph
from tarjanplanner.visualizer import Visualizer
from tarjanplanner.decorators import log_execution, validate_input
from tarjanplanner.errors import InvalidInputError, FileNotFoundError, NetworkError


def validate_input_regex(input_value, pattern, error_message):
    """
    Validates input using the provided regex pattern.
    Raises a ValueError if the input does not match the pattern.
    """
    if not re.match(pattern, input_value):
        raise ValueError(error_message)
    return input_value

def filter_nodes(graph, tsp_path):
    """
    Filter out nodes that are not part of the TSP path.
    """
    tsp_nodes = set(tsp_path)
    return graph.subgraph(tsp_nodes).copy()


def main():
    try:
        # Initialize FileManager for output handling
        file_manager = FileManager(base_dir="outputs")
        file_manager.setup_logging()
        
        # Initial message
        print("Starting TarjanPlanner...")
        logging.info("Starting TarjanPlanner...")

        # Get optimization type
        optimization_type = input(
            "Choose optimization type ('single', 'mixed-time', 'mixed-cost', 'balanced'): "
        ).strip().lower()
        optimization_type = validate_input_regex(
            optimization_type,
            r"^(single|mixed-time|mixed-cost|balanced)$",
            "Invalid optimization type! Must be one of: single, mixed-time, mixed-cost, balanced.",
        )

        #If 'single', ask for transport mode
        if optimization_type == "single":
            transport_mode = input(
                "Select transport mode (Bus, Train, Bicycle, Walking): "
            ).strip().capitalize()
            transport_mode = validate_input_regex(
                transport_mode,
                r"^(Bus|Train|Bicycle|Walking)$",
                "Invalid transport mode! Must be one of: Bus, Train, Bicycle, Walking.",
            )
            logging.info(f"Selected transport mode: {transport_mode}")

        #Define data
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

        transport_modes = {
            "Bus": {"speed_kmh": 40, "cost_per_km": 2, "transfer_time_min": 5},
            "Train": {"speed_kmh": 80, "cost_per_km": 5, "transfer_time_min": 2},
            "Bicycle": {"speed_kmh": 15, "cost_per_km": 0, "transfer_time_min": 1},
            "Walking": {"speed_kmh": 5, "cost_per_km": 0, "transfer_time_min": 0},
        }

        # Build the graph
        builder = GraphBuilder(relatives, transport_modes)
        logging.info("Building graph...")
        graph = builder.build_graph()
        logging.info("Graph built and validated successfully!")

        # Apply optimization logic
        if optimization_type == "single":
            builder.apply_criteria("time", transport_mode=transport_mode)
        elif optimization_type == "mixed-time":
            builder.apply_criteria_with_thresholds(optimize_by="time")
        elif optimization_type == "mixed-cost":
            builder.apply_criteria_with_thresholds(optimize_by="cost")
        elif optimization_type == "balanced":
            w_time = 0.7
            w_cost = 0.3
            builder.apply_criteria("mixed", w_time=w_time, w_cost=w_cost)

        logging.info(f"Optimization type applied: {optimization_type}")

        # Select the TSP algorithm
        tsp_algorithm = input(
            "Choose TSP solving method ('approximation', 'greedy','evolutionary'): "
        ).strip().lower()
        tsp_algorithm = validate_input_regex(
            tsp_algorithm,
            r"^(approximation|greedy)$",
            "Invalid TSP solving method! Must be one of: approximation, greedy.",
        )
        logging.info(f"Selected TSP algorithm: {tsp_algorithm}")

        # Solve the TSP
        solver = TSPSolver()
        logging.info("Solving TSP...")
        tsp_path, tsp_length = solver.solve_tsp(graph, method=tsp_algorithm)
        logging.info(f"TSP Path: {tsp_path}")
        logging.info(f"Total Travel Length: {tsp_length:.2f}")

        # Filter the graph to include only nodes in the TSP path
        filtered_graph = filter_nodes(graph, tsp_path)

        # Save the transport mode on the nodes
        builder.save_mode_on_nodes()
        
        # Calculate total time and cost for the path
        total_time = 0
        total_cost = 0
        for i in range(len(tsp_path) - 1):
            u, v = tsp_path[i], tsp_path[i + 1]
            edge_data = graph[u][v]
            total_time += edge_data.get("time", 0)
            total_cost += edge_data.get("cost", 0)

        # Output results
        print(f"\nOptimal Path: {tsp_path}")
        print(f"Total Travel Length: {tsp_length:.2f}")
        print(f"Total Travel Time: {total_time:.2f} minutes")
        print(f"Total Travel Cost: {total_cost:.2f} currency units")

        logging.info(f"Total Travel Time: {total_time:.2f} minutes")
        logging.info(f"Total Travel Cost: {total_cost:.2f} currency units")

        def sanitize_filename(title):
            return re.sub(r'[<>:"/\\|?*]', '_', title)
        # Visualize the graph
        if optimization_type == "single":
            graph_title = f"TSP Path (Single Mode - {transport_mode})"
        elif optimization_type in ["mixed-time", "mixed-cost"]:
            graph_title = f"TSP Path Optimized by {'Time' if optimization_type == 'mixed-time' else 'Cost'}"
        else:
            graph_title = "TSP Path (Balanced - Time and Cost)"
        
        graph_title = f"{graph_title} - Algorithm: {tsp_algorithm}"
        Visualizer.plot_graph(graph, tsp_path, title=graph_title)
        
        
        sanitized_title = sanitize_filename(graph_title)
        filename = f"{sanitized_title}.png"
        
        file_manager.save_graph(graph, tsp_path, filename=filename)
                

        # Organize files
        classifier = FileClassifier(base_dir="outputs")
        dest_dirs = {
            ".log": file_manager.log_dir,
            ".png": file_manager.graph_dir,
            ".txt": "outputs/documents",
        }
        classifier.classify_files(dest_dirs)

    except InvalidInputError as e:
        logging.error(e)
        print(f"Invalid input: {e}")
    except FileNotFoundError as e:
        logging.error(e)
        print(f"File not found: {e}")
    except NetworkError as e:
        logging.error(e)
        print(f"Network error: {e}")
    except ValueError as e:
        logging.error(e)
        print(f"Validation error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
