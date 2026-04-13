"""
Flask web application example.
"""
from flask import Flask, jsonify, request, abort, render_template_string

app = Flask(__name__)

# In-memory data store
todos = [
    {"id": 1, "title": "Learn Python", "done": True},
    {"id": 2, "title": "Build a web app", "done": False},
    {"id": 3, "title": "Deploy to production", "done": False},
]

# HTML template
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head><title>Todo App</title></head>
<body>
    <h1>Todo List</h1>
    <ul>
    {% for todo in todos %}
        <li>
            {{ todo.title }}
            {% if todo.done %}✅{% else %}⬜{% endif %}
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, todos=todos)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        abort(404)
    return jsonify(todo)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    if not request.json or 'title' not in request.json:
        abort(400)
    new_id = max(t['id'] for t in todos) + 1 if todos else 1
    todo = {
        'id': new_id,
        'title': request.json['title'],
        'done': False,
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    todo['title'] = request.json.get('title', todo['title'])
    todo['done'] = request.json.get('done', todo['done'])
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        abort(404)
    todos.remove(todo)
    return jsonify({'result': True})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
