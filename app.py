from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("model.h5")

# Classes (must match training order)
classes = [
    "Avian Influenza",
    "Coccidiosis",
    "Coryza",
    "Fowl Cholera",
    "Fowl Pox",
    "Healthy",
    "Infectious Bronchitis",
    "Mareks",
    "Mycoplasma",
    "Newcastle"
]

@app.route('/')
def home():
    return "FlockSafe AI Image API is running"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files['file']

    img = Image.open(file).convert('RGB')
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    confidence = float(np.max(prediction))

    disease = classes[class_index]

    info = {
        "Avian Influenza": ("Respiratory distress", "Isolate birds, contact vet"),
        "Coccidiosis": ("Bloody diarrhea", "Use anticoccidial drugs"),
        "Coryza": ("Swollen face, nasal discharge", "Antibiotics"),
        "Fowl Cholera": ("Sudden death", "Vaccination, antibiotics"),
        "Fowl Pox": ("Skin lesions", "Vaccination"),
        "Healthy": ("No symptoms", "No treatment needed"),
        "Infectious Bronchitis": ("Coughing, sneezing", "Supportive care"),
        "Mareks": ("Paralysis", "Vaccination"),
        "Mycoplasma": ("Respiratory issues", "Antibiotics"),
        "Newcastle": ("Nervous signs", "Vaccination")
    }

    symptoms, remedy = info.get(disease, ("Unknown", "Consult vet"))

    return jsonify({
        "disease": disease,
        "confidence": confidence,
        "symptoms": symptoms,
        "remedy": remedy
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
