from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("fake_company_detector.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    website = request.form["website"]
    review = float(request.form["review"])
    email = request.form["email"]
    desc = request.form["description"]

    # Feature 1: suspicious_words
    suspicious_words = 1 if any(word in desc.lower() for word in ['pay', 'fee', 'money', 'charges', 'suspicious']) else 0

    # Feature 2: mail_check (domain looks suspicious or unprofessional)
    suspicious_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    domain = email.split("@")[-1]
    mail_check = 1 if domain in suspicious_domains else 0

    # Feature 3: review_score
    review_score = review

    # Final feature array
    features = np.array([[suspicious_words, mail_check, review_score]])
    result = model.predict(features)[0]

    return render_template("index.html", prediction="Fake" if result else "Genuine")

if __name__ == "__main__":
    app.run(debug=True)
