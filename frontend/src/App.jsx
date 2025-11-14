import React, { useState } from "react";

const App = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setPrediction(data.prediction_name || data.prediction); // Works for both Fashion MNIST or sign gestures
    } catch (err) {
      console.error(err);
      alert("Error sending image to backend.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Upload Image for Prediction</h2>
      <input type="file" onChange={handleFileChange} />
      <br />
      <button onClick={handleSubmit} style={{ marginTop: "20px" }}>
        Predict
      </button>

      <h3>Prediction:</h3>
      <p>{prediction ? prediction : "None"}</p>
    </div>
  );
};

export default App;
