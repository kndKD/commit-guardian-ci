"""Project 1 base app — the same Flask app carried through Projects 2-12.

Endpoints are intentionally small: this project is about Docker + CI,
not about building a large app yet. Later projects add auth, ML, and
security layers on top of this same service.
"""

import os
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

__version__ = "0.1.0"

_STARTED = time.monotonic()


@app.get("/")
def index():
    return jsonify(
        {
            "service": "system-core",
            "project": "commit-guardian-ci",
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


@app.get("/api/status")
def status():
    return jsonify(
        {
            "service": "system-core",
            "project": "commit-guardian-ci",
            "version": __version__,
            "status": "ok",
            "uptime_seconds": int(time.monotonic() - _STARTED),
            "endpoints": ["/", "/health", "/api/hello", "/api/status", "/api/echo"],
        }
    )


@app.post("/api/echo")
def echo():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(
            {
                "error": "bad_request",
                "message": "expected a JSON body",
            }
        ), 400
    return jsonify({"echo": data}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "error": "not_found",
            "message": "the requested resource was not found",
        }
    ), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "error": "method_not_allowed",
            "message": "this method is not allowed on this resource",
        }
    ), 405


@app.errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            "error": "bad_request",
            "message": getattr(error, "description", None) or "bad request",
        }
    ), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
