# Convex Hull Algorithm

A clean Python implementation of the Convex Hull algorithm using divide and conquer. Fast and efficient!

## What's in here

```
25-algo/
├── Project1/                    # Test data and helpers
│   ├── input.csv               # Sample points (x,y format)
│   ├── expectedOutput.txt      # Expected results
│   ├── DisplaySolution.py      # Visualize the hull
│   └── project1.sh            # Run script
├── point.py                    # Simple Point class
├── convex_hull.py             # Main algorithm
└── README.md                  # This file
```

## How it works

Pretty straightforward divide and conquer:

1. **Sort** points by x-coordinate 
2. **Split** into two halves
3. **Recurse** on each half
4. **Merge** the hulls together

## Key stuff

- **Point Class**: Just x,y coordinates, nothing fancy
- **Input Parsing**: Reads CSV and makes Point objects
- **Base Cases**: Handles 2-3 points easily
- **Hull Merging**: Finds tangents to combine hulls
- **Output**: Writes hull point indices to output.txt

## Running it

```bash
python3 convex_hull.py
```

## What you need

- Python 3.6+ (just the standard library)
- That's it! No extra packages

## Testing

Check it out with the included test data:
- `input.csv`: 50 sample points
- `expectedOutput.txt`: What the output should look like
- `DisplaySolution.py`: Visualize your results

## Performance

- **Time**: O(n log n) - pretty fast!
- **Space**: O(n) - memory efficient
- **Scale**: Handles up to 1 million points no problem
