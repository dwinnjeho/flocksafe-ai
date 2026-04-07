from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

app = Flask(__name__)

# Load TFLite model
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

classes = [
    "Avian Influenza",
    "Coccidiosis",
    "Coryza",
    "Fowl Cholera",
    "Fowl Pox",
    "Healthy",
    "Infectious Bronchitis",
    "Marek's Disease",
    "Mycoplasma",
    "Newcastle Disease"
]

info = {
    "Avian Influenza": {"symptoms": "Swelling, breathing issues, sudden death", "remedy": "Isolate birds and notify vet"},
    "Coccidiosis": {"symptoms": "Bloody diarrhea, weakness", "remedy": "Use anticoccidial drugs"},
    "Coryza": {"symptoms": "Swollen face, nasal discharge", "remedy": "Antibiotics"},
    "Fowl Cholera": {"symptoms": "Loss of appetite, diarrhea", "remedy": "Vaccination"},
    "Fowl Pox": {"symptoms": "Skin lesions", "remedy": "Vaccinate birds"},
    "Healthy": {"symptoms": "No symptoms", "remedy": "No action needed"},
    "Infectious Bronchitis": {"symptoms": "Coughing", "remedy": "Improve ventilation"},
    "Marek's Disease": {"symptoms": "Paralysis", "remedy": "Vaccination"},
    "Mycoplasma": {"symptoms": "Respiratory issues", "remedy": "Antibiotics"},
    "Newcastle Disease": {"symptoms": "Twisted neck", "remedy": "Vaccinate birds"}
}

@app.route('/')
def home():
    return "FlockSafe AI TFLite API is running"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']

    try:
        img = Image.open(file).convert('RGB')
        img = img.resize((224, 224))
        img = np.array(img, dtype=np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])

        index = int(np.argmax(output))
        confidence = float(np.max(output))
        disease = classes[index]

        disease_info = info.get(disease, {"symptoms": "Unknown", "remedy": "Consult expert"})

        return jsonify({
            "disease": disease,
            "confidence": confidence,
            "symptoms": disease_info["symptoms"],
            "remedy": disease_info["remedy"]
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
