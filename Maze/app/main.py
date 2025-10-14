from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes import router as maze_router

app = FastAPI(title="Maze Game")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(maze_router)


@app.get("/", response_class=HTMLResponse)
async def index(_: Request):
    index_file = TEMPLATES_DIR / "index.html"
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# API endpoint to generate maze is added later in maze endpoints


