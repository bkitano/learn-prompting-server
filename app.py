from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Home page
@app.route("/api/v1/check", methods=["POST"])
def check():
    print(request.json)
    return jsonify({"status": "OK"})
