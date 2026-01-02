from database.models import init_db

from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
from database.crud import create_user, create_task_list
from schemas import UserCreate, TaskCreate

if __name__ == "__main__":
    init_db()
    print("База данных запущена.")

app = FastAPI()



# Регистрация пользователя
@app.post("/register")
def register(user: UserCreate):
    user_id = create_user(user.username, user.email, user.password)
    return {"message" : "Пользователь создан. " , "user_id" : user_id}
# Создания задачи
@app.post("/task")
def task(task: TaskCreate, id: int):
    task_id = create_task_list(task, id)
    return {"message": "Task created", "task_id": task_id}