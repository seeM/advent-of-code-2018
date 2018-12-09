from collections import Counter, deque
from typing import List, Optional


def marble_mania(players: int,
                 marbles: int) -> Counter:

    player_scores: Counter = Counter()
    circle = deque([0], marbles)
    for marble in range(1, marbles + 1):
        if not marble % 23:
            player = player_from_turn(marble, players)

            circle.rotate(7)
            bonus = circle.popleft()

            player_scores[player] += (marble + bonus)
        else:
            circle.rotate(-2)
            circle.append(marble)
            circle.rotate(1)

    return player_scores


def player_from_turn(turn: int, players: int) -> Optional[int]:
    return (turn - 1) % players + 1 if turn > 0 else None


def high_score(scores: Counter) -> int:
    return scores.most_common(1)[0][1]


assert high_score(marble_mania(10, 1618)) == 8317
assert high_score(marble_mania(13, 7999)) == 146373
assert high_score(marble_mania(17, 1104)) == 2764
assert high_score(marble_mania(21, 6111)) == 54718
assert high_score(marble_mania(30, 5807)) == 37305


if __name__ == '__main__':
    print(high_score(marble_mania(400, 71864)))
    print(high_score(marble_mania(400, 71864 * 100)))
