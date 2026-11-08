"""Project 1 base app — the same Flask app carried through Projects 2-12.

Endpoints are intentionally small: this project is about Docker + CI,
not about building a large app yet. Later projects add auth, ML, and
security layers on top of this same service.
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def index():
    return jsonify(
        {
            "service": "system-core",
            "project": "01-docker-ci-ai-guardian",
            "status": "ok",
            "message": "Hello from the Project 1 Flask app.",
        }
    )

@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.get("/api/hello")
def hello():
    name = os.environ.get("HELLO_NAME", "world")
    return jsonify({"hello": name})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
