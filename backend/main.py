from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS so React (3000) can call FastAPI (8000)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    name: str
    email: str


# simple in-memory "database"
users: list[User] = []


@app.post("/user/create")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}


@app.get("/user/list")
def list_users():
    return users
