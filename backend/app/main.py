from database.models import init_db

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
from database.crud import create_user, create_task, authenticate_user, get_user_tasks
from schemas import UserCreate, TaskCreate, UserLogin

if __name__ == "__main__":
    init_db()
    print("База данных запущена.")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены (или укажи конкретный домен)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.post("/login")
def login(user: UserLogin):
    user_id = authenticate_user(user)
    return {"message": "Login successful", "user_id": user_id}


# Регистрация пользователя
@app.post("/register")
def register(user: UserCreate):
    user_id = create_user(user.username, user.email, user.password)
    return {"message" : "Пользователь создан. " , "user_id" : user_id}
# Создания задачи
@app.post("/task")
def task(task: TaskCreate):
    task_id = create_task(task, id)
    return {"message": "Task created", "task_id": task_id}
# получение задач
@app.get("/tasks/{user_id}")
def get_user_tasks_endpoint(user_id: int):
    tasks = get_user_tasks(user_id)
    return {"tasks": tasks}