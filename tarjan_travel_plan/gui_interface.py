import tkinter as tk
import re
from tkinter import filedialog, messagebox
import logging
import os
from tarjan_travel_plan.fileorganizer.file_manager import FileManager
from tarjan_travel_plan.fileorganizer.file_classifier import FileClassifier
from tarjan_travel_plan.tarjanplanner.graph_builder import GraphBuilder
from tarjan_travel_plan.tarjanplanner.tsp_solver import TSPSolver
#from tarjanplanner.tsp_solver import validate_graph
from tarjan_travel_plan.tarjanplanner.visualizer import Visualizer
from tarjan_travel_plan.tarjanplanner.decorators import log_execution, validate_input
from tarjan_travel_plan.tarjanplanner.errors import InvalidInputError, FileNotFoundError, NetworkError

# Initialize logger
#logging.basicConfig(level=logging.INFO)
def organize_files(file_manager):
    """
    Organizes files in the outputs directory using FileClassifier.
    """
    logging.info("Starting file organization...")
    classifier = FileClassifier(base_dir=file_manager.base_dir)

    dest_dirs = {
    r".*\.log$": file_manager.log_dir,          # Match `.log` files
    r".*\.png$": file_manager.graph_dir,        # Match `.png` files
    r".*\.txt$": file_manager.document_dir,     # Match `.txt` files
    r".*\.csv$": file_manager.spreadsheet_dir,  # Match `.csv` files
    r".*": os.path.join(file_manager.base_dir, "others"),  # Catch-all for unmatched files
    }

    classifier.classify_files(dest_dirs)
    logging.info("File organization complete.")

def calculate_cost_and_time(graph, tsp_path):
    total_cost = 0
    total_time = 0
    for i in range(len(tsp_path) - 1):
        u, v = tsp_path[i], tsp_path[i + 1]
        if graph.has_edge(u, v):
            edge_data = graph[u][v]
            total_cost += edge_data.get("cost", 0)
            total_time += edge_data.get("time", 0)
    # Add cost and time for returning to the start
    u, v = tsp_path[-1], tsp_path[0]
    if graph.has_edge(u, v):
        edge_data = graph[u][v]
        total_cost += edge_data.get("cost", 0)
        total_time += edge_data.get("time", 0)
    return total_cost, total_time


def sanitize_filename(title):
    """
    Sanitizes the filename by replacing invalid characters.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', title)

def run_planner(optimization_type, transport_mode, tsp_algorithm):
    """
    Runs the Tarjan Planner with the selected options from the GUI.
    """
    try:
        
        # Initialize FileManager and set up logging
        file_manager = FileManager(base_dir="outputs")
        file_manager.setup_logging()

        logging.info("Tarjan Planner started.")
        # Define data
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
        graph = builder.build_graph()

        # Apply optimization logic
        if optimization_type == "single":
            builder.apply_criteria("time", transport_mode=transport_mode)
        elif optimization_type == "mixed-time":
            builder.apply_criteria_with_thresholds(optimize_by="time")
        elif optimization_type == "mixed-cost":
            builder.apply_criteria_with_thresholds(optimize_by="cost")
        elif optimization_type == "balanced":
            builder.apply_criteria("mixed", w_time=0.7, w_cost=0.3)

        # Solve the TSP
        solver = TSPSolver()
        tsp_path, tsp_length = solver.solve_tsp(graph, method=tsp_algorithm)

        # Calculate total cost and time
        total_cost, total_time = calculate_cost_and_time(graph, tsp_path)

        # Visualize and save the graph
        if optimization_type == "single":
            graph_title = f"TSP Path (Single Mode - {transport_mode})"
        elif optimization_type in ["mixed-time", "mixed-cost"]:
            graph_title = f"TSP Path Optimized by {'Time' if optimization_type == 'mixed-time' else 'Cost'}"
        else:
            graph_title = "TSP Path (Balanced - Time and Cost)"
        graph_title = f"{graph_title} - Algorithm: {tsp_algorithm}"
        Visualizer.plot_graph(graph, tsp_path, title=graph_title)

        # Sanitize filename and save the graph
        sanitized_title = sanitize_filename(graph_title)
        filename = f"{sanitized_title}.png"
        file_manager = FileManager(base_dir="outputs")
        file_manager.save_graph(graph, tsp_path, filename=filename)

        
        organize_files(file_manager)


        # Return results
        return (f"TSP Path: {tsp_path}\n"
                f"Total Travel Length: {tsp_length:.2f}\n"
                f"Total Cost: {total_cost:.2f}\n"
                f"Total Time: {total_time:.2f} minutes")

    except InvalidInputError as e:
        logging.error(e)
        return f"Invalid input: {e}"
    except FileNotFoundError as e:
        logging.error(e)
        return f"File not found: {e}"
    except NetworkError as e:
        logging.error(e)
        return f"Network error: {e}"
    except ValueError as e:
        logging.error(e)
        return f"Validation error: {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"


def open_gui():
    """
    Opens the GUI for the Tarjan Planner.
    """
    def on_run():
        optimization_type = opt_var.get()
        transport_mode = mode_var.get()
        tsp_algorithm = alg_var.get()

        # Validate inputs
        if optimization_type == "single" and not transport_mode:
            messagebox.showerror("Error", "Transport mode is required for 'single' optimization.")
            return

        # Run planner and show results
        result = run_planner(optimization_type, transport_mode, tsp_algorithm)
        result_label.config(text=result)


    root = tk.Tk()
    root.title("Tarjan Planner GUI")

    # Optimization Type
    tk.Label(root, text="Optimization Type:").pack()
    opt_var = tk.StringVar(value="single")
    opt_menu = tk.OptionMenu(root, opt_var, "single", "mixed-time", "mixed-cost", "balanced")
    opt_menu.pack()

    # Transport Mode
    tk.Label(root, text="Transport Mode:").pack()
    mode_var = tk.StringVar(value="Bus")
    mode_menu = tk.OptionMenu(root, mode_var, "Bus", "Train", "Bicycle", "Walking")
    mode_menu.pack()

    # TSP Algorithm
    tk.Label(root, text="TSP Algorithm:").pack()
    alg_var = tk.StringVar(value="approximation")
    alg_menu = tk.OptionMenu(root, alg_var, "approximation", "greedy", "evolutionary")
    alg_menu.pack()

    # Run Button
    tk.Button(root, text="Run Planner", command=on_run).pack()

    # Result Label
    result_label = tk.Label(root, text="", fg="blue")
    result_label.pack()

    root.mainloop()

if __name__ == "__main__":
    open_gui()
