# app.py
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # ❌ LỖ HỔNG SQL INJECTION
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return "Login thành công!"
    else:
        return "Sai tài khoản hoặc mật khẩu!"

app.run(debug=True)