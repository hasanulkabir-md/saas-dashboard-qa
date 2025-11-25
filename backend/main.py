# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3

DB_NAME = "dashboard.db"

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Or: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],            # <-- IMPORTANT (allows OPTIONS)
    allow_headers=["*"],
)


def init_db():
    """
    Initialize SQLite database and create users table if not exists.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()


# Run DB setup on app startup
init_db()


class User(BaseModel):
    name: str
    email: EmailStr   # Validates email format automatically


@app.post("/user/create")
def create_user(user: User):
    """
    Create a user in SQLite DB.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email),
        )
        conn.commit()
        return {"message": "User created"}

    except sqlite3.IntegrityError:
        return {"error": "Email already exists"}

    finally:
        conn.close()


@app.get("/user/list")
def list_users():
    """
    List all users from SQLite DB.
    """
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT id, name, email FROM users"
    ).fetchall()
    conn.close()

    return [
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ]
