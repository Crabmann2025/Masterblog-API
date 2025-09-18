from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample list of blog posts
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

# Helper function to generate the next unique ID
def get_next_id():
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    return 1

# GET endpoint: list all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS), 200

# POST endpoint: add a new post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # Check if title and content are provided
    if not data or 'title' not in data or 'content' not in data:
        missing_fields = []
        if not data or 'title' not in data:
            missing_fields.append('title')
        if not data or 'content' not in data:
            missing_fields.append('content')
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields)}"}), 400

    # Create the new post
    new_post = {
        "id": get_next_id(),
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
