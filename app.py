from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store predictions in memory for now
prediction_log = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_prediction():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    top_class = max(data, key=lambda x: x["probability"])
    entry = {
        "time": timestamp,
        "class": top_class["className"],
        "confidence": round(top_class["probability"] * 100, 2),
        "all_predictions": data
    }
    prediction_log.append(entry)
    return jsonify({"status": "logged"})

@app.route('/dashboard')
def dashboard():
    # Summarize prediction counts
    class_counts = {}
    for entry in prediction_log:
        cls = entry["class"]
        class_counts[cls] = class_counts.get(cls, 0) + 1

    return render_template("dashboard.html",
                           logs=prediction_log,
                           class_counts=class_counts)

if __name__ == "__main__":
    app.run(debug=True)
