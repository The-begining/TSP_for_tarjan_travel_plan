import os
import shutil
import logging


class FileManager:
    def __init__(self, base_dir=None):
        """
        Initialize the FileManager.

        Args:
        - base_dir (str): The base directory for outputs. If None, defaults to 'outputs' in the project root.
        """
        # Dynamically set the base directory
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
        self.base_dir = base_dir

        self.log_dir = os.path.join(self.base_dir, "logs")
        self.graph_dir = os.path.join(self.base_dir, "graphs")

        # Ensure directories exist
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.graph_dir, exist_ok=True)

    def setup_logging(self, log_filename="application.log"):
        """
        Set up logging to a file and console.
        """
        log_path = os.path.join(self.log_dir, log_filename)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="a"),  # Append logs to the file
                logging.StreamHandler(),  # Also log to console
            ],
        )
        logging.info(f"Logging initialized. Logs will be saved to {log_path}")

    def save_graph(self, graph, tsp_path, filename="graph.png"):
        """
        Save the graph visualization to a file.
        
        Args:
        - graph (nx.Graph): The graph object.
        - tsp_path (list): List of nodes representing the TSP path (optional).
        - filename (str): File name for saving the graph.
        """
        from matplotlib import pyplot as plt
        import networkx as nx

        graph_path = os.path.join(self.graph_dir, filename)
        pos = nx.get_node_attributes(graph, 'pos')

        plt.figure(figsize=(12, 10))
        nx.draw(graph, pos, with_labels=True, node_size=700, font_size=9, edge_color='gray')

        if tsp_path:
            tsp_edges = list(zip(tsp_path, tsp_path[1:]))
            nx.draw_networkx_edges(graph, pos, edgelist=tsp_edges, edge_color='blue', width=2)

        plt.title("TSP Path")
        plt.savefig(graph_path, format=graph_path.split('.')[-1], bbox_inches='tight')
        plt.close()
        logging.info(f"Graph saved to {graph_path}")
