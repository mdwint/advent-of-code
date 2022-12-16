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


def simulate(s: Scan, total_time: int, actors: int) -> int:
    start = Valve("AA")

    @lru_cache(maxsize=None)
    def step(at: Valve, time_left: int, opened: tuple[Valve, ...], others: int) -> int:
        if time_left <= 1:
            return step(start, total_time, opened, others - 1) if others else 0

        if_skip = max(step(dst, time_left - 1, opened, others) for dst in s.tunnels[at])
        outcomes = [if_skip]

        rate = s.flow_rates[at]
        if rate and at not in opened:
            opened = tuple(sorted((*opened, at)))
            if_open = rate * (time_left - 1) + max(
                step(dst, time_left - 2, opened, others) for dst in s.tunnels[at]
            )
            outcomes.append(if_open)

        return max(outcomes)

    return step(start, total_time, opened=(), others=actors - 1)


lines = Path("input.txt").read_text().splitlines()
s = parse_scan(lines)
print("Part 1:", simulate(s, total_time=30, actors=1))
print("Part 2:", simulate(s, total_time=26, actors=2))
