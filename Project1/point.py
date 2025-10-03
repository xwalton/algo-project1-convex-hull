class Point:
    """
    Represents a 2D point with x and y coordinates.
    Used for convex hull calculations in the divide and conquer algorithm.
    """
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        """String representation of the point."""
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"Point(x={self.x}, y={self.y})"
