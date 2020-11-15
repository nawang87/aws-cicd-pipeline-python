from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def homepage():
    if request.method == "GET":
        return jsonify({"message": "Hello World from CI/CD Python-ECS Fargate Pipeline!"})

PORT = int(os.environ.get("PORT", 8080))
if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=PORT)