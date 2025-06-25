# app.py
from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
def create_admin():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # User already exists
    conn.close()

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return "Login thành công!"
    else:
        return "Sai tài khoản hoặc mật khẩu!"
    
@app.route('/')
def index():
    return "Chào mừng đến với ứng dụng Flask!"

init_db()
create_admin()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    
    