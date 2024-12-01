from pathlib import Path


def find_marker(data: str, width: int) -> int:
    for start in range(len(data)):
        end = start + width
        if len(set(data[start:end])) == width:
            return end
    return -1


data = Path("input.txt").read_text()
print("Part 1:", find_marker(data, 4))
print("Part 2:", find_marker(data, 14))
