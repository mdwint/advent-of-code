import sys
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

text = Path(sys.argv[1]).read_text().strip()

Mat = str
Costs = dict[Mat, int]
Blueprint = dict[Mat, Costs]

blueprints: list[Blueprint] = []
for i, line in enumerate(text.splitlines()):
    bp = {}
    for sentence in line.split(":")[1].rstrip(".").split(". "):
        prefix, suffix = sentence.split(" costs ")
        robot_type = prefix.split()[1]
        costs = {}
        for cost in suffix.split(" and "):
            n, material = cost.split()
            costs[material] = int(n)
        bp[robot_type] = costs
    blueprints.append(bp)


def hashable(d: dict) -> tuple:
    return tuple(sorted(d.items()))


def simulate(bp: Blueprint, total_time: int) -> int:
    Mats = tuple[tuple[Mat, int]]

    @lru_cache(maxsize=None)
    def step(time_left: int, robots: Mats, resources: Mats) -> int:
        # print(time_left, robots, resources)

        res: dict[Mat, int] = defaultdict(int)
        res.update(resources)

        assert time_left >= 0
        if not time_left:
            return res.get("geode", 0)

        outcomes = []

        if robots:
            _res = deepcopy(res)
            for mat, n in robots:
                _res[mat] += n

            s = step(time_left - 1, robots, hashable(_res))
            outcomes.append(s)

        can_build = [
            typ
            for typ, costs in bp.items()
            if all(res[mat] >= cost for mat, cost in costs.items())
        ]
        for pref in ("geode", "obsidian"):
            if pref in can_build:
                can_build = [pref]

        rob: dict[Mat, int] = defaultdict(int)
        rob.update(robots)

        for typ in can_build:
            _rob = deepcopy(rob)
            _res = deepcopy(res)
            for mat, cost in bp[typ].items():
                _res[mat] -= cost
            for mat, n in _rob.items():
                _res[mat] += n
            _rob[typ] += 1

            s = step(time_left - 1, hashable(_rob), hashable(_res))
            outcomes.append(s)

        return max(outcomes)

    score = step(total_time, robots=(("ore", 1),), resources=())
    print(score, bp)
    return score


s = sum(simulate(bp, total_time=24) * i for i, bp in enumerate(blueprints, start=1))
print("Part 1:", s)
