import json

def load_seed(path="contributions.json"):
    with open(path) as f:
        grid = json.load(f)
    # any day with 1+ contributions starts "alive"
    return [[1 if cell > 0 else 0 for cell in row] for row in grid]

def count_neighbors(grid, x, y):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                count += grid[nx][ny]
    return count

def step(grid):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    for x in range(rows):
        for y in range(cols):
            alive = grid[x][y]
            n = count_neighbors(grid, x, y)
            if alive and n in (2, 3):
                new_grid[x][y] = 1
            elif not alive and n == 3:
                new_grid[x][y] = 1
    return new_grid

def generate_frames(seed, generations=20):
    frames = [seed]
    current = seed
    for _ in range(generations):
        current = step(current)
        frames.append(current)
    return frames
