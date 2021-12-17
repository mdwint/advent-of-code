# Sample:
# tx0, tx1, ty0, ty1 = 20, 30, -10, -5

# Input:
tx0, tx1, ty0, ty1 = 209, 238, -86, -59

x_clip = max(tx0, tx1)
y_clip = min(ty0, ty1)


def sign(x: int) -> int:
    return (1 if x > 0 else -1) if x else 0


def simulate(dx: int, dy: int):
    start = dx, dy
    x, y = 0, 0
    max_y = y
    hit = False
    while True:
        x += dx
        y += dy
        dx -= sign(dx)
        dy -= 1
        max_y = max(y, max_y)
        if tx0 <= x <= tx1 and ty0 <= y <= ty1:
            hit = True
            break
        if dx > 0 and x > x_clip or dy < 0 and y < y_clip:
            break
    if hit:
        print(start, "->", (x, y), max_y)
    return max_y if hit else 0, hit


velocities = [(dx, dy) for dx in range(0, 400) for dy in range(-200, 200)]
results = [simulate(*vel) for vel in velocities]

print("Part 1:", max(results)[0])
print("Part 2:", sum(1 for _, hit in results if hit))
