from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, API!"})

if __name__ == "__main__":
    app.run(port=5000)
