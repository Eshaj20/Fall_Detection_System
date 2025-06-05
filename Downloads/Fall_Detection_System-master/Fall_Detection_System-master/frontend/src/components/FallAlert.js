import React from "react";
import "./FallAlert.css"; // Import styles

const FallAlert = ({ fallDetected }) => {
  return (
    <div className={fallDetected ? "alert-box alert" : "alert-box safe"}>
      <h2>{fallDetected ? "⚠️ Fall Detected!" : "✅ No Fall"}</h2>
    </div>
  );
};

export default FallAlert;
