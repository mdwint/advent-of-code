from pathlib import Path

ROCK, PAPER, SCISSORS = LOSE, DRAW, WIN = 1, 2, 3

BEATS = {
    ROCK: PAPER,
    PAPER: SCISSORS,
    SCISSORS: ROCK,
}
LOSES = {y: x for x, y in BEATS.items()}


def parse(move: str, offset: str) -> int:
    return ord(move) - ord(offset) + 1


text = Path("input.txt").read_text()
moves = []
for line in text.splitlines():
    a, x = line.split()
    moves.append((parse(a, "A"), parse(x, "X")))


def outcome(they: int, me: int) -> int:
    if they == me:
        return DRAW
    if BEATS[they] == me:
        return WIN
    return LOSE


def choice(they: int, outcome: int) -> int:
    if outcome == WIN:
        return BEATS[they]
    if outcome == LOSE:
        return LOSES[they]
    return they


def score(me: int, outcome: int) -> int:
    return me + (outcome - 1) * 3


s = sum(score(me, outcome(they, me)) for they, me in moves)
print("Part 1:", s)

s = sum(score(choice(they, outcome), outcome) for they, outcome in moves)
print("Part 2:", s)
