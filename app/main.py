from fastapi import FastAPI, Response, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import app.routes.users as users

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)

index_html_file_path = Path("static/index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    return HTMLResponse(content=index_html_file_path.read_text(), status_code=200)
