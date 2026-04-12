# Web development (Flask) simple app
# Requires Flask package
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'msg':'Hello from Flask'})

if __name__ == '__main__':
    app.run(debug=True)
