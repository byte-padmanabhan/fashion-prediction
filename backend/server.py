from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
import numpy as np
import cv2

app = Flask(__name__)
CORS(app)

# Load your saved CNN model
model = keras.models.load_model("my_model.keras")

# Class labels for Fashion MNIST
class_labels = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]

@app.post("/predict")
def predict():
    # Get image file from frontend
    file = request.files['file']

    # Convert bytes to grayscale OpenCV image
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    # Resize to 28x28 (same as your CNN input)
    img = cv2.resize(img, (28, 28))

    # Normalize & reshape for CNN
    img = img.reshape(1, 28, 28, 1) / 255.0

    # Make prediction
    pred = model.predict(img)
    label_index = int(np.argmax(pred))
    label_name = class_labels[label_index]

    return jsonify({
        "prediction_index": label_index,
        "prediction_name": label_name
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
