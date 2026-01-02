from database.db import get_db_connection
from fastapi import HTTPException
import psycopg2
from schemas import UserCreate, TaskCreate, UserLogin

# добавить позже хеширование и валидацию
# создание пользователя
def create_user(user : UserCreate):
    db = get_db_connection()
    cursor = db.cursor()
    # 1. Проверяем существует ли такой пользователь
    cursor.execute("""
    SELECT id FROM users WHERE email = %s""", (user.email))
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

# Авторизация
def authenticate_user(user: UserLogin):
    db = get_db_connection()
    cursor = db.cursor()
    # 1. Проверяем существует ли такой пользователь 
    cursor.execute("""
        SELECT id FROM users WHERE email = %s AND password = %s""", (user.email, user.password))
    db_user = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return db_user[0]


# создание задачи
def create_task(task: TaskCreate, id: int):
    db = get_db_connection()
    cursor = db.cursor()
    # 1. Проверяем существует ли такой пользователь
    cursor.execute("""SELECT id FROM users WHERE id = %s""", (id,))
    if not cursor.fetchone:
        db.close
        cursor.close
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    # 2. Вставляем задачу в бд
    cursor.execute("""
    INSERT INTO task(title, description, deadline, priority, tag) VALUES(%s, %s, %s, %s, %s) RETURNING id  """, (id, task.title, task.description, task.deadline, task.priority, task.tag))
    task_id = cursor.fetchone()[0]
    cursor.execute("""
            INSERT INTO task_users (task_id, user_id)
            VALUES (%s, %s)
        """, (task_id, task.user_id))
    db.close()
    cursor.close()
    return task_id
# получение списка задач
def get_user_tasks(user_id: int):
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT t.id, t.title, t.description, t.deadline, t.priority, t.tag
            FROM task t
            JOIN task_users tu ON t.id = tu.task_id
            WHERE tu.user_id = %s
        """, (user_id,))

        tasks = cursor.fetchall()
        cursor.close()
        db.close()
        return tasks