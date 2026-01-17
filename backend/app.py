import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "house_price_model.pkl")
model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return {"status": "House Price Prediction API running"}


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        pred_log = model.predict(df)[0]
        prediction = float(np.expm1(pred_log))
        return jsonify({
            "predicted_price": round(prediction, 0)
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

