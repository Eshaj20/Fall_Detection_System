async function checkFall() {
    const inputData = document.getElementById("sensorData").value;
    const sensorArray = inputData.split(",").map(Number);

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sensor_data: sensorArray }),
    });

    const result = await response.json();
    const resultText = result.fall_detected ? "⚠️ Fall Detected!" : "✅ No Fall";
    document.getElementById("result").innerText = resultText;
}
