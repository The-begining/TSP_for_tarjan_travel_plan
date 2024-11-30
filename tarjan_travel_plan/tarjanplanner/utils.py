from tarjan_travel_plan.tarjanplanner.decorators import log_execution
import networkx as nx
def add_logging_to_methods(cls):
    """
    Adds logging to all methods of a class dynamically.
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # Only modify callable methods
            setattr(cls, attr_name, log_execution(attr_value))
    return cls

