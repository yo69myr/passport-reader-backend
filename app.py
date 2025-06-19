from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import uuid

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    login = data['login']
    password = data['password']
    subscription = 'active'  # За замовчуванням активна підписка

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (login, password, creation_date, subscription) VALUES (?, ?, ?, ?)',
                   (login, password, datetime.now(), subscription))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data['login']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
    if user:
        token = str(uuid.uuid4())  # Генеруємо унікальний токен
        cursor.execute('UPDATE users SET token = ? WHERE id = ?', (token, user['id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Login successful', 'subscription': user['subscription'], 'token': token}), 200
    else:
        conn.close()
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/check_token', methods=['POST'])
def check_token():
    data = request.json
    login = data['login']
    token = data['token']

    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT token FROM users WHERE login = ?', (login,)).fetchone()
    conn.close()

    if user and user['token'] == token:
        return jsonify({'message': 'Token valid'}), 200
    else:
        return jsonify({'message': 'Token invalid'}), 403

if __name__ == '__main__':
    app.run(debug=True)
