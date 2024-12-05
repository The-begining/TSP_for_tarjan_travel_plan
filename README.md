# TSP for Tarjan Travel Plan

## Overview
**Tarjan Travel Plan** is a Python-based application that solves the **Traveling Salesman Problem (TSP)** for planning optimal travel routes between a set of locations. The application provides flexible optimization options for travel based on time, cost, and transport mode. It supports:
- **Single-mode transport** (e.g., Bus, Train, Bicycle, Walking).
- **Mixed-mode transport** optimization based on distance thresholds.
- Optimization criteria such as **time**, **cost**, or a **balanced** combination of both.

The application includes:
- **Graph-based travel modeling**.
- **TSP-solving algorithms** for route optimization.
- **Interactive CLI and GUI** for easy customization.
- **Dynamic visualizations** of the travel graph and optimized route.

---

## Features
- **Transport Modes**:
  - Walking, Bicycle, Bus, and Train.
- **Optimization Options**:
  - Single-mode: Optimize using a single transport mode.
  - Mixed-mode: Automatically select transport mode based on distance thresholds.
  - Mixed-time: Optimize for shortest travel time.
  - Mixed-cost: Optimize for the lowest travel cost.
  - Balanced: Combine time and cost for efficient planning.
- **Graphical User Interface (GUI)**:
  - Intuitive interface for selecting optimization options and visualizing the TSP graph.
- **Dynamic Graph Visualization**:
  - View the travel network graph and optimized path.
- **Evolutionary Algorithms**:
  - Solve TSP using approximation, greedy, or evolutionary methods.
- **File Organization**:
  - Automated organization of outputs (e.g., logs, visualizations).

---

## Installation

### Prerequisites
- Python 3.7 or later
- pip (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/The-begining/TSP_for_tarjan_travel_plan.git
   cd TSP_for_tarjan_travel_plan

2. pip install -r requirements.txt
3. pip install -e .

-------------
## Usage

### Command-Line Interface(CLI)

tarjan-planner

You will be prompted to choose optimization options:
1. Single-mode: Optimize using one transport mode (e.g., Bus).
2. Mixed-time: Optimize for shortest travel time.
3. Mixed-cost: Optimize for the lowest travel cost.
4. Balanced: Combine time and cost for an optimal solution.
#### Example:
Choose optimization type ('single', 'mixed-time', 'mixed-cost', 'balanced'): balanced

### Graphical User Interface (GUI)
Run the GUI:

tarjan-planner-gui

The GUI allows you to:

-Select optimization type (e.g., single, mixed-time, mixed-cost, balanced).
-Choose a transport mode for single-mode optimization.
-Select a TSP algorithm (e.g., approximation, greedy, evolutionary).
-View the optimized graph visualization.

---------------------------
## File Structure
TSP_FOR_TARJAN_TRAVEL_PLAN/
├──tarjan_travel_plan/                  # Project documentation
│  ├── tarjanplanner/                # Core application logic
│  │     ├── __init__.py
│  │     ├── main.py                   # CLI entry point
│  │     ├── graph_builder.py          # Graph construction and edge weighting
│  │     ├── tsp_solver.py             # TSP solver logic
│  │     ├── visualizer.py             # Graph visualization
│  │     ├── decorators.py             # Utilities for decorators
│  │     ├── errors.py                 # Custom error handling
│  ├── fileorganizer/                # File management utilities
│  │     ├── __init__.py
│  │     ├── file_manager.py           # File and logging manager
│  │     ├── file_classifier.py        # File classification logic
│  ├── outputs/                      # Output directory for logs and visualizations  
│  ├── tests/                        # Unit tests
│  │     ├── __init__.py
│  │     ├── test_graph_builder.py
│  │     ├── test_tsp_solver.py
│  │     ├── test_input_validation.py
│  ├── tarjan_travel_plan.log 
├──gui_interface.py       # Logging file for CLI/GUI execution
├── setup.py                      # Installation configuration
├── requirements.txt              # Project dependencies
├── README.md
------------------------
## Testing
pytest tests/

#### Example Output:
============================================================================== test session starts =========================================================
platform win32 -- Python 3.13.0, pytest-8.3.3, pluggy-1.5.0
plugins: anyio-4.6.2.post1
collected 6 items

tests\test_file_classifier.py                                                                                                                    [ 16%]
tests\test_graph_builder.py                                                                                                                      [ 50%] 
tests\test_input_validation.py                                                                                                                   [ 83%] 
tests\test_tsp_solver.py                                                                                                                         [100%]    
====================================================================== 6 passed in 1.09s ================================================================ 
### Key Concepts
#### Transport Modes
  -Walking: For distances under 1 km.
  -Bicycle: For medium distances (1-3 km).
  -Bus: For distances between 3 and 20 km.
  -Train: For distances over 20 km.
#### Optimization Criteria
  -Time: Minimizes total travel time (including transfer times).
  -Cost: Minimizes total travel cost based on the transport mode.
  -Balanced: Combines time and cost for a weighted solution.

-------------------------------
## Graph Visualization
The application dynamically generates a travel network graph:

  Nodes: Relatives' locations.
  Edges: Travel paths annotated with transport modes, costs, and times.

### Contributing
Contributions are welcome! Please:

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request.

---------------------------
## License
This project is licensed under the MIT License.

## Author

**Shubham Singh**  
[shsin5910@oslomet.no](mailto:shsin5910@oslomet.no)




