# Convex Hull Divide and Conquer Algorithm

A Python implementation of the Convex Hull algorithm using the Divide and Conquer approach with O(n log n) complexity.

## Project Structure

```
25-algo/
├── Project1/                    # Project files and test data
│   ├── input.csv               # Input points (x,y format)
│   ├── expectedOutput.txt      # Expected output indices
│   ├── DisplaySolution.py      # Visualization helper
│   └── project1.sh            # Execution script
├── tasks/                      # Task management
│   └── tasks-convex-hull-divide-conquer.md
├── point.py                    # Point class definition
├── convex_hull.py             # Main algorithm implementation
└── README.md                  # This file
```

## Algorithm Overview

The implementation follows the divide and conquer approach:

1. **Sort points by x-coordinate** (O(n log n))
2. **Divide** the point set into two halves
3. **Recursively compute** convex hulls for each half
4. **Merge** the two hulls using tangent finding (O(n))

## Key Components

- **Point Class**: Represents 2D coordinates with minimal dependencies
- **Input Parsing**: Reads CSV files and creates Point objects
- **Base Cases**: Handles 2 and 3 point scenarios
- **Hull Merging**: Implements tangent finding for hull combination
- **Output Generation**: Writes hull point indices to output.txt

## Usage

```bash
python3 convex_hull.py
```

## Requirements

- Python 3.6+
- No external dependencies (minimal imports approach)

## Testing

The project includes comprehensive unit tests and integration tests to verify:
- Point creation and manipulation
- Input parsing with error handling
- Base case scenarios (2-3 points)
- Hull merging algorithms
- Complete divide and conquer implementation

## Performance

- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Handles**: Up to 1 million points efficiently
