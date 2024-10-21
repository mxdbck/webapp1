from fastapi import FastAPI, Response, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import app.routes.users as users

from fastapi.templating import Jinja2Templates

# Point Jinja2 to the "templates" folder
templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)


index_html_file_path = Path("static/index.html")

@app.get("/")
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
