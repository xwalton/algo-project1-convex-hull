from point import Point
from convex_hull import parse_input_file, find_rightmost_point, find_leftmost_point


def test_point_creation():
    """Test Point class creation and string representations."""
    print("Testing Point class...")
    
    # Test basic creation
    p1 = Point(1.0, 2.0)
    assert p1.x == 1.0
    assert p1.y == 2.0
    
    # Test string representation
    assert str(p1) == "Point(1.0, 2.0)"
    assert repr(p1) == "Point(x=1.0, y=2.0)"
    
    # Test with negative coordinates
    p2 = Point(-3.5, 4.2)
    assert p2.x == -3.5
    assert p2.y == 4.2
    
    print("✓ Point class tests passed")


def test_input_parsing():
    """Test input parsing functionality."""
    print("Testing input parsing...")
    
    # Test with valid input file
    try:
        points = parse_input_file('input.csv')
        assert len(points) == 50
        assert isinstance(points[0], Point)
        assert points[0].x == 0.233396975
        assert points[0].y == 1.224233318
        print("✓ Valid input parsing passed")
    except Exception as e:
        print(f"✗ Valid input parsing failed: {e}")
        return False
    
    # Test with non-existent file
    try:
        parse_input_file('nonexistent.csv')
        print("✗ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("✓ Non-existent file handling passed")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    return True


def test_helper_functions():
    """Test helper functions for finding extreme points."""
    print("Testing helper functions...")
    
    # Create test hull
    test_hull = [
        Point(0.0, 0.0),   # leftmost
        Point(1.0, 1.0),
        Point(2.0, 0.5),
        Point(3.0, 2.0),   # rightmost
        Point(1.5, 3.0)
    ]
    
    # Test rightmost point
    rightmost_idx = find_rightmost_point(test_hull)
    assert rightmost_idx == 3
    assert test_hull[rightmost_idx].x == 3.0
    print("✓ Rightmost point finding passed")
    
    # Test leftmost point
    leftmost_idx = find_leftmost_point(test_hull)
    assert leftmost_idx == 0
    assert test_hull[leftmost_idx].x == 0.0
    print("✓ Leftmost point finding passed")
    
    # Test with single point
    single_point = [Point(1.0, 1.0)]
    assert find_rightmost_point(single_point) == 0
    assert find_leftmost_point(single_point) == 0
    print("✓ Single point handling passed")
    
    # Test empty hull error
    try:
        find_rightmost_point([])
        print("✗ Should have raised ValueError for empty hull")
        return False
    except ValueError:
        print("✓ Empty hull error handling passed")
    
    return True


def test_edge_cases():
    """Test edge cases and error conditions."""
    print("Testing edge cases...")
    
    # Test points with same x-coordinate
    same_x_hull = [
        Point(1.0, 0.0),   # lower y
        Point(1.0, 2.0),   # higher y
        Point(2.0, 1.0)
    ]
    
    rightmost_idx = find_rightmost_point(same_x_hull)
    # Should pick the one with highest x-coordinate (2.0)
    assert rightmost_idx == 2
    print("✓ Rightmost point with different x-coordinates passed")
    
    # Test tie-breaking for equal x-coordinates
    equal_x_hull = [
        Point(1.0, 0.0),   # lower y
        Point(1.0, 2.0),   # higher y
    ]
    
    rightmost_idx = find_rightmost_point(equal_x_hull)
    # Should pick the one with higher y-coordinate when x is equal
    assert rightmost_idx == 1
    print("✓ Tie-breaking for equal x-coordinates passed")
    
    return True


def run_all_tests():
    """Run all unit tests."""
    print("Running unit tests for convex hull implementation...\n")
    
    try:
        test_point_creation()
        print()
        
        if not test_input_parsing():
            return False
        print()
        
        if not test_helper_functions():
            return False
        print()
        
        if not test_edge_cases():
            return False
        print()
        
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
