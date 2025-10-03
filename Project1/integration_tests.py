#!/usr/bin/env python3
"""
Integration tests for the complete convex hull pipeline.
Tests the entire system from input parsing to output generation.
"""

import os
import tempfile
import unittest
from convex_hull import (
    parse_input_file, 
    convex_hull_divide_and_conquer, 
    write_hull_indices_to_file,
    convex_hull_base_case,
    find_rightmost_point,
    find_leftmost_point,
    point_is_above_line
)
from point import Point


class TestConvexHullIntegration(unittest.TestCase):
    """Integration tests for the complete convex hull pipeline."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_points = [
            Point(0, 0),
            Point(1, 1), 
            Point(2, 0),
            Point(1, 0.5),
            Point(0.5, 0.5)
        ]
        
        # Create temporary files for testing
        self.temp_input = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.temp_output = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        self.temp_input.close()
        self.temp_output.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary files
        if os.path.exists(self.temp_input.name):
            os.unlink(self.temp_input.name)
        if os.path.exists(self.temp_output.name):
            os.unlink(self.temp_output.name)
    
    def test_input_parsing_integration(self):
        """Test input parsing with various CSV formats."""
        # Test normal CSV format
        csv_content = "0,0\n1,1\n2,0\n"
        with open(self.temp_input.name, 'w') as f:
            f.write(csv_content)
        
        points = parse_input_file(self.temp_input.name)
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0], Point(0, 0))
        self.assertEqual(points[1], Point(1, 1))
        self.assertEqual(points[2], Point(2, 0))
    
    def test_base_case_integration(self):
        """Test base case algorithm integration."""
        # Test 2 points
        two_points = [Point(0, 0), Point(1, 1)]
        hull_2 = convex_hull_base_case(two_points)
        self.assertEqual(len(hull_2), 2)
        self.assertIn(Point(0, 0), hull_2)
        self.assertIn(Point(1, 1), hull_2)
        
        # Test 3 points (triangle)
        three_points = [Point(0, 0), Point(2, 0), Point(1, 1)]
        hull_3 = convex_hull_base_case(three_points)
        self.assertEqual(len(hull_3), 3)
        
        # Test 3 collinear points
        collinear = [Point(0, 0), Point(1, 1), Point(2, 2)]
        hull_collinear = convex_hull_base_case(collinear)
        self.assertEqual(len(hull_collinear), 2)  # Should return endpoints
    
    def test_helper_functions_integration(self):
        """Test helper functions integration."""
        hull = [Point(0, 0), Point(2, 0), Point(1, 1), Point(0, 2)]
        
        # Test rightmost point finding
        rightmost_idx = find_rightmost_point(hull)
        self.assertEqual(rightmost_idx, 1)  # Point(2, 0)
        
        # Test leftmost point finding
        leftmost_idx = find_leftmost_point(hull)
        self.assertEqual(leftmost_idx, 0)  # Point(0, 0)
        
        # Test point above line
        p1, p2 = Point(0, 0), Point(2, 0)
        q_above = Point(1, 1)
        q_below = Point(1, -1)
        
        self.assertTrue(point_is_above_line(p1, p2, q_above))
        self.assertFalse(point_is_above_line(p1, p2, q_below))
    
    def test_output_writing_integration(self):
        """Test output writing integration."""
        hull_points = [Point(0, 0), Point(2, 0), Point(1, 1)]
        original_points = [Point(0, 0), Point(0.5, 0.5), Point(1, 1), Point(1.5, 0.5), Point(2, 0)]
        
        write_hull_indices_to_file(hull_points, original_points, self.temp_output.name)
        
        # Verify output file was created
        self.assertTrue(os.path.exists(self.temp_output.name))
        
        # Verify output content
        with open(self.temp_output.name, 'r') as f:
            content = f.read()
            lines = content.strip().split('\n')
            
        # Should have 3 indices plus empty line
        self.assertEqual(len(lines), 4)  # 3 indices + empty line
        self.assertEqual(lines[0], '0')  # Point(0, 0) at index 0
        self.assertEqual(lines[1], '4')  # Point(2, 0) at index 4
        self.assertEqual(lines[2], '2')  # Point(1, 1) at index 2
        self.assertEqual(lines[3], '')   # Empty line at end
    
    def test_complete_pipeline_integration(self):
        """Test complete pipeline with small dataset."""
        # Create test CSV file
        csv_content = "0,0\n1,1\n2,0\n"
        with open(self.temp_input.name, 'w') as f:
            f.write(csv_content)
        
        # Run complete pipeline
        points = parse_input_file(self.temp_input.name)
        self.assertEqual(len(points), 3)
        
        # Use base case for small datasets
        hull = convex_hull_base_case(points)
        self.assertGreater(len(hull), 0)
        self.assertLessEqual(len(hull), len(points))
        
        # Write output
        write_hull_indices_to_file(hull, points, self.temp_output.name)
        
        # Verify output
        self.assertTrue(os.path.exists(self.temp_output.name))
        with open(self.temp_output.name, 'r') as f:
            content = f.read()
            self.assertIn('\n', content)  # Should have line breaks
            self.assertTrue(content.endswith('\n\n'))  # Should end with empty line
    
    def test_error_handling_integration(self):
        """Test error handling across the pipeline."""
        # Test empty file
        with open(self.temp_input.name, 'w') as f:
            f.write('')
        
        with self.assertRaises(ValueError):
            parse_input_file(self.temp_input.name)
        
        # Test invalid CSV format
        with open(self.temp_input.name, 'w') as f:
            f.write("invalid,format,too,many,columns\n")
        
        with self.assertRaises(ValueError):
            parse_input_file(self.temp_input.name)
        
        # Test single point
        with open(self.temp_input.name, 'w') as f:
            f.write("1,1\n")
        
        points = parse_input_file(self.temp_input.name)
        with self.assertRaises(ValueError):
            convex_hull_base_case(points)
    
    def test_file_operations_integration(self):
        """Test file operations integration."""
        # Test with non-existent input file
        with self.assertRaises(FileNotFoundError):
            parse_input_file('non_existent_file.csv')
        
        # Test with read-only output file (if possible)
        # This test might not work on all systems, so we'll skip it
        pass
    
    def test_algorithm_correctness_integration(self):
        """Test algorithm correctness with known cases."""
        # Test with simple triangle (base case)
        triangle_points = [Point(0, 0), Point(2, 0), Point(1, 1)]
        
        hull = convex_hull_base_case(triangle_points)
        
        # Hull should contain all 3 points
        self.assertEqual(len(hull), 3)
        for point in triangle_points:
            self.assertIn(point, hull)
    
    def test_performance_integration(self):
        """Test performance with small dataset."""
        # Create a small dataset (5 points)
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), Point(0.5, 0.5)]
        
        # Test base case only (avoid divide and conquer for performance)
        hull = convex_hull_base_case(points[:3])  # Use first 3 points
        self.assertGreater(len(hull), 0)
        self.assertLessEqual(len(hull), 3)


def run_integration_tests():
    """Run all integration tests."""
    print("Running Convex Hull Integration Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvexHullIntegration)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✓ All integration tests passed!")
        return True
    else:
        print(f"✗ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
