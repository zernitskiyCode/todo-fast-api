from database.db import get_db_connection
from fastapi import HTTPException
import psycopg2
from schemas import UserCreate, TaskCreate

# добавить позже хеширование и валидацию
# создание пользователя
def create_user(user : UserCreate):
    db = get_db_connection()
    cursor = db.cursor()
    # 1. Проверяем существует ли такой пользователь
    cursor.execute("""
    SELECT id FROM users WHERE username = %s OR email = %s""", (user.username, user.email))
    if cursor.fetchone:
        db.close
        cursor.close
        raise HTTPException(status_code=400, detail="Пользовател с таким email уже зарегестрирован.")
    # 2. Если пользователя нет, добавляем в бд
    cursor.execute("""
    INSERT INTO users(username, email, password) VALUES (%s, %s, %s) RETURNING id""", (user.username, user.email, user.password))
    user_id = cursor.fetchone()[0]
    db.close
    cursor.close
    return user_id

# создание задачи
def create_task_list(task: TaskCreate, id: int):
    db = get_db_connection()
    cursor = db.cursor()
    # 1. Проверяем существует ли такой пользователь
    cursor.execute("""
    SELECT id FROM users WHERE id = %s""", (id))
    if not cursor.fetchone:
        db.close
        cursor.close
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    # 2. Вставляем задачу в бд
    cursor.execute("""
    INSERT INTO task(title, description, deadline, priority, tag) VALUES(%s, %s, %s, %s, %s) RETURNING id  """, (id, task.title, task.description, task.deadline, task.priority, task.tag))
    task_id = cursor.fetchone()[0]
    db.close()
    cursor.close()
    return task_id
