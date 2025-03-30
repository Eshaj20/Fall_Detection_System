from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
import joblib
import numpy as np
import threading

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load(r"trained_model_path")  # Update path

# Twilio Configuration
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE = "your_twilio_phone_number"  # Twilio phone number
EMERGENCY_NUMBER = "your_emergency_number"  # Default number

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_alert_sms():
    try:
        message = client.messages.create(
            body="🚨 EMERGENCY: Fall detected! Immediate assistance needed.",
            from_=TWILIO_PHONE,
            to=EMERGENCY_NUMBER
        )
        print(f"SMS sent: {message.sid}")
        return True
    except Exception as e:
        print(f"SMS Error: {e}")
        return False

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        sensor_data = np.array(data["sensor_data"]).reshape(1, -1)
        
        # Validate input
        if sensor_data.shape[1] != 11:
            return jsonify({"error": "Exactly 11 sensor values required"}), 400
            
        prediction = model.predict(sensor_data)
        fall_detected = bool(prediction[0])
        
        if fall_detected:
            # Send SMS in background thread to avoid delay
            threading.Thread(target=send_alert_sms).start()
            
        return jsonify({
            "fall_detected": fall_detected,
            "sensor_data": sensor_data.tolist()[0]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
