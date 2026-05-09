import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Render provides DATABASE_URL automatically if we link a database
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for local development
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "tts_db")

def get_db_connection():
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
        else:
            conn = psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    voice VARCHAR(255) NOT NULL,
                    file_path VARCHAR(255) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error initializing database: {e}")

def log_request(text, voice, file_path):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO requests (text, voice, file_path)
                VALUES (%s, %s, %s)
            ''', (text, voice, file_path))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error logging request: {e}")

def get_recent_requests(limit=10):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT text, voice, file_path, timestamp FROM requests
                ORDER BY timestamp DESC
                LIMIT %s
            ''', (limit,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print(f"Error fetching history: {e}")
            return []
    return []

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
