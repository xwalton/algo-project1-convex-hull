from point import Point
from convex_hull import parse_input_file, find_rightmost_point, find_leftmost_point, convex_hull_base_case


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


def test_base_case_scenarios():
    """Test base case scenarios for convex hull computation."""
    print("Testing base case scenarios...")
    
    # Test 2 points - normal case
    two_points = [Point(0.0, 0.0), Point(1.0, 1.0)]
    hull_2 = convex_hull_base_case(two_points)
    assert len(hull_2) == 2
    assert hull_2[0].x == 0.0 and hull_2[0].y == 0.0
    assert hull_2[1].x == 1.0 and hull_2[1].y == 1.0
    print("✓ 2-point normal case passed")
    
    # Test 2 points - identical points (should raise error)
    try:
        identical_points = [Point(1.0, 1.0), Point(1.0, 1.0)]
        convex_hull_base_case(identical_points)
        print("✗ Should have raised error for identical points")
        return False
    except ValueError as e:
        assert "identical points" in str(e).lower()
        print("✓ 2-point identical points error handling passed")
    
    # Test 3 points - triangle (counterclockwise)
    triangle_points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.5, 1.0)]
    hull_3 = convex_hull_base_case(triangle_points)
    assert len(hull_3) == 3
    print("✓ 3-point triangle case passed")
    
    # Test 3 points - collinear
    collinear_points = [Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0)]
    hull_collinear = convex_hull_base_case(collinear_points)
    assert len(hull_collinear) == 2  # Should return only extremes
    assert hull_collinear[0].x == 0.0 and hull_collinear[0].y == 0.0
    assert hull_collinear[1].x == 2.0 and hull_collinear[1].y == 2.0
    print("✓ 3-point collinear case passed")
    
    # Test 3 points - duplicate points (should raise error)
    try:
        duplicate_points = [Point(0.0, 0.0), Point(1.0, 1.0), Point(0.0, 0.0)]
        convex_hull_base_case(duplicate_points)
        print("✗ Should have raised error for duplicate points")
        return False
    except ValueError as e:
        assert "duplicate points" in str(e).lower()
        print("✓ 3-point duplicate points error handling passed")
    
    # Test edge cases
    try:
        convex_hull_base_case([])
        print("✗ Should have raised error for empty list")
        return False
    except ValueError as e:
        assert "empty point set" in str(e).lower()
        print("✓ Empty list error handling passed")
    
    try:
        convex_hull_base_case([Point(1.0, 1.0)])
        print("✗ Should have raised error for single point")
        return False
    except ValueError as e:
        assert "at least 2 points" in str(e).lower()
        print("✓ Single point error handling passed")
    
    try:
        convex_hull_base_case([Point(1.0, 1.0), Point(2.0, 2.0), Point(3.0, 3.0), Point(4.0, 4.0)])
        print("✗ Should have raised error for too many points")
        return False
    except ValueError as e:
        assert "at most 3 points" in str(e).lower()
        print("✓ Too many points error handling passed")
    
    # Test with invalid Point objects
    try:
        convex_hull_base_case([Point(1.0, 1.0), "not a point"])
        print("✗ Should have raised error for invalid Point object")
        return False
    except ValueError as e:
        if "not a point object" in str(e).lower():
            print("✓ Invalid Point object error handling passed")
        else:
            print(f"✗ Unexpected error message: {e}")
            return False
    except TypeError:
        # This might also raise TypeError depending on implementation
        print("✓ Invalid Point object error handling passed (TypeError)")
    
    # Test with NaN values
    try:
        import math
        nan_point = Point(float('nan'), 1.0)
        convex_hull_base_case([Point(1.0, 1.0), nan_point])
        print("✗ Should have raised error for NaN values")
        return False
    except ValueError as e:
        assert "nan values" in str(e).lower()
        print("✓ NaN values error handling passed")
    
    # Test with infinity values
    try:
        inf_point = Point(float('inf'), 1.0)
        convex_hull_base_case([Point(1.0, 1.0), inf_point])
        print("✗ Should have raised error for infinity values")
        return False
    except ValueError as e:
        assert "infinite values" in str(e).lower()
        print("✓ Infinity values error handling passed")
    
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
        
        if not test_base_case_scenarios():
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
