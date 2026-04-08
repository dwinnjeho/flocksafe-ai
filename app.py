from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Server running"

@app.route('/predict', methods=['POST'])
def predict():

    if 'file' in request.files:
        file = request.files['file']

        return jsonify({
            "result": "Healthy Chicken",
            "confidence": "98%"
        })

    else:
        return jsonify({"error": "No file"}), 400

if __name__ == '__main__':
    app.run()
