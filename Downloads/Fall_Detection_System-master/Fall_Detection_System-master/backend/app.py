from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
import joblib
import numpy as np
import threading

app = Flask(__name__)
CORS(app)

# Load the trained KNN model and scaler
MODEL_PATH = r"your_model_path"
SCALER_PATH = r"your_scaler_model_path"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Twilio Configuration
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE = "twilio_phone_no"
EMERGENCY_NUMBER = "your_phone_number"

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Root route for health check
@app.route("/")
def home():
    return "✅ Fall Detection Flask Server is Running!"

# Function to send SMS alert
def send_alert_sms():
    try:
        message = client.messages.create(
            body="🚨 EMERGENCY: Fall detected! Immediate assistance needed.",
            from_=TWILIO_PHONE,
            to=EMERGENCY_NUMBER
        )
        print(f"✅ SMS sent: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ SMS Error: {e}")
        return False

# Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        sensor_data = np.array(data.get("sensor_data")).reshape(1, -1)

        # Ensure input is of correct shape
        if sensor_data.shape[1] != 10:
            return jsonify({"error": "Exactly 10 sensor values required"}), 400

        # Scale the sensor data
        sensor_data_scaled = scaler.transform(sensor_data)

        # Make prediction
        prediction = model.predict(sensor_data_scaled)
        fall_detected = prediction[0] == "fall"  # Adjust if your labels are 0/1

        # If fall is detected, send an SMS alert
        if fall_detected:
            threading.Thread(target=send_alert_sms).start()

        return jsonify({
            "fall_detected": fall_detected,
            "sensor_data": sensor_data.tolist()[0],
            "scaled_data": sensor_data_scaled.tolist()[0],
            "prediction": prediction[0]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
