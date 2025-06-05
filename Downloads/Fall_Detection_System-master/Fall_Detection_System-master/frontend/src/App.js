import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [sensorData, setSensorData] = useState("");
  const [fallDetected, setFallDetected] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkFall = async () => {
    if (!sensorData) {
      alert("Please enter sensor values!");
      return;
    }

    setLoading(true);
    try {
      const inputValues = sensorData.split(",").map(Number);
      
      if (inputValues.length !== 11) {
        alert("❌ Please enter exactly 11 sensor values!");
        return;
      }

      const response = await axios.post("http://localhost:5000/predict", {
        sensor_data: inputValues,
      });

      setFallDetected(response.data.fall_detected);
    } catch (error) {
      console.error("Error:", error);
      alert(error.response?.data?.error || "Failed to get prediction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🚨 Fall Detection System</h1>
      
      <div className="input-section">
        <textarea
          placeholder="Enter 11 sensor values (comma-separated)"
          value={sensorData}
          onChange={(e) => setSensorData(e.target.value)}
          rows={3}
        />
        <button onClick={checkFall} disabled={loading}>
          {loading ? "Processing..." : "Check Fall"}
        </button>
      </div>

      {fallDetected !== null && (
        <div className={`alert-box ${fallDetected ? "danger" : "safe"}`}>
          {fallDetected ? (
            <>
              <h2>FALL DETECTED!</h2>
              <p>Emergency alert has been sent!</p>
            </>
          ) : (
            <h2>No fall detected</h2>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
