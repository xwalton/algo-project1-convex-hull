from point import Point


def parse_input_file(filename: str) -> list[Point]:
    """
    Parse a CSV file containing points and return a list of Point objects.
    
    Args:
        filename (str): Path to the CSV file containing points in format "x,y"
        
    Returns:
        list[Point]: List of Point objects parsed from the file
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file format is invalid
    """
    points = []
    
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                try:
                    # Split the line by comma and parse coordinates
                    parts = line.split(',')
                    if len(parts) != 2:
                        raise ValueError(f"Line {line_num}: Expected format 'x,y', got '{line}'")
                    
                    x_str = parts[0].strip()
                    y_str = parts[1].strip()
                    
                    # Validate that coordinates are not empty
                    if not x_str or not y_str:
                        raise ValueError(f"Line {line_num}: Empty coordinates in '{line}'")
                    
                    # Parse coordinates
                    x = float(x_str)
                    y = float(y_str)
                    
                    # Check for NaN or infinity values
                    if not (x == x and y == y):  # NaN check
                        raise ValueError(f"Line {line_num}: NaN values not allowed in '{line}'")
                    if abs(x) == float('inf') or abs(y) == float('inf'):
                        raise ValueError(f"Line {line_num}: Infinite values not allowed in '{line}'")
                    
                    points.append(Point(x, y))
                    
                except ValueError as e:
                    if "could not convert" in str(e):
                        raise ValueError(f"Line {line_num}: Invalid number format in '{line}'")
                    else:
                        raise ValueError(f"Line {line_num}: {e}")
                        
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file '{filename}'")
    
    # Validate minimum point count
    if len(points) < 3:
        raise ValueError(f"At least 3 points required for convex hull, got {len(points)}")
    
    # Check for duplicate points
    seen_points = set()
    for i, point in enumerate(points):
        point_tuple = (point.x, point.y)
        if point_tuple in seen_points:
            raise ValueError(f"Duplicate point found at index {i}: ({point.x}, {point.y})")
        seen_points.add(point_tuple)
    
    return points


def find_rightmost_point(hull: list[Point]) -> int:
    """
    Find the index of the rightmost point in a convex hull.
    
    Args:
        hull (list[Point]): List of points forming a convex hull
        
    Returns:
        int: Index of the rightmost point (highest x-coordinate)
    """
    if not hull:
        raise ValueError("Cannot find rightmost point in empty hull")
    
    rightmost_idx = 0
    for i in range(1, len(hull)):
        if hull[i].x > hull[rightmost_idx].x:
            rightmost_idx = i
        elif hull[i].x == hull[rightmost_idx].x and hull[i].y > hull[rightmost_idx].y:
            # If x-coordinates are equal, choose the one with higher y-coordinate
            rightmost_idx = i
    
    return rightmost_idx


def find_leftmost_point(hull: list[Point]) -> int:
    """
    Find the index of the leftmost point in a convex hull.
    
    Args:
        hull (list[Point]): List of points forming a convex hull
        
    Returns:
        int: Index of the leftmost point (lowest x-coordinate)
    """
    if not hull:
        raise ValueError("Cannot find leftmost point in empty hull")
    
    leftmost_idx = 0
    for i in range(1, len(hull)):
        if hull[i].x < hull[leftmost_idx].x:
            leftmost_idx = i
        elif hull[i].x == hull[leftmost_idx].x and hull[i].y < hull[leftmost_idx].y:
            # If x-coordinates are equal, choose the one with lower y-coordinate
            leftmost_idx = i
    
    return leftmost_idx


def convex_hull_base_case(points: list[Point]) -> list[Point]:
    """
    Handle base cases for convex hull computation.
    
    Args:
        points (list[Point]): List of 2 or 3 points
        
    Returns:
        list[Point]: Convex hull points in order
        
    Raises:
        ValueError: If points list has invalid size
    """
    if len(points) == 2:
        # For 2 points, return them in order (line segment)
        return points.copy()
    
    elif len(points) == 3:
        # For 3 points, determine if they form a triangle or are collinear
        p1, p2, p3 = points[0], points[1], points[2]
        
        # Calculate cross product to determine orientation
        # (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        cross_product = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        
        if abs(cross_product) < 1e-10:  # Points are collinear
            # Return the two extreme points
            if p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y):
                if p2.x < p3.x or (p2.x == p3.x and p2.y < p3.y):
                    return [p1, p3]  # p1 and p3 are extremes
                else:
                    return [p1, p2]  # p1 and p2 are extremes
            else:
                if p1.x < p3.x or (p1.x == p3.x and p1.y < p3.y):
                    return [p2, p3]  # p2 and p3 are extremes
                else:
                    return [p1, p2]  # p1 and p2 are extremes
        else:
            # Points form a triangle, return all three in counterclockwise order
            if cross_product > 0:
                # Counterclockwise order
                return [p1, p2, p3]
            else:
                # Clockwise order, reverse to get counterclockwise
                return [p1, p3, p2]
    
    else:
        raise ValueError(f"Base case requires 2 or 3 points, got {len(points)}")


def main():
    """Main function to run the convex hull algorithm."""
    try:
        # Parse input points
        points = parse_input_file('input.csv')
        print(f"Parsed {len(points)} points from input file")
        
        # Test helper functions with first few points
        if len(points) >= 3:
            test_hull = points[:5]  # Use first 5 points for testing
            rightmost_idx = find_rightmost_point(test_hull)
            leftmost_idx = find_leftmost_point(test_hull)
            print(f"Test hull rightmost point: {test_hull[rightmost_idx]} at index {rightmost_idx}")
            print(f"Test hull leftmost point: {test_hull[leftmost_idx]} at index {leftmost_idx}")
            
            # Test base case functions
            print("\nTesting base cases:")
            # Test 2 points
            two_points = points[:2]
            hull_2 = convex_hull_base_case(two_points)
            print(f"2-point hull: {hull_2}")
            
            # Test 3 points
            three_points = points[:3]
            hull_3 = convex_hull_base_case(three_points)
            print(f"3-point hull: {hull_3}")
        
        # TODO: Implement convex hull algorithm
        # TODO: Write output to output.txt
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
