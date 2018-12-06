"""
Idea:
-----
Build a grid in a single pass through the data:
    Grid is a dict, mapping (x, y) co-ordinates to a list of claim IDs

    Grid counts is a dict, mapping (x, y) co-ordinates to length of list

Count number of elements in grid_counts with value > 1
"""
import re
from collections import defaultdict
from typing import Dict, List, NamedTuple, Set, Tuple


Point = Tuple[int, int]

class Claim(NamedTuple):
    id: int
    x: int
    y: int
    width: int
    height: int

    def points(self) -> List[Point]:
        return [(x, y) for x in range(self.x, self.x + self.width)
                for y in range(self.y, self.y + self.height)]

Grid = Dict[Point, Set[int]]

def build_grid(claims: List[Claim]) -> Grid:
    grid: Grid = defaultdict(set)

    for claim in claims:
        for point in claim.points():
            grid[point].add(claim.id)

    return grid

def shared_inches(grid: Grid) -> int:
    return len([point for point, claim_ids in grid.items()
                if len(claim_ids) > 1])

def unique_claims(claims: List[Claim], grid: Grid) -> List[int]:
    unique_claim_ids = {claim.id for claim in claims}
    for _, claim_ids in grid.items():
        if len(claim_ids) <= 1:
            continue
        for claim_id in claim_ids:
            unique_claim_ids.discard(claim_id)
    return list(unique_claim_ids)


pattern = re.compile('^#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)$')

with open('data/day_03.txt') as f:
    claims = []
    for line in f.readlines():
        line = line.strip()
        id, x, y, width, height = re.match(pattern, line).groups()
        id = int(id)
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        claims.append(Claim(id, x, y, width, height))

test_claims = [Claim(1, 1, 3, 4, 4),
               Claim(2, 3, 1, 4, 4),
               Claim(3, 5, 5, 2, 2)]
test_grid = build_grid(test_claims)
test_unique_claims = unique_claims(test_claims, test_grid)
assert shared_inches(test_grid) == 4
assert len(test_unique_claims) == 1
assert test_unique_claims[0] == 3

grid = build_grid(claims)
print(shared_inches(grid))
unique_claims_ = unique_claims(claims, grid)
assert len(unique_claims_) == 1
print(unique_claims_[0])
