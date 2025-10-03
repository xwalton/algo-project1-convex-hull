#!/bin/bash

echo "Running Convex Hull Algorithm..."
echo "================================"

# Run the convex hull algorithm
python3 convex_hull.py input.csv -o output.txt

echo ""
echo "Algorithm completed. Displaying results..."
echo ""

# Display the results using the visualization script
python3 DisplaySolution.py