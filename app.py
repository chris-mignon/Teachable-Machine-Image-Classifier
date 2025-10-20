from flask import Flask, render_template, request, jsonify
from datetime import datetime
from collections import Counter

app = Flask(__name__)

# Store logs in memory
prediction_logs = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    # Count frequency of each class
    counts = Counter([log["class"] for log in prediction_logs])
    return render_template("dashboard.html", logs=prediction_logs, class_counts=counts)

@app.route("/log", methods=["POST"])
def log_prediction():
    data = request.get_json()
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "class": data.get("class"),
        "confidence": round(float(data.get("confidence", 0)) * 100, 2)
    }
    prediction_logs.append(log_entry)
    return jsonify({"status": "ok", "message": "logged"})
    
if __name__ == "__main__":
    app.run(debug=True)
