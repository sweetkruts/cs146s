from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    
    if not data.get('title') or not data['title'].strip():
        return jsonify({'error': 'Title is required'}), 400
    
    if len(data['title']) > 200:
        return jsonify({'error': 'Title must be 200 characters or less'}), 400
    
    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)',
        (data['title'], data.get('description', ''), data.get('completed', False))
    )
    conn.commit()
    task_id = cursor.lastrowid
    
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(task)), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(dict(task))

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    conn = get_db()
    
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    if not data.get('title') or not data['title'].strip():
        conn.close()
        return jsonify({'error': 'Title is required'}), 400
    
    if len(data['title']) > 200:
        conn.close()
        return jsonify({'error': 'Title must be 200 characters or less'}), 400
    
    conn.execute(
        'UPDATE tasks SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (data['title'], data.get('description', ''), data.get('completed', False), task_id)
    )
    conn.commit()
    
    updated_task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(updated_task))

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return '', 204

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

