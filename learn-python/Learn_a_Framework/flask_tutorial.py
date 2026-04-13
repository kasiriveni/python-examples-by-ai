"""
Learn a Framework: Flask web framework tutorial.
"""

# === Flask Application Examples ===
# NOTE: Requires `pip install flask`

FLASK_BASIC = '''
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# === Basic routes ===
@app.route("/")
def home():
    return "<h1>Hello, Flask!</h1>"

@app.route("/about")
def about():
    return jsonify({"app": "Flask Tutorial", "version": "1.0"})

# === Dynamic routes ===
@app.route("/user/<username>")
def user_profile(username):
    return f"<h1>Profile: {username}</h1>"

@app.route("/post/<int:post_id>")
def show_post(post_id):
    return jsonify({"post_id": post_id, "title": f"Post {post_id}"})

# === HTTP Methods ===
@app.route("/api/items", methods=["GET", "POST"])
def items():
    if request.method == "POST":
        data = request.get_json()
        return jsonify({"created": data}), 201
    return jsonify({"items": ["item1", "item2"]})

# === Templates ===
TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/page")
def page():
    return render_template_string(
        TEMPLATE,
        title="My Items",
        items=["Python", "Flask", "HTML"]
    )

# === Error handlers ===
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''

# === Flask with database (SQLAlchemy) ===
FLASK_WITH_DB = '''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

with app.app_context():
    db.create_all()

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([t.to_dict() for t in todos])

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    todo = Todo(title=data["title"])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.done = data.get("done", todo.done)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return "", 204
'''

# === Flask blueprints ===
FLASK_BLUEPRINTS = '''
from flask import Flask, Blueprint, jsonify

# Define blueprints
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
api_bp = Blueprint("api", __name__, url_prefix="/api")

@auth_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"token": "abc123"})

@auth_bp.route("/logout")
def logout():
    return jsonify({"message": "Logged out"})

@api_bp.route("/users")
def get_users():
    return jsonify({"users": []})

# Register blueprints
app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
'''

if __name__ == "__main__":
    sections = [
        ("Basic Flask App", FLASK_BASIC),
        ("Flask with Database", FLASK_WITH_DB),
        ("Flask Blueprints", FLASK_BLUEPRINTS),
    ]

    for title, code in sections:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        print(code)
