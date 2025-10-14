from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import random


Cell = Tuple[int, int]


@dataclass
class Maze:
    width: int
    height: int
    grid: List[List[int]]  # 0 = wall, 1 = path


def generate_maze(width: int, height: int, seed: int | None = None) -> Maze:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    rng = random.Random(seed)

    grid = [[0 for _ in range(width)] for _ in range(height)]

    def neighbors(cell: Cell) -> List[Tuple[Cell, Cell]]:
        r, c = cell
        options: List[Tuple[Cell, Cell]] = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 1 <= nr < height - 1 and 1 <= nc < width - 1:
                wall = (r + dr // 2, c + dc // 2)
                options.append(((nr, nc), wall))
        return options

    start: Cell = (1, 1)
    grid[start[0]][start[1]] = 1

    stack: List[Cell] = [start]
    visited = {start}

    while stack:
        current = stack[-1]
        unvisited = [(n, w) for n, w in neighbors(current) if n not in visited]
        if not unvisited:
            stack.pop()
            continue
        (next_cell, wall_cell) = rng.choice(unvisited)
        # carve wall
        wr, wc = wall_cell
        grid[wr][wc] = 1
        nr, nc = next_cell
        grid[nr][nc] = 1
        visited.add(next_cell)
        stack.append(next_cell)

    return Maze(width=width, height=height, grid=grid)


def complexity_to_size(level: int) -> Tuple[int, int]:
    # level 1..4 -> progressively larger and tighter mazes
    mapping = {
        1: (21, 15),
        2: (31, 21),
        3: (41, 31),
        4: (55, 41),
    }
    return mapping.get(level, mapping[2])


