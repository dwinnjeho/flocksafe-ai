from flask import Flask, request, jsonify

app = Flask(__name__)

# limit para hindi mag error
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  

@app.route('/')
def home():
    return "Server running"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file received", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    # save image
    file.save("uploaded.jpg")

    # SAMPLE AI RESPONSE (palitan mo ng AI mo)
    result = "Detected: Chicken (Healthy)"

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
