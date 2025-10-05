#!/usr/bin/env python3
"""
Convex Hull using Divide and Conquer Algorithm
University Project - Analysis of Algorithms
"""

import sys
import csv
import argparse

# For Python 2.7 compatibility
try:
    from typing import List, Tuple
except ImportError:
    pass

EPS = 1e-12

class Point:
    """2D point with original index."""
    def __init__(self, x, y, idx):
        self.x = float(x)
        self.y = float(y)
        self.idx = int(idx)
    
    def __repr__(self):
        return "Point({}, {}, {})".format(self.x, self.y, self.idx)

def orient(a, b, c):
    """+1 if a->b->c CCW, -1 if CW, 0 if collinear (with EPS)."""
    val = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    if val > +EPS: 
        return +1
    if val < -EPS: 
        return -1
    return 0

def left_of(a, b, p):
    return orient(a, b, p) > 0

def right_of(a, b, p):
    return orient(a, b, p) < 0

def index_rightmost(H):
    """Find rightmost point in hull (max x, break ties with max y)."""
    k = 0
    for i in range(1, len(H)):
        if (H[i].x > H[k].x) or (H[i].x == H[k].x and H[i].y > H[k].y):
            k = i
    return k

def index_leftmost(H):
    """Find leftmost point in hull (min x, break ties with min y)."""
    k = 0
    for i in range(1, len(H)):
        if (H[i].x < H[k].x) or (H[i].x == H[k].x and H[i].y < H[k].y):
            k = i
    return k

def hull_base_case(arr, lo, hi):
    """Return CCW hull for 1..3 points in arr[lo:hi] (sorted by x then y)."""
    n = hi - lo
    if n == 1:
        return [arr[lo]]
    if n == 2:
        a, b = arr[lo], arr[lo+1]
        return [a, b]
    a, b, c = arr[lo], arr[lo+1], arr[lo+2]
    o = orient(a, b, c)
    if o >= 0:    # CCW or collinear
        if o == 0:
            # keep extremes only (sorted by x then y; a & c are extremes)
            return [a, c]
        return [a, b, c]
    else:
        return [a, c, b]  # flip to CCW

def upper_tangent(L, R):
    """Find upper tangent between two CCW hulls L and R."""
    i = index_rightmost(L)
    j = index_leftmost(R)
    nL, nR = len(L), len(R)

    changed = True
    # Safe bound: an endpoint can wrap at most once
    for _ in range(nL + nR + 5):
        if not changed:
            break
        changed = False
        # Move i forward while next L vertex is to the RIGHT of R[j] -> L[i]
        while right_of(R[j], L[i], L[(i+1) % nL]):
            i = (i + 1) % nL
            changed = True
        # Move j backward while previous R vertex is to the LEFT of L[i] -> R[j]
        while left_of(L[i], R[j], R[(j-1) % nR]):
            j = (j - 1) % nR
            changed = True
    else:
        raise RuntimeError("upper_tangent did not converge")
    return i, j

def lower_tangent(L, R):
    """Find lower tangent between two CCW hulls L and R."""
    i = index_rightmost(L)
    j = index_leftmost(R)
    nL, nR = len(L), len(R)

    changed = True
    for _ in range(nL + nR + 5):
        if not changed:
            break
        changed = False
        # Move i backward while previous L vertex is to the LEFT of R[j] -> L[i]
        while left_of(R[j], L[i], L[(i-1) % nL]):
            i = (i - 1) % nL
            changed = True
        # Move j forward while next R vertex is to the RIGHT of L[i] -> R[j]
        while right_of(L[i], R[j], R[(j+1) % nR]):
            j = (j + 1) % nR
            changed = True
    else:
        raise RuntimeError("lower_tangent did not converge")
    return i, j

def ensure_upper_tangent_valid(L, R, i, j):
    """Validate upper tangent (enable during debugging)."""
    A, B = L[i], R[j]
    assert orient(A, B, L[(i-1) % len(L)]) <= 0 and orient(A, B, L[(i+1) % len(L)]) <= 0, "Upper tangent invalid on L"
    assert orient(A, B, R[(j-1) % len(R)]) <= 0 and orient(A, B, R[(j+1) % len(R)]) <= 0, "Upper tangent invalid on R"

def ensure_lower_tangent_valid(L, R, i, j):
    """Validate lower tangent (enable during debugging)."""
    A, B = L[i], R[j]
    assert orient(A, B, L[(i-1) % len(L)]) >= 0 and orient(A, B, L[(i+1) % len(L)]) >= 0, "Lower tangent invalid on L"
    assert orient(A, B, R[(j-1) % len(R)]) >= 0 and orient(A, B, R[(j+1) % len(R)]) >= 0, "Lower tangent invalid on R"

def merge_hulls(L, R):
    """Merge two CCW hulls using upper and lower tangents."""
    if not L or not R:
        return L if L else R
    
    iu, ju = upper_tangent(L, R)
    il, jl = lower_tangent(L, R)

    # Enable while fixing; disable once stable
    # ensure_upper_tangent_valid(L, R, iu, ju)
    # ensure_lower_tangent_valid(L, R, il, jl)

    H = []

    # Walk L from iu -> il (inclusive) CCW
    k = iu
    H.append(L[k])
    while k != il:
        k = (k + 1) % len(L)
        H.append(L[k])

    # Walk R from jl -> ju (inclusive) CCW
    k = jl
    H.append(R[k])
    while k != ju:
        k = (k + 1) % len(R)
        H.append(R[k])

    return H

def convex_hull_dac(points_sorted, lo, hi):
    """Divide and conquer convex hull on index range."""
    n = hi - lo
    if n <= 3:
        return hull_base_case(points_sorted, lo, hi)

    mid = (lo + hi) // 2
    HL = convex_hull_dac(points_sorted, lo, mid)
    HR = convex_hull_dac(points_sorted, mid, hi)
    return merge_hulls(HL, HR)

def parse_input_file(filename):
    """Parse CSV file and return list of (x, y) tuples."""
    points = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for line_num, row in enumerate(reader, 1):
                if len(row) != 2:
                    raise ValueError("Line {}: Expected format 'x,y', got '{}'".format(line_num, ','.join(row)))
                try:
                    x, y = float(row[0]), float(row[1])
                    points.append((x, y))
                except ValueError as e:
                    raise ValueError("Line {}: Invalid coordinates '{}'".format(line_num, ','.join(row)))
    except IOError as e:
        raise IOError("Could not read file '{}': {}".format(filename, e))
    
    if len(points) < 3:
        raise ValueError("Need at least 3 points, got {}".format(len(points)))
    
    return points

def convex_hull(points_xy):
    """Compute convex hull and return indices in CCW order."""
    # Keep original indices
    pts = [Point(x, y, i) for i, (x, y) in enumerate(points_xy)]

    # Deduplicate exact duplicates (optional, recommended)
    pts.sort(key=lambda t: (t.x, t.y, t.idx))
    unique = []
    last = None
    for p in pts:
        if last is None or p.x != last.x or p.y != last.y:
            unique.append(p)
            last = p
    pts = unique

    # Sort once by (x, then y)
    pts.sort(key=lambda t: (t.x, t.y))

    H = convex_hull_dac(pts, 0, len(pts))

    # Return indices in hull cycle order (CCW)
    return [p.idx for p in H]

def write_hull_indices_to_file(hull_indices, filename):
    """Write hull indices to file, one per line."""
    try:
        with open(filename, 'w') as f:
            for i, idx in enumerate(hull_indices):
                if i > 0:
                    f.write('\n')
                f.write(str(idx))
    except IOError as e:
        raise IOError("Could not write to file '{}': {}".format(filename, e))

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Convex Hull using Divide and Conquer')
    parser.add_argument('input_file', help='Input CSV file with x,y coordinates')
    parser.add_argument('-o', '--output', default='output.txt', help='Output file for hull indices')
    
    args = parser.parse_args()
    
    try:
        # Parse input
        points = parse_input_file(args.input_file)
        print("Parsed {} points from {}".format(len(points), args.input_file))
        
        # Compute convex hull
        print("Computing convex hull...")
        hull_indices = convex_hull(points)
        
        # Write output
        write_hull_indices_to_file(hull_indices, args.output)
        print("Convex hull computed with {} points".format(len(hull_indices)))
        print("Results written to {}".format(args.output))
        
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()