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
    Handle base cases for convex hull computation with comprehensive edge case validation.
    
    Args:
        points (list[Point]): List of 2 or 3 points
        
    Returns:
        list[Point]: Convex hull points in order
        
    Raises:
        ValueError: If points list has invalid size or contains invalid points
    """
    # Validate input
    if not points:
        raise ValueError("Cannot compute convex hull of empty point set")
    
    if len(points) < 2:
        raise ValueError(f"Convex hull requires at least 2 points, got {len(points)}")
    
    if len(points) > 3:
        raise ValueError(f"Base case handles at most 3 points, got {len(points)}")
    
    # Validate that all points are valid
    for i, point in enumerate(points):
        if not isinstance(point, Point):
            raise ValueError(f"Point at index {i} is not a Point object")
        if not (point.x == point.x and point.y == point.y):  # NaN check
            raise ValueError(f"Point at index {i} contains NaN values")
        if abs(point.x) == float('inf') or abs(point.y) == float('inf'):
            raise ValueError(f"Point at index {i} contains infinite values")
    
    if len(points) == 2:
        # For 2 points, return them in order (line segment)
        # Handle edge case where points are identical
        p1, p2 = points[0], points[1]
        if p1.x == p2.x and p1.y == p2.y:
            raise ValueError("Cannot compute convex hull of identical points")
        return points.copy()
    
    elif len(points) == 3:
        # For 3 points, determine if they form a triangle or are collinear
        p1, p2, p3 = points[0], points[1], points[2]
        
        # Check for duplicate points
        if (p1.x == p2.x and p1.y == p2.y) or \
           (p1.x == p3.x and p1.y == p3.y) or \
           (p2.x == p3.x and p2.y == p3.y):
            raise ValueError("Cannot compute convex hull with duplicate points")
        
        # Calculate cross product to determine orientation
        # (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        cross_product = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        
        # Use a more robust tolerance for collinearity check
        tolerance = 1e-12
        if abs(cross_product) < tolerance:  # Points are collinear
            # Find the two extreme points (leftmost and rightmost)
            # Sort by x-coordinate, then by y-coordinate for ties
            sorted_points = sorted(points, key=lambda p: (p.x, p.y))
            return [sorted_points[0], sorted_points[2]]  # Return extremes
        else:
            # Points form a triangle, return all three in counterclockwise order
            if cross_product > 0:
                # Counterclockwise order
                return [p1, p2, p3]
            else:
                # Clockwise order, reverse to get counterclockwise
                return [p1, p3, p2]


def point_is_above_line(p1: Point, p2: Point, q: Point) -> bool:
    """
    Determine if point q is above the line formed by points p1 and p2.
    
    This function is used for tangent validation in hull merging.
    
    Args:
        p1 (Point): First point defining the line
        p2 (Point): Second point defining the line  
        q (Point): Point to test if it's above the line
        
    Returns:
        bool: True if q is above the line, False otherwise
        
    Raises:
        ValueError: If p1 and p2 are the same point (vertical line)
    """
    # Handle edge case where p1 and p2 are the same point
    if p1.x == p2.x and p1.y == p2.y:
        raise ValueError("Cannot determine line with identical points")
    
    # Handle vertical line case
    if abs(p1.x - p2.x) < 1e-12:  # Vertical line
        # For vertical lines, compare y-coordinates
        return q.y > max(p1.y, p2.y)
    
    # Calculate slope and y-intercept for the line
    slope = (p2.y - p1.y) / (p2.x - p1.x)
    y_intercept = p1.y - slope * p1.x
    
    # Calculate the y-value of the line at q's x-coordinate
    y_line = slope * q.x + y_intercept
    
    # Point is above the line if its y-coordinate is greater than the line's y-value
    return q.y > y_line


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
            
            # Test edge cases
            print("\nTesting edge cases:")
            try:
                # Test empty list
                convex_hull_base_case([])
                print("✗ Should have raised error for empty list")
            except ValueError as e:
                print(f"✓ Empty list error: {e}")
            
            try:
                # Test single point
                convex_hull_base_case([points[0]])
                print("✗ Should have raised error for single point")
            except ValueError as e:
                print(f"✓ Single point error: {e}")
            
            try:
                # Test identical points
                identical_points = [points[0], points[0]]
                convex_hull_base_case(identical_points)
                print("✗ Should have raised error for identical points")
            except ValueError as e:
                print(f"✓ Identical points error: {e}")
            
            try:
                # Test collinear points
                collinear_points = [
                    Point(0.0, 0.0),
                    Point(1.0, 1.0),
                    Point(2.0, 2.0)
                ]
                hull_collinear = convex_hull_base_case(collinear_points)
                print(f"✓ Collinear points hull: {hull_collinear}")
            except Exception as e:
                print(f"✗ Collinear test failed: {e}")
            
            # Test PointIsAboveLine function
            print("\nTesting PointIsAboveLine function:")
            try:
                # Test normal case
                p1 = Point(0.0, 0.0)
                p2 = Point(2.0, 2.0)
                q_above = Point(1.0, 2.0)  # Above the line
                q_below = Point(1.0, 0.5)  # Below the line
                
                above_result = point_is_above_line(p1, p2, q_above)
                below_result = point_is_above_line(p1, p2, q_below)
                
                print(f"Point {q_above} above line: {above_result}")
                print(f"Point {q_below} above line: {below_result}")
                
                # Test vertical line
                p_vert1 = Point(1.0, 0.0)
                p_vert2 = Point(1.0, 2.0)
                q_vert = Point(1.0, 3.0)
                vert_result = point_is_above_line(p_vert1, p_vert2, q_vert)
                print(f"Point {q_vert} above vertical line: {vert_result}")
                
            except Exception as e:
                print(f"✗ PointIsAboveLine test failed: {e}")
        
        # TODO: Implement convex hull algorithm
        # TODO: Write output to output.txt
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
