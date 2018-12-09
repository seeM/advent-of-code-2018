"""
Task 1
------
Keep a Counter of player scores

Marble number == tick / turn in simulation

Simulation loop:
    If marble_num is divisable by 23:
        Add marble_num to players score
        Remove marble 7 left of `current`
          & add to score
          & set `current` 1 right of it
    Else:
        Append to _circular_ list two indices right of `current`

'Last Marble is worth X points' means run the loop for X turns / until marble number X
"""
from collections import Counter
from typing import List, Optional


def marble_mania(players: int,
                 marbles: int) -> Counter:

    player_scores: Counter = Counter()
    circle = [0]
    for marble in range(1, marbles + 1):
        if not marble % 23:
            player = player_from_turn(marble, players)

            for _ in range(7):
                circle = rshift(circle)
            bonus = circle.pop(0)

            player_scores[player] += (marble + bonus)
        else:
            circle = append(marble, circle)

    return player_scores


def player_from_turn(turn: int, players: int) -> Optional[int]:
    return (turn - 1) % players + 1 if turn > 0 else None


def lshift(array: List) -> List:
    """
    Example
    -------
    >>> lshift([0, 1, 2, 3, 4])
    [1, 2, 3, 4, 0]
    >>> lshift([0])
    [0]
    >>> lshift([])
    []
    """
    return (array[1:] + [array[0]]) if len(array) > 1 else array


def rshift(array: List) -> List:
    return ([array[-1]] + array[:-1]) if len(array) > 1 else array


def append(x: int, array: List[int]) -> List[int]:
    array = lshift(array)
    array = lshift(array)
    array.append(x)
    array = rshift(array)
    return array


def high_score(scores: Counter) -> int:
    return scores.most_common(1)[0][1]


assert high_score(marble_mania(10, 1618)) == 8317
assert high_score(marble_mania(13, 7999)) == 146373
assert high_score(marble_mania(17, 1104)) == 2764
assert high_score(marble_mania(21, 6111)) == 54718
assert high_score(marble_mania(30, 5807)) == 37305


if __name__ == '__main__':
    scores = marble_mania(400, 71864)
    print(high_score(scores))
