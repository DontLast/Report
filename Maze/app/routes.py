from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from .maze import generate_maze, complexity_to_size

router = APIRouter(prefix="/api", tags=["maze"])


@router.get("/maze")
async def get_maze(level: int = Query(1, ge=1, le=4), seed: int | None = None):
    width, height = complexity_to_size(level)
    maze = generate_maze(width=width, height=height, seed=seed)
    return JSONResponse({
        "width": maze.width,
        "height": maze.height,
        "grid": maze.grid,
        "start": [1, 1],
        "end": [maze.height - 2, maze.width - 2],
    })


