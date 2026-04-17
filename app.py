"""Flask application for the Crash Analysis & Injury Prediction System."""

import os
from flask import Flask, render_template, request, jsonify
from main import run_analysis
from utils import validate_inputs

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        speed = float(request.form.get("speed", 50))
        collision_type = request.form.get("collision", "frontal")
        seatbelt = request.form.get("seatbelt", "false") == "true"
        airbags = request.form.get("airbags", "false") == "true"

        validate_inputs(speed, collision_type, seatbelt, airbags)
        report = run_analysis(speed, collision_type, seatbelt, airbags)
        return jsonify({"success": True, "data": report})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "error": "Internal server error."}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
