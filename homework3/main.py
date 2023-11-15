import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask("homework3")
CORS(app, resources=r'/api/*')

DATABASE = "/Users/andrewchris/Desktop/Homework Web/DB/database.db"

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route('/follows', methods=['GET'])
def get_follows():
    with get_db() as db:
        follows = db.execute('SELECT * FROM follows').fetchall()
    return jsonify([dict(row) for row in follows])

@app.route('/follows/<int:id>', methods=['GET'])
def get_follow(id):
    with get_db() as db:
        follow = db.execute('SELECT * FROM follows WHERE id = ?', (id,)).fetchone()
    if follow:
        return jsonify(dict(follow))
    else:
        return jsonify({'message': 'Follow not found'}), 404

@app.route('/follows', methods=['POST'])
def create_follow():
    data = request.json
    with get_db() as db:
        db.execute('INSERT INTO follows (following_user_id, followed_user_id) VALUES (?, ?)', (data['following_user_id'], data['followed_user_id']))
        db.commit()
    return jsonify({'message': 'Follow created successfully'}), 201

@app.route('/follows/<int:id>', methods=['PUT'])
def update_follow(id):
    data = request.json
    with get_db() as db:
        db.execute('UPDATE follows SET following_user_id = ?, followed_user_id = ? WHERE id = ?', (data['following_user_id'], data['followed_user_id'], id))
        db.commit()
    return jsonify({'message': 'Follow updated successfully'})

@app.route('/follows/<int:id>', methods=['DELETE'])
def delete_follow(id):
    with get_db() as db:
        db.execute('DELETE FROM follows WHERE id = ?', (id,))
        db.commit()
    return jsonify({'message': 'Follow deleted successfully'})

# Users CRUD operations

@app.route('/users', methods=['GET'])
def get_users():
    with get_db() as db:
        users = db.execute('SELECT * FROM users').fetchall()
    return jsonify([dict(row) for row in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    with get_db() as db:
        user = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    with get_db() as db:
        db.execute('INSERT INTO users (username, role) VALUES (?, ?)', (data['username'], data.get('role', '')))
        db.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    with get_db() as db:
        db.execute('UPDATE users SET username = ?, role = ? WHERE id = ?', (data['username'], data.get('role', ''), id))
        db.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    with get_db() as db:
        db.execute('DELETE FROM users WHERE id = ?', (id,))
        db.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/posts', methods=['GET'])
def get_posts():
    with get_db() as db:
        posts = db.execute('SELECT * FROM posts').fetchall()
    return jsonify([dict(row) for row in posts])

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    with get_db() as db:
        post = db.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if post:
        return jsonify(dict(post))
    else:
        return jsonify({'message': 'Post not found'}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    with get_db() as db:
        db.execute('INSERT INTO posts (title, body, user_id, status) VALUES (?, ?, ?, ?)',
                   (data['title'], data['body'], data['user_id'], data.get('status', '')))
        db.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.json
    with get_db() as db:
        db.execute('UPDATE posts SET title = ?, body = ?, user_id = ?, status = ? WHERE id = ?',
                   (data['title'], data['body'], data['user_id'], data.get('status', ''), id))
        db.commit()
    return jsonify({'message': 'Post updated successfully'})

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    with get_db() as db:
        db.execute('DELETE FROM posts WHERE id = ?', (id,))
        db.commit()
    return jsonify({'message': 'Post deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
