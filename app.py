from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔥 FIX 413 ERROR
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

@app.route('/')
def home():
    return "Server running"

@app.route('/predict', methods=['POST'])
def predict():

    # ✅ accept file
    if 'file' not in request.files:
        return jsonify({"error": "No file received"})

    file = request.files['file']

    # 🔥 TEST RESULT
    return jsonify({
        "result": "Healthy Chicken",
        "confidence": "98%"
    })

if __name__ == '__main__':
    app.run()
