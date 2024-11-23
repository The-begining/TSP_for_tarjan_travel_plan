# TSP_for_tarjan_visiting

## Overview
**Tarjan Travel Plan** is a Python-based application that solves the **Traveling Salesman Problem (TSP)** for planning optimal travel routes between a set of relatives' locations. It supports:
- **Single-mode transport** optimization (e.g., Bus, Train, Bicycle, Walking).
- **Mixed-mode transport** optimization based on distance thresholds.
- Optimization based on **time**, **cost**, or a **balanced** combination of both.

The project incorporates:
- **Graph-building for locations**.
- **TSP solving** for route optimization.
- **Interactive CLI options** for customization.
- **Dynamic visualizations** of the travel network and path.

---

## Features
- **Multiple Transport Modes**:
  - Walking, Bicycle, Bus, and Train.
- **Optimization Options**:
  - Single-mode: Optimize using one transport mode.
  - Mixed-mode: Automatically select transport mode based on distance thresholds.
  - Mixed-time and Mixed-cost optimization.
  - Balanced optimization (time + cost).
- **Dynamic Graph Visualization**:
  - View the travel network and optimal path.

---

## Installation

### Prerequisites
- Python 3.7 or later
- pip (Python package manager)

### Install Dependencies
Clone the repository and navigate to the project directory:
```bash
git https://github.com/The-begining/TSP_for_tarjan_travel_plan.git
cd tarjan_travel_plan
Install dependencies:

bash
Copy code
pip install -r requirements.txt

## Install the project in editable mode:


bash
Copy code
pip install -e .
Usage
Command-Line Interface
Run the application:

bash
Copy code
tarjan-planner
You will be prompted to choose optimization options:

Single-mode: Optimize using a single transport mode (e.g., Bus).
Mixed-time: Optimize for shortest travel time.
Mixed-cost: Optimize for the lowest travel cost.
Balanced: Combine time and cost for a balanced solution.
Example
plaintext
Copy code
Choose optimization type ('single', 'mixed-time', 'mixed-cost', 'balanced'): balanced
Project Structure
plaintext
Copy code
tarjan_travel_plan/
├── setup.py                # Installation configuration
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── tarjanplanner/          # Core application logic
│   ├── __init__.py
│   ├── main.py             # Main entry point
│   ├── graph_builder.py    # Graph construction and edge weighting
│   ├── tsp_solver.py       # TSP solver logic
│   ├── visualizer.py       # Graph visualization
│   ├── decorators.py       # Metaprogramming utilities
│   ├── utils.py            # Helper utilities
│   ├── errors.py           # Custom error handling
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_graph_builder.py
│   ├── test_tsp_solver.py
│   ├── test_input_validation.py
Testing
Run tests using pytest:

bash
Copy code
pytest tests/
Example output:

plaintext
Copy code
======================================================== test session starts ========================================================
platform win32 -- Python 3.10.0, pytest-8.3.3
collected 4 items

tests/test_graph_builder.py ..                                                                                                 [ 50%]
tests/test_tsp_solver.py ..                                                                                                   [100%]

========================================================= 4 passed in 0.52s =========================================================
Key Concepts
Transport Modes
Walking: Suitable for short distances (<1 km).
Bicycle: For medium distances (1-3 km).
Bus: For distances between 3 and 20 km.
Train: For distances over 20 km.
Optimization Criteria
Time: Minimizes total travel time (including transfer times).
Cost: Minimizes total travel cost based on transport mode.
Balanced: Combines time and cost for an efficient solution.
Graph Visualization
The application dynamically generates and displays a graph of the travel network. The graph includes:

Nodes: Relatives' locations.
Edges: Travel paths with modes, costs, and times labeled.
Future Enhancements
Add support for dynamic transport costs (e.g., surge pricing).
Enable route adjustments for specific preferences (e.g., avoid trains).
Add live data integration (e.g., traffic or public transport schedules).
Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

License
This project is licensed under the MIT License.

Author
Shubham Singh
Email: shsin5910@oslomet.no