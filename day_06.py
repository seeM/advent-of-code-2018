"""
Notes
-----
Build a grid of letters (dict mapping (x,y) points to letters).

Although the grid is infinite, we only care about the list of co-ordinates and
their neighbours.

Co-ordinates with finite area are those with letters not on the edge of the
truncated grid.

Once we have the grid, we can get the letter counts and the most common:
    Counter(grid.values()).most_common(1)

How to build the grid?

1. Add co-ordinates.
2. Find (x_min, x_max, y_min, y_max)
3. Loop through (x_min, x_max) -> (y_min, y_max):
     - Calculate manhatten distance to each co-ordinate
     - Take min distance's letter

Part 2
------
Build a different grid?
"""
from collections import Counter
from typing import Dict, List, Set, Tuple


Point = Tuple[int, int]
Grid = Dict[Point, Point]

def grid_bounds(coords: List[Point]) -> Tuple[Point, Point]:
    xs: List[int] = []
    ys: List[int] = []
    for x, y in coords:
        xs.append(x)
        ys.append(y)

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    return (x_min, y_min), (x_max, y_max)

def manhatten(point1: Point, point2: Point) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)

def build_grid(coords: List[Point]) -> Grid:
    (x_min, y_min), (x_max, y_max) = grid_bounds(coords)

    # Start one to the left of x_min and end one to the right of x_max
    grid: Grid = {}
    for x in range(x_min - 1, x_max + 2):
        # Start one to the left of y_min and end one to the right of y_max
        for y in range(y_min - 1, y_max + 2):
            point = (x, y)
            dists = [manhatten(point, coord) for coord in coords]
            min_dist = min(dists)

            closest_coord_idx = dists.index(min_dist)
            closest_coord = coords[closest_coord_idx]
            # If more than one coord are equally close then don't set grid val
            dists.pop(closest_coord_idx)
            try:
                dists.index(min_dist)
            except ValueError:
                grid[point] = closest_coord

    return grid

def boundary_points(grid: Grid, coords: List[Point]) -> List[Point]:
    """ Return points on the boundary of a grid, not necessarily sorted."""
    (x_min, y_min), (x_max, y_max) = grid_bounds(coords)

    # Top and bottom edge
    for x in range(x_min - 1, x_max + 2):
        point = (x, y_min - 1)
        if point in grid:
            yield point

        point = (x, y_max + 1)
        if point in grid:
            yield point

    # Left and right edge
    for y in range(y_min - 1, y_max + 2):
        point = (x_min - 1, y)
        if point in grid:
            yield point

        point = (x_max + 1, y)
        if point in grid:
            yield point

def finite_area_coords(grid: Grid, coords: List[Point]) -> Set[int]:
    coords = set(coords)
    for point in boundary_points(grid, coords):
        coord = grid[point]
        coords.discard(coord)
    return coords

def build_safe_region(coords: List[Point], threshold: int = 10_000) -> Set[Point]:
    (x_min, y_min), (x_max, y_max) = grid_bounds(coords)

    # Start one to the left of x_min and end one to the right of x_max
    region: Set[Point] = set()
    for x in range(x_min - 1, x_max + 2):
        # Start one to the left of y_min and end one to the right of y_max
        for y in range(y_min - 1, y_max + 2):
            point = (x, y)
            dist = sum(manhatten(point, coord) for coord in coords)
            if dist < threshold:
                region.add(point)

    return region


test_coords = [(1, 1),    # A
               (1, 6),    # B
               (8, 3),    # C
               (3, 4),    # D
               (5, 5),    # E
               (8, 9)]    # F
test_grid = build_grid(test_coords)
test_counts = Counter(test_grid.values())
test_finite_area_coords = finite_area_coords(test_grid, test_coords)
assert test_finite_area_coords == {(3, 4), (5, 5)}    # D, E
test_finite_area_counts = Counter({coord: count for coord, count in test_counts.items()
                                  if coord in test_finite_area_coords})
test_largest_finite_area = test_finite_area_counts.most_common(1)[0]
assert test_counts[(3, 4)] == 9
assert test_counts[(5, 5)] == 17
assert test_largest_finite_area == ((5, 5), 17)
test_safe_region = build_safe_region(test_coords, 32)
assert len(test_safe_region) == 16


if __name__ == '__main__':
    with open('data/day_06.txt') as f:
        coords = []
        for line in f.readlines():
            x, y = line.strip().split(', ')
            coords.append((int(x), int(y)))

    grid = build_grid(coords)
    # grid = finite_area_grid(grid)
    counts = Counter(grid.values())
    finite_area_coords_ = finite_area_coords(grid, coords)

    finite_area_counts = Counter({coord: count for coord, count in counts.items()
                                  if coord in finite_area_coords_})

    largest_finite_area = finite_area_counts.most_common(1)[0]

    print(largest_finite_area)
    print(len(build_safe_region(coords, 10_000)))
