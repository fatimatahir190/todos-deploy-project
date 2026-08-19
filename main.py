from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)


class Todo(BaseModel):
    title: str
    description: str
    is_completed: bool


@app.post("/todos")
def create_todo(todo: Todo):

    data = {
        "title": todo.title,
        "description": todo.description,
        "is_completed": todo.is_completed
    }

    response = supabase.table("todos").insert(data).execute()

    return response.data


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):

    response = supabase.table("todos").update({
        "title": todo.title,
        "description": todo.description,
        "is_completed": todo.is_completed
    }).eq("id", todo_id).execute()

    return response.data


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    response = supabase.table("todos").delete().eq(
        "id", todo_id
    ).execute()

    return response.data


@app.get("/todos")
def get_todos():

    response = supabase.table("todos").select("*").execute()

    return response.data
