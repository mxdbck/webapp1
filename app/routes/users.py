from fastapi import APIRouter, Form, Response, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
from pathlib import Path
from app.db import get_db, DATABASE

import os
from dotenv import load_dotenv

load_dotenv()
REGISTRATION_SECRET = os.getenv("REGISTRATION_SECRET")

router = APIRouter()

protected_html_file_path = Path("static/protected.html")

@router.post("/register")
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    text_field: str = Form(...),
    secret: str = Form(...)
):
    # Check if the provided secret matches the one in the .env file
    if secret != REGISTRATION_SECRET:
        raise HTTPException(status_code=400, detail="Invalid registration secret!")

    conn = get_db()
    cursor = conn.cursor()

    print(f"Registering user {username}...")

    try:
        cursor.execute('INSERT INTO users (username, password, text_field) VALUES (?, ?, ?)',
                       (username, password, text_field))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

    return {"message": f"User {username} registered successfully!"}

@router.post("/login")
async def login_user(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Query to check if the user exists and password matches
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        # Set a cookie upon successful login
        response.set_cookie(key="mycookie", value=username, httponly=False)
        return {"message": "Login successful! Cookie set!"}
    else:
        return {"error": "Invalid username or password"}

# Protected route, accessible only if the cookie is set
@router.get("/protected", response_class=HTMLResponse)
async def protected_route(request: Request):
    cookie_value = request.cookies.get("mycookie")

    if not cookie_value:
        return RedirectResponse(url="/")

    # Connect to the database and retrieve the user data based on the username in the cookie
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT text_field FROM users WHERE username = ?
    ''', (cookie_value,))

    user_text = cursor.fetchone()
    conn.close()

    if user_text:
        return HTMLResponse(content=protected_html_file_path.read_text())
    else:
        return HTMLResponse(content="You are not authorized to access this page!", status_code=403)

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="mycookie")
    return {"message": "Logged out!"}
