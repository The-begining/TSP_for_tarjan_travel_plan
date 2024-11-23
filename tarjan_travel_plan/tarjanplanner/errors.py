class TarjanPlannerError(Exception):
    """Base class for all custom errors in TarjanPlanner."""
    pass

class InvalidInputError(TarjanPlannerError):
    """Raised when user input is invalid."""
    pass

class FileNotFoundError(TarjanPlannerError):
    """Raised when a required file is missing."""
    pass

class NetworkError(TarjanPlannerError):
    """Raised when a network operation fails."""
    pass
