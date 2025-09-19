import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Flask App erstellen
app = Flask(
    __name__,
    static_url_path='/static',
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)
CORS(app)  # CORS für alle Routen aktivieren

# Blog Posts Liste
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

# Hilfsfunktion für nächste eindeutige ID
def get_next_id():
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    return 1

# ------------------ Endpoints ------------------

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Liste alle Posts, optional sortierbar"""
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    results = POSTS.copy()

    if sort_field:
        if sort_field not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field"}), 400
        results.sort(key=lambda x: x[sort_field], reverse=(direction == 'desc'))

    return jsonify(results), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    """Neuen Post hinzufügen"""
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        missing_fields = []
        if not data or 'title' not in data:
            missing_fields.append('title')
        if not data or 'content' not in data:
            missing_fields.append('content')
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields)}"}), 400

    new_post = {
        "id": get_next_id(),
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Post löschen"""
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Post aktualisieren"""
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Posts nach Titel oder Content durchsuchen"""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    results = [p for p in POSTS if title_query in p['title'].lower() and content_query in p['content'].lower()]
    return jsonify(results), 200

# ------------------ Swagger ------------------

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"  # JSON-Datei im Backend-static

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Masterblog API'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# ------------------ App starten ------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
