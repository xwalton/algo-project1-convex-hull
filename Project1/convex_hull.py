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


def find_lower_tangent(hull_a: list[Point], hull_b: list[Point]) -> tuple[int, int]:
    """
    Find the lower tangent between two convex hulls.
    
    The lower tangent is the line that connects the two hulls and lies below all other points
    in both hulls. This is used in the hull merging process.
    
    Args:
        hull_a (list[Point]): First convex hull (points in counterclockwise order)
        hull_b (list[Point]): Second convex hull (points in counterclockwise order)
        
    Returns:
        tuple[int, int]: Indices (a_idx, b_idx) of the tangent points in hull_a and hull_b
        
    Raises:
        ValueError: If either hull is empty or has fewer than 2 points
    """
    if not hull_a or not hull_b:
        raise ValueError("Both hulls must be non-empty")
    
    if len(hull_a) < 2 or len(hull_b) < 2:
        raise ValueError("Both hulls must have at least 2 points")
    
    # Start with rightmost point of hull_a and leftmost point of hull_b
    a_idx = find_rightmost_point(hull_a)
    b_idx = find_leftmost_point(hull_b)
    
    # Find the lower tangent by moving points until tangent is found
    improved = True
    while improved:
        improved = False
        
        # Move point a clockwise on hull_a until tangent is valid
        while True:
            next_a = (a_idx - 1) % len(hull_a)
            
            # Check if moving to next_a would improve the tangent
            # A tangent is valid if all other points in hull_b are above the line
            valid = True
            for i in range(len(hull_b)):
                if i != b_idx:
                    if not point_is_above_line(hull_a[next_a], hull_b[b_idx], hull_b[i]):
                        valid = False
                        break
            
            if valid:
                a_idx = next_a
                improved = True
            else:
                break
        
        # Move point b counterclockwise on hull_b until tangent is valid
        while True:
            next_b = (b_idx + 1) % len(hull_b)
            
            # Check if moving to next_b would improve the tangent
            # A tangent is valid if all other points in hull_a are above the line
            valid = True
            for i in range(len(hull_a)):
                if i != a_idx:
                    if not point_is_above_line(hull_a[a_idx], hull_b[next_b], hull_a[i]):
                        valid = False
                        break
            
            if valid:
                b_idx = next_b
                improved = True
            else:
                break
    
    return (a_idx, b_idx)


def find_upper_tangent(hull_a: list[Point], hull_b: list[Point]) -> tuple[int, int]:
    """
    Find the upper tangent between two convex hulls.
    
    The upper tangent is the line that connects the two hulls and lies above all other points
    in both hulls. This is used in the hull merging process.
    
    Args:
        hull_a (list[Point]): First convex hull (points in counterclockwise order)
        hull_b (list[Point]): Second convex hull (points in counterclockwise order)
        
    Returns:
        tuple[int, int]: Indices (a_idx, b_idx) of the tangent points in hull_a and hull_b
        
    Raises:
        ValueError: If either hull is empty or has fewer than 2 points
    """
    if not hull_a or not hull_b:
        raise ValueError("Both hulls must be non-empty")
    
    if len(hull_a) < 2 or len(hull_b) < 2:
        raise ValueError("Both hulls must have at least 2 points")
    
    # Start with rightmost point of hull_a and leftmost point of hull_b
    a_idx = find_rightmost_point(hull_a)
    b_idx = find_leftmost_point(hull_b)
    
    # Find the upper tangent by moving points until tangent is found
    improved = True
    while improved:
        improved = False
        
        # Move point a counterclockwise on hull_a until tangent is valid
        while True:
            next_a = (a_idx + 1) % len(hull_a)
            
            # Check if moving to next_a would improve the tangent
            # A tangent is valid if all other points in hull_b are below the line
            valid = True
            for i in range(len(hull_b)):
                if i != b_idx:
                    if point_is_above_line(hull_a[next_a], hull_b[b_idx], hull_b[i]):
                        valid = False
                        break
            
            if valid:
                a_idx = next_a
                improved = True
            else:
                break
        
        # Move point b clockwise on hull_b until tangent is valid
        while True:
            next_b = (b_idx - 1) % len(hull_b)
            
            # Check if moving to next_b would improve the tangent
            # A tangent is valid if all other points in hull_a are below the line
            valid = True
            for i in range(len(hull_a)):
                if i != a_idx:
                    if point_is_above_line(hull_a[a_idx], hull_b[next_b], hull_a[i]):
                        valid = False
                        break
            
            if valid:
                b_idx = next_b
                improved = True
            else:
                break
    
    return (a_idx, b_idx)


