from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import NewType

Valve = NewType("Valve", str)


@dataclass
class Scan:
    flow_rates: dict[Valve, int]
    tunnels: dict[Valve, list[Valve]]


def parse_scan(lines: list[str]) -> Scan:
    flow_rates = {}
    tunnels = {}

    for line in lines:
        parts = line.split()
        valve = Valve(parts[1])
        flow_rates[valve] = int(parts[4][5:].strip(";"))
        tunnels[valve] = [Valve(v.strip(",")) for v in parts[9:]]

    return Scan(flow_rates, tunnels)


def simulate_part_1(s: Scan) -> int:
    @lru_cache(maxsize=None)
    def step(at: Valve, time_left: int, seen: tuple[Valve, ...]) -> int:
        if time_left <= 1:
            return 0

        if_skip = max(step(dst, time_left - 1, seen) for dst in s.tunnels[at])
        outcomes = [if_skip]

        rate = s.flow_rates[at]
        if rate and at not in seen:
            seen = (*seen, at)
            win = rate * (time_left - 1)
            if_open = win + max(step(dst, time_left - 2, seen) for dst in s.tunnels[at])
            outcomes.append(if_open)

        return max(outcomes)

    return step(at=Valve("AA"), time_left=30, seen=())


lines = Path("input.txt").read_text().splitlines()
s = parse_scan(lines)
print("Part 1:", simulate_part_1(s))
