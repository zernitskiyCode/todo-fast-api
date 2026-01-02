from database.db import get_db_connection

def init_db():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT True)
        """)
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS task(
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            deadline TIMESTAMP,
            priority INTEGER DEFAULT 2,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            tag TEXT NOT NULL)
        """)
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS task_users(
            id SERIAL PRIMARY KEY,
            task_id INTEGER NOT NULL REFERENCES task(id),
            user_id INTEGER NOT NULL REFERENCES users(id))
        """)
        db.commit()
        cursor.close()
        db.close()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
