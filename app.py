from flask import Flask, request, render_template
import numpy as np
from preprocessing import load_and_preprocess
from model import load_trained_model
import plotly.graph_objs as go
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

app = Flask(__name__)
model = load_trained_model()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]

        if file:
            file_path = "uploaded.csv"
            file.save(file_path)

            # Preprocess
            X, y_true_scaled, scaler = load_and_preprocess(file_path)

            # Predict
            y_pred_scaled = model.predict(X)

            # Inverse transform
            y_true = scaler.inverse_transform(y_true_scaled.reshape(-1,1)).flatten()
            y_pred = scaler.inverse_transform(y_pred_scaled).flatten()

            # Metrics (for full data)
            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            r2 = r2_score(y_true, y_pred)

            # Send raw arrays to template
            return render_template(
                "results.html",
                mae=mae, rmse=rmse, r2=r2,
                y_true=y_true.tolist(),
                y_pred=y_pred.tolist()
            )

    return render_template("index.html")

if __name__ == "__main__":
    print("Open your browser and go to http://127.0.0.1:5000/")
    app.run(debug=True, host="127.0.0.1", port=5000)
