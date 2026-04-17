import os
from flask import Flask, render_template, request, jsonify
from main import run_analysis
from utils import validate_inputs
from vehicle_data import get_all_frontend_data
from health_monitor import calculate_health_score
from alert_payload import build_all_payloads
from vehicle_data import get_vehicle

app = Flask(__name__)
app.json.sort_keys = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/vision", methods=["GET"])
def vision():
    return render_template("vision.html")


@app.route("/vehicle-data", methods=["GET"])
def vehicle_data():
    return jsonify(get_all_frontend_data())


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        speed         = float(request.form.get("speed", 50))
        collision_type = request.form.get("collision", "frontal")
        seatbelt      = request.form.get("seatbelt", "false") == "true"
        airbags       = request.form.get("airbags",  "false") == "true"
        vehicle_model = request.form.get("vehicle_model", "")
        generation    = request.form.get("generation", "")

        validate_inputs(speed, collision_type, seatbelt, airbags)
        report = run_analysis(speed, collision_type, seatbelt, airbags, vehicle_model, generation)
        return jsonify({"success": True, "data": report})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Internal server error."}), 500


@app.route("/api/health-score", methods=["POST"])
def api_health_score():
    # returns a safety health score for the selected vehicle + inputs
    try:
        speed         = float(request.form.get("speed", 50))
        seatbelt      = request.form.get("seatbelt", "false") == "true"
        airbags       = request.form.get("airbags",  "false") == "true"
        vehicle_model = request.form.get("vehicle_model", "")
        generation    = request.form.get("generation", "")

        vehicle = get_vehicle(vehicle_model, generation)
        score   = calculate_health_score(
            ncap_stars    = vehicle["ncap_stars"],
            seatbelt      = seatbelt,
            airbags       = airbags,
            speed_kmh     = speed,
            crumple_time_s= vehicle["crumple_time_s"],
            care_key_limit= vehicle["care_key_speed_limit"],
        )
        return jsonify({"success": True, "data": score})
    except Exception:
        return jsonify({"success": False, "error": "Could not calculate health score."}), 500


@app.route("/api/alert-preview", methods=["POST"])
def api_alert_preview():
    # builds a preview of what alert payloads would be sent
    # useful for the vision page and educational demo
    try:
        speed         = float(request.form.get("speed", 50))
        collision_type = request.form.get("collision", "frontal")
        seatbelt      = request.form.get("seatbelt", "false") == "true"
        airbags       = request.form.get("airbags",  "false") == "true"
        vehicle_model = request.form.get("vehicle_model", "")
        generation    = request.form.get("generation", "")

        validate_inputs(speed, collision_type, seatbelt, airbags)
        report   = run_analysis(speed, collision_type, seatbelt, airbags, vehicle_model, generation)

        # attach input fields so alert builder can use them
        report["summary"]["speed_kmh"]      = speed
        report["summary"]["collision_type"] = collision_type
        report["vehicle"]["seatbelt"]       = seatbelt
        report["vehicle"]["airbags"]        = airbags

        payloads = build_all_payloads(report)
        return jsonify({"success": True, "data": payloads})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        return jsonify({"success": False, "error": "Could not build alert payloads."}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", port=int(os.getenv("PORT", 5001)))
