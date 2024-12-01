from collections import deque

from aoc import read_input


def mix(numbers: list[int], rounds: int = 1) -> int:
    q = deque(enumerate(numbers))
    n = len(numbers)

    for _ in range(rounds):
        for i in range(n):
            # Rotate to the i-th item:
            dist = next(d for (d, (j, _)) in enumerate(q) if j == i)
            q.rotate(-dist)

            item = q.popleft()
            q.rotate(-item[1])
            q.append(item)

    numbers = [x for _, x in q]
    z = numbers.index(0)
    return sum(numbers[(z + d) % n] for d in (1000, 2000, 3000))


numbers = [int(x) for x in read_input().splitlines()]
print("Part 1:", mix(numbers))

numbers = [x * 811589153 for x in numbers]
print("Part 2:", mix(numbers, rounds=10))
