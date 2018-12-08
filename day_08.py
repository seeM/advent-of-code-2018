"""
Task 1
------
Need a way to process a stream of numbers to build a tree
Then need a way of recursively adding properties of nodes in the tree

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2

Need to know if its a new node, and if so:
e.g [2, 3, ...]
     |  |
     |  ----> Number of metadata entries
     -------> Number of children
"""
from operator import add
from functools import reduce
from typing import List, NamedTuple


class Node(NamedTuple):
    children: List['Node']
    metadata: List[int]


def parse_nums(nums: List[int]) -> Node:
    nodes = _parse_nums(nums)
    return nodes[0].children[0]


def _parse_nums(nums: List[int],
                num_children: int = 1,
                num_metadata: int = 0):
    children = []
    for _ in range(num_children):
        child_num_children = nums[0]
        child_num_metadata = nums[1]
        nums = nums[2:]
        child_node, nums = _parse_nums(nums, child_num_children, child_num_metadata)
        children.append(child_node)

    metadata = nums[:num_metadata]
    nums = nums[num_metadata:]

    return Node(children, metadata), nums


def get_metadata(node: Node) -> List[int]:
    return node.metadata \
           + reduce(add, (get_metadata(child) for child in node.children), [])


def get_value(node: Node) -> int:
    if node.children:
        value = 0
        for index in node.metadata:
            try:
                child = node.children[index - 1]
                value += get_value(child)
            except IndexError:
                pass
        return value
    else:
        return sum(node.metadata)


test_license = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
test_nums = [int(num) for num in test_license.split()]
test_parent = parse_nums(test_nums)
test_metadata = get_metadata(test_parent)
assert test_metadata == [1, 1, 2, 10, 11, 12, 2, 99]
assert sum(test_metadata) == 138
assert get_value(test_parent) == 66


if __name__ == '__main__':
    with open('data/day_08.txt') as f:
        nums = [int(num) for num in f.read().split()]
        parent = parse_nums(nums)
        metadata = get_metadata(parent)
        print(sum(metadata))
        print(get_value(parent))
