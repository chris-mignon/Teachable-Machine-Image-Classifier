from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Optional route to log predictions
@app.route('/log', methods=['POST'])
def log_prediction():
    data = request.get_json()
    print("Prediction received:", data)  # Print to console for now
    return jsonify({"status": "logged"})

if __name__ == "__main__":
    app.run(debug=True)
