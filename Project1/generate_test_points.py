#!/usr/bin/env python3
"""
Script to generate 50 additional random points for testing the convex hull algorithm.
"""

import random
import csv

def generate_random_points(num_points=50, x_range=(0, 10), y_range=(0, 10)):
    """Generate random points within specified ranges."""
    points = []
    for _ in range(num_points):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        points.append((x, y))
    
    # Sort by x-coordinate to maintain the expected format
    points.sort(key=lambda p: p[0])
    return points

def append_points_to_csv(filename, new_points):
    """Append new points to the existing CSV file."""
    with open(filename, 'a') as file:
        for x, y in new_points:
            file.write("{},{}\n".format(x, y))

def main():
    # Generate 50 random points
    print("Generating 50 random points...")
    new_points = generate_random_points(50, x_range=(0, 10), y_range=(0, 10))
    
    # Append to input.csv
    print("Appending points to input.csv...")
    append_points_to_csv('input.csv', new_points)
    
    print("Generated {} new points and appended to input.csv".format(len(new_points)))
    print("New points range:")
    print("  X: {:.3f} to {:.3f}".format(min(p[0] for p in new_points), max(p[0] for p in new_points)))
    print("  Y: {:.3f} to {:.3f}".format(min(p[1] for p in new_points), max(p[1] for p in new_points)))

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    main()
