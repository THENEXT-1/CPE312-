from pathlib import Path
import math
import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
FEATURES = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return jsonify(ok=True, features=FEATURES)

def validate_features(values):
    if not isinstance(values, (list, tuple)) or len(values) != len(FEATURES):
        raise ValueError(f"กรุณาระบุตัวเลข 8 ค่าให้ครบตามลำดับนี้: {FEATURES}")
    try:
        numbers = [float(value) for value in values]
    except (TypeError, ValueError, OverflowError):
        raise ValueError("ข้อมูลทั้ง 8 รายการต้องเป็นตัวเลข")
    if not all(math.isfinite(value) for value in numbers):
        raise ValueError("ข้อมูลทั้ง 8 รายการต้องเป็นตัวเลขที่ถูกต้อง")
    return numbers

@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="ข้อมูลคำขอต้องอยู่ในรูปแบบ JSON object"), 400
    try:
        values = validate_features(data.get("features"))
        prediction = float(model.predict(np.asarray([values], dtype=float))[0])
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(prediction=prediction)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("main.html")
    values = []
    try:
        for feature in FEATURES:
            raw = request.form.get(feature, "").strip()
            if not raw:
                raise ValueError(f"กรุณากรอกค่า {feature} ให้ครบ")
            values.append(float(raw))
        if not all(math.isfinite(v) for v in values):
            raise ValueError("กรุณากรอกตัวเลขที่ถูกต้อง")
        prediction = float(model.predict(np.asarray([values], dtype=float))[0])
        return render_template("main.html", form_values=dict(zip(FEATURES, values)), form_prediction=prediction)
    except (ValueError, TypeError, OverflowError) as exc:
        return render_template("main.html", form_values=request.form, form_error=str(exc)), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
