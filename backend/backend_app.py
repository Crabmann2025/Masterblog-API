from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

# Helper function to generate the next unique ID
def get_next_id():
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    return 1

# GET endpoint: list all posts with optional sorting
@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    valid_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    if sort_field and sort_field not in valid_fields:
        return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400
    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction: {direction}"}), 400

    posts = POSTS.copy()
    if sort_field:
        reverse = direction == 'desc'
        posts.sort(key=lambda x: x[sort_field].lower(), reverse=reverse)

    return jsonify(posts), 200

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

# DELETE endpoint: delete a post by id
@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_to_delete = next((post for post in POSTS if post['id'] == id), None)
    if not post_to_delete:
        return jsonify({"error": f"Post with id {id} not found"}), 404
    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

# PUT endpoint: update a post by id
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    post_to_update = next((post for post in POSTS if post['id'] == id), None)
    if not post_to_update:
        return jsonify({"error": f"Post with id {id} not found"}), 404
    if data.get('title') is not None:
        post_to_update['title'] = data['title']
    if data.get('content') is not None:
        post_to_update['content'] = data['content']
    return jsonify(post_to_update), 200

# SEARCH endpoint: search posts by title or content
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    results = []
    for post in POSTS:
        if (title_query in post['title'].lower()) or (content_query in post['content'].lower()):
            results.append(post)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
