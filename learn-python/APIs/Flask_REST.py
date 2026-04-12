# Flask: REST API Example

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    q = request.args.get("q")
    return jsonify({"item_id": item_id, "q": q})

if __name__ == "__main__":
    app.run(debug=True)
