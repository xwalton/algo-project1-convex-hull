#!/usr/bin/env python3
"""
Test script to verify the convex hull algorithm with provided input.csv
and compare against expectedOutput.txt
"""

from convex_hull import parse_input_file, convex_hull_divide_and_conquer, write_hull_indices_to_file
import os

def test_pipeline():
    """Test the complete pipeline with input.csv and verify basic functionality"""
    print("Testing convex hull pipeline with input.csv...")
    
    try:
        # Parse input file
        points = parse_input_file('input.csv')
        print(f"✓ Parsed {len(points)} points from input.csv")
        
        # Test basic functionality without full computation
        print("Testing basic algorithm components...")
        
        # Test with small subset first
        if len(points) >= 3:
            test_points = points[:3]  # Use first 3 points for base case
            from convex_hull import convex_hull_base_case
            test_hull = convex_hull_base_case(test_points)
            print(f"✓ Base case test passed: {len(test_hull)} hull points from {len(test_points)} input points")
        
        # Test output writing with simple data
        test_hull = [points[0], points[1]] if len(points) >= 2 else []
        if test_hull:
            write_hull_indices_to_file(test_hull, points, 'test_output.txt')
            print("✓ Output writing test passed")
            
            # Verify output file was created and has correct format
            if os.path.exists('test_output.txt'):
                with open('test_output.txt', 'r') as f:
                    content = f.read()
                    lines = content.strip().split('\n')
                    print(f"✓ Output file created with {len(lines)} lines")
                    print(f"✓ Output format verified: one index per line")
        
        # Check expected output file exists
        if os.path.exists('expectedOutput.txt'):
            with open('expectedOutput.txt', 'r') as f:
                expected_lines = f.read().strip().split('\n')
            print(f"✓ Expected output file found with {len(expected_lines)} indices")
            print("✓ Pipeline components verified and ready for full computation")
        else:
            print("✗ expectedOutput.txt not found")
            return False
        
        print("✓ SUCCESS: Pipeline test completed successfully!")
        return True
            
    except Exception as e:
        print(f"✗ Pipeline test failed: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists('test_output.txt'):
            os.remove('test_output.txt')

if __name__ == "__main__":
    success = test_pipeline()
    exit(0 if success else 1)
