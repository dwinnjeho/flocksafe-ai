from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "FlockSafe API is running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    user_input = data.get("input", "")

    if "danger" in user_input.lower():
        result = "Warning: Unsafe"
    else:
        result = "Safe"

    return jsonify({
        "input": user_input,
        "result": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
