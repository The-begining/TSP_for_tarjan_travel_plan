import os
from graphviz import Digraph

# Set Graphviz path (replace with your actual Graphviz installation path)
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

# Create the flowchart as before
flowchart = Digraph(format='png', graph_attr={'rankdir': 'TB'}, node_attr={'shape': 'box', 'style': 'rounded'})
flowchart.node("User Interaction", "User Interaction (Main Interface)\nInput preferences: locations, transport modes,\noptimization criteria, algorithm selection")
flowchart.node("GraphBuilder", "GraphBuilder\nConstructs graph with nodes and edges\nAssigns weights based on optimization criteria")
flowchart.node("TSPSolver", "TSPSolver\nSelects algorithm (Christofides, Heuristic, Evolutionary)\nComputes optimal route")
flowchart.node("Visualizer", "Visualizer\nGenerates graphical representation\nHighlights computed route")
flowchart.node("FileManager", "FileManager\nLogs execution details\nOrganizes outputs (logs, graphs, reports)")

# Add edges to represent the flow
flowchart.edge("User Interaction", "GraphBuilder", label="Validate input and process data")
flowchart.edge("GraphBuilder", "TSPSolver", label="Constructed graph with weights")
flowchart.edge("TSPSolver", "Visualizer", label="Optimal route and metrics")
flowchart.edge("Visualizer", "FileManager", label="Save visualized graph")
flowchart.edge("FileManager", "User Interaction", label="Access results")

# Render the flowchart
flowchart.render('Tarjan_Travel_Planner_Flowchart', format='png', cleanup=True)
