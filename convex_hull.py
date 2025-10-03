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


def main():
    """Main function to run the convex hull algorithm."""
    try:
        # Parse input points
        points = parse_input_file('Project1/input.csv')
        print(f"Parsed {len(points)} points from input file")
        
        # TODO: Implement convex hull algorithm
        # TODO: Write output to output.txt
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
