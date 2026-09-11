from flask import Flask, render_template
import pickle

app = Flask(__name__)

with open("../models/arima_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    forecast = model.forecast(steps=7)
    return render_template("index.html", forecast=forecast)

if __name__ == "__main__":
    app.run(debug=True)
