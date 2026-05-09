import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "tts_db")

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    # Initial connection without database to create it if it doesn't exist
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()
        
        # Now connect to the database and create the table
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    voice VARCHAR(255) NOT NULL,
                    file_path VARCHAR(255) NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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
