"""
Part 1
------
We assume the data is a directed acyclic graph (DAG) of tasks.

Represented by a set of nodes, and a dictionary mapping Target nodes to a list
of their pre-requisites.

We need to build a basic task scheduler:
    Starting with leaf nodes (initial available nodes)
    Loop until no available nodes:
        Given all available nodes, schedule first (in alphabetical order)
        Update list of available nodes
            Create a new tree: where scheduled node is removed from all
            dependency lists

Scratch that, new idea
----------------------

Build a list of Node objects
    Nodes know their pre-requisite nodes (prev)
    and which nodes they are pre-requisites of (next)
Identify leaf nodes as those nodes with no prev
Set leaf nodes to available
Loop:
    Given available nodes, schedule / resolve first
        For each of the scheduled_node's next_nodes
            Remove scheduled_node from their prev
    Update list of available - all nodes with no prev

Part 2
------
A worker is an object that either points to a Node or points to nothing (idle)
and chips away at the Node's cost at each timestep in a loop

Main Loop:
    For each idle worker:
        assign to any available

        complete 1 second of work

        if no seconds of work left, make idle
"""
import re
from copy import deepcopy
from string import ascii_uppercase
from typing import Dict, List, Set


LETTER_COST = {letter: (i + 1) for i, letter in enumerate(ascii_uppercase)}


class Node:
    def __init__(self,
                 name: str,
                 prev: Set[str] = None,
                 next: Set[str] = None):
        self.name = name
        self.cost = LETTER_COST[name]
        self.prev = prev if prev is not None else set()
        self.next = next if next is not None else set()

    def __repr__(self):
        return f'Node({self.name},' \
               f'cost={self.cost},' \
               f'prev={self.prev},' \
               f'next={self.next})'

    def update(self):
        self.cost -= 1
        if self.cost < 0:
            raise RuntimeError('cost must not be less than zero')


def parse_nodes(lines: List[str]) -> Dict[str, Node]:
    pattern = re.compile(
        r'^Step ([A-Z]) must be finished before step ([A-Z]) can begin.$')
    nodes: Dict[str, Node] = {}
    for line in lines:
        req, target = re.match(pattern, line.strip()).groups()

        if req not in nodes:
            nodes[req] = Node(req)
        nodes[req].next.add(target)

        if target not in nodes:
            nodes[target] = Node(target)
        nodes[target].prev.add(req)

    return nodes


def leaf_nodes(nodes: Dict[str, Node]) -> List[str]:
    return [name for name, node in nodes.items() if not node.prev]


def schedule_nodes(nodes: Dict[str, Node]) -> List[str]:
    nodes = deepcopy(nodes)
    schedule = []
    available = sorted(leaf_nodes(nodes))
    while available:
        scheduled = available[0]
        scheduled_node = nodes.pop(scheduled)

        for name in scheduled_node.next:
            node = nodes[name]
            node.prev.discard(scheduled)

        available = sorted(leaf_nodes(nodes))

        schedule.append(scheduled)

    return schedule


def multi_schedule_nodes(nodes: Dict[str, Node],
                         num_workers: int,
                         base_cost: int) -> int:

    for _, node in nodes.items():
        node.cost += base_cost

    workers = [id for id in range(num_workers)]
    jobs = {id: None for id in workers}

    available = sorted(leaf_nodes(nodes))
    done: List[str] = []
    time = 0

    msg = 'Second  '
    for id in workers:
        msg += f'Worker {id}  '
    msg += 'Done'
    print(msg)

    while True:
        # Schedule jobs to idle workers
        idle_workers = [id for id, node in jobs.items() if node is None]
        for worker in idle_workers:
            if not available:
                break
            jobs[worker] = available.pop(0)

        # Logging
        msg = f'{time:4d}    '
        sorted_job_nodes = [jobs[id] for id in workers]
        for node in sorted_job_nodes:
            if node is None:
                node = '.'
            msg += f' {node:^8} '
        done_str = ''.join(done)
        msg += done_str
        print(msg)

        if not nodes:
            break

        # Apply work: reduce each job node's cost by 1
        active_workers = [id for id, node in jobs.items() if node is not None]
        for worker in active_workers:
            name = jobs[worker]
            node = nodes[name]
            node.update()

            # If node is completed, update graph
            if node.cost == 0:
                # Set worker to idle
                jobs[worker] = None
                # Remove this node from the list
                nodes.pop(name)
                done.append(name)
                # Remove this node from next node's state
                for next_name in node.next:
                    next_node = nodes[next_name]
                    next_node.prev.discard(name)

        scheduled = jobs.values()
        available = [name for name in sorted(leaf_nodes(nodes))
                     if name not in scheduled]
        # print(nodes)

        time += 1

    return time


test_lines = """Step C must be finished before step A can begin.
                Step C must be finished before step F can begin.
                Step A must be finished before step B can begin.
                Step A must be finished before step D can begin.
                Step B must be finished before step E can begin.
                Step D must be finished before step E can begin.
                Step F must be finished before step E can begin.""".split('\n')
test_nodes = parse_nodes(test_lines)
assert leaf_nodes(test_nodes) == ['C']
assert ''.join(schedule_nodes(test_nodes)) == 'CABDFE'
assert multi_schedule_nodes(test_nodes, 2, 0) == 15

if __name__ == '__main__':
    with open('data/day_07.txt') as f:
        nodes = parse_nodes(f.readlines())
    print(''.join(schedule_nodes(nodes)))
    print(multi_schedule_nodes(nodes, 5, 60))