def merge_hulls(hull_a: list[Point], hull_b: list[Point]) -> list[Point]:
    """
    Merge two convex hulls using tangent finding.
    
    This function combines two separate convex hulls into a single convex hull
    by finding the upper and lower tangents and connecting them.
    
    Args:
        hull_a (list[Point]): First convex hull (points in counterclockwise order)
        hull_b (list[Point]): Second convex hull (points in counterclockwise order)
        
    Returns:
        list[Point]: Merged convex hull in counterclockwise order
        
    Raises:
        ValueError: If either hull is empty or has fewer than 2 points
    """
    if not hull_a or not hull_b:
        raise ValueError("Both hulls must be non-empty")
    
    if len(hull_a) < 2 or len(hull_b) < 2:
        raise ValueError("Both hulls must have at least 2 points")
    
    # Find the upper and lower tangents
    upper_a_idx, upper_b_idx = find_upper_tangent(hull_a, hull_b)
    lower_a_idx, lower_b_idx = find_lower_tangent(hull_a, hull_b)
    
    # Build the merged hull by traversing from lower tangent to upper tangent
    merged_hull = []
    
    # Add points from hull_a from lower tangent to upper tangent (counterclockwise)
    current_idx = lower_a_idx
    while True:
        merged_hull.append(hull_a[current_idx])
        if current_idx == upper_a_idx:
            break
        current_idx = (current_idx + 1) % len(hull_a)
    
    # Add points from hull_b from upper tangent to lower tangent (counterclockwise)
    current_idx = upper_b_idx
    while True:
        merged_hull.append(hull_b[current_idx])
        if current_idx == lower_b_idx:
            break
        current_idx = (current_idx + 1) % len(hull_b)
    
    return merged_hull


def convex_hull_recursive(points: list[Point]) -> list[Point]:
    """
    Recursively compute the convex hull using divide and conquer approach.
    
    This function implements the main divide and conquer algorithm:
    1. If points <= 3, use base case
    2. Divide points into two halves
    3. Recursively compute hulls for each half
    4. Merge the two hulls
    
    Args:
        points (list[Point]): List of points sorted by x-coordinate
        
    Returns:
        list[Point]: Convex hull points in counterclockwise order
        
    Raises:
        ValueError: If points list is empty or invalid
    """
    if not points:
        raise ValueError("Cannot compute convex hull of empty point set")
    
    # Base case: use base case function for small point sets
    if len(points) <= 3:
        return convex_hull_base_case(points)
    
    # Divide step: split points into two halves
    mid = len(points) // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Recursively compute convex hulls for each half
    left_hull = convex_hull_recursive(left_points)
    right_hull = convex_hull_recursive(right_points)
    
    # Merge the two hulls
    merged_hull = merge_hulls(left_hull, right_hull)
    
    return merged_hull


def convex_hull_divide_and_conquer(points: list[Point]) -> list[Point]:
    """
    Main entry point for the convex hull divide and conquer algorithm.
    
    This function implements the complete divide and conquer convex hull algorithm:
    1. Sort points by x-coordinate (O(n log n))
    2. Call the recursive convex hull function
    3. Return the final convex hull
    
    Args:
        points (list[Point]): List of points to compute convex hull for
        
    Returns:
        list[Point]: Convex hull points in counterclockwise order
        
    Raises:
        ValueError: If points list is empty or has fewer than 2 points
    """
    if not points:
        raise ValueError("Cannot compute convex hull of empty point set")
    
    if len(points) < 2:
        raise ValueError("Convex hull requires at least 2 points")
    
    # Step 1: Sort points by x-coordinate (O(n log n))
    # Note: According to the project requirements, points are already sorted by x-coordinate
    # But we'll ensure they are sorted for robustness
    sorted_points = sorted(points, key=lambda p: (p.x, p.y))
    
    # Step 2: Call the recursive convex hull function
    hull = convex_hull_recursive(sorted_points)
    
    # Step 3: Return the final convex hull
    return hull


def write_hull_indices_to_file(hull_points: list[Point], original_points: list[Point], filename: str = 'output.txt') -> None:
    """
    Write the indices of hull points to an output file.
    
    This function finds the indices of the hull points in the original point list
    and writes them to the specified output file, one index per line.
    
    Args:
        hull_points (list[Point]): List of points forming the convex hull
        original_points (list[Point]): Original list of all points
        filename (str): Name of the output file (default: 'output.txt')
        
    Raises:
        ValueError: If hull_points or original_points is empty
        IOError: If unable to write to the output file
    """
    if not hull_points:
        raise ValueError("Cannot write empty hull to file")
    
    if not original_points:
        raise ValueError("Original points list cannot be empty")
    
    # Find indices of hull points in the original point list
    hull_indices = []
    for hull_point in hull_points:
        # Find the index of this hull point in the original points
        for i, orig_point in enumerate(original_points):
            if hull_point.x == orig_point.x and hull_point.y == orig_point.y:
                hull_indices.append(i)
                break
        else:
            # If hull point not found in original points, this is an error
            raise ValueError(f"Hull point {hull_point} not found in original points")
    
    # Write indices to file
    try:
        with open(filename, 'w') as file:
            for index in hull_indices:
                file.write(f"{index}\n")
    except IOError as e:
        raise IOError(f"Unable to write to output file '{filename}': {e}")


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
            
            # Test output writing function
            print("\nTesting output writing function:")
            try:
                # Test with simple hull
                test_hull = [points[0], points[1]]  # First two points
                write_hull_indices_to_file(test_hull, points, 'test_output.txt')
                print("✓ Output writing function test passed")
                
                # Clean up test file
                import os
                if os.path.exists('test_output.txt'):
                    os.remove('test_output.txt')
                
            except Exception as e:
                print(f"✗ Output writing test failed: {e}")
        
        # TODO: Write output to output.txt
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
