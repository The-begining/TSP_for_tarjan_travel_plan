import logging
import time

def log_execution(func):
    """
    A decorator that logs the execution of a function.
    """
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with arguments {args} and {kwargs}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def validate_input(allowed_values):
    """
    Validates that the first argument of the function is in the allowed values.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_input = args[0]
            if user_input not in allowed_values:
                raise ValueError(f"Invalid input: {user_input}. Allowed values are: {allowed_values}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
