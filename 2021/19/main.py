import itertools
import math

import numpy as np

RAD_90 = math.pi / 2


def rotation_matrix(axis: int, angle: float) -> np.array:
    assert abs(angle) % RAD_90 == 0
    c = round(math.cos(angle))
    s = round(math.sin(angle))
    if axis == 0:
        m = [
            [1, 0, 0],
            [0, c, -s],
            [0, s, c],
        ]
    elif axis == 1:
        m = [
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c],
        ]
    elif axis == 2:
        m = [
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1],
        ]
    else:
        raise ValueError(axis)
    return np.array(m)


# Generate rotation matrices and eliminate duplicates:
matrices = []
for turns_xyz in itertools.product(range(4), repeat=3):
    rot_x, rot_y, rot_z = (
        rotation_matrix(axis, angle=RAD_90 * turns)
        for axis, turns in enumerate(turns_xyz)
    )
    matrices.append(rot_x @ rot_y @ rot_z)
matrices = [np.array(t) for t in {tuple(map(tuple, m)) for m in matrices}]
assert len(matrices) == 24


def main():
    with open("input.txt") as f:
        text = f.read()

    groups_todo = [
        [np.array([int(x) for x in line.split(",")]) for line in block.splitlines()[1:]]
        for block in text.split("\n\n")
    ]
    found_scanners = [(0, 0, 0)]
    found_beacons = {tuple(v) for v in groups_todo.pop(0)}

    while groups_todo:
        gid, scanner, beacons = find(groups_todo, found_beacons)
        found_scanners.append(scanner)
        found_beacons.update(beacons)
        groups_todo.pop(gid)

    print("Part 1:", len(found_beacons))
    max_distance = max(
        abs(x1 - x0) + abs(y1 - y0) + abs(z1 - z0)
        for x0, y0, z0 in found_scanners
        for x1, y1, z1 in found_scanners
    )
    print("Part 2:", max_distance)


def find(groups_todo, found_beacons):
    for ref_origin in found_beacons:
        ref_origin = np.array(ref_origin)
        for gid, group in enumerate(groups_todo):
            for m in matrices:
                rotated = [m @ v for v in group]
                for origin in rotated:
                    delta = origin - ref_origin
                    beacons = {tuple(v - delta) for v in rotated}
                    matches = beacons.intersection(found_beacons)
                    if len(matches) >= 12:
                        scanner = tuple(-delta)
                        return gid, scanner, beacons

    raise ValueError("No matches")


if __name__ == "__main__":
    main()
