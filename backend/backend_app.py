from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

POSTS = [
    {
        "id": 1,
        "title": "First post",
        "content": "This is the first post.",
        "author": "Alice",
        "date": "2025-09-01"
    },
    {
        "id": 2,
        "title": "Second post",
        "content": "This is the second post.",
        "author": "Bob",
        "date": "2025-09-05"
    },
]

def get_next_id():
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    return 1

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = POSTS.copy()
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    if sort_field:
        if sort_field not in ['title', 'content', 'author', 'date']:
            return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400
        reverse = direction == 'desc'
        if sort_field == 'date':
            posts.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=reverse)
        else:
            posts.sort(key=lambda x: x[sort_field], reverse=reverse)
    return jsonify(posts), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    missing_fields = [field for field in ['title', 'content', 'author', 'date'] if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields)}"}), 400

    new_post = {
        "id": get_next_id(),
        "title": data['title'],
        "content": data['content'],
        "author": data['author'],
        "date": data['date']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    for field in ['title', 'content', 'author', 'date']:
        if field in data:
            post[field] = data[field]

    return jsonify(post), 200

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    POSTS = [p for p in POSTS if p['id'] != post_id]
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_q = request.args.get('title', '').lower()
    content_q = request.args.get('content', '').lower()
    author_q = request.args.get('author', '').lower()
    date_q = request.args.get('date', '').lower()

    results = [
        p for p in POSTS
        if title_q in p['title'].lower()
        or content_q in p['content'].lower()
        or author_q in p['author'].lower()
        or date_q in p['date']
    ]
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
