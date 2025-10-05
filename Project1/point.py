class Point:
    """
    Represents a 2D point with x and y coordinates.
    Used for convex hull calculations in the divide and conquer algorithm.
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """String representation of the point."""
        return "Point({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        """Detailed string representation for debugging."""
        return "Point(x={}, y={})".format(self.x, self.y)
