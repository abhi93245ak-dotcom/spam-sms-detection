from flask import Flask, request, jsonify, render_template
import pickle
import mysql.connector

app = Flask(__name__)


with open("spam_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

db = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="",       
    database="spamdb"
)
cursor = db.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    message = data['message']

    msg_vec = vectorizer.transform([message])

    prediction = model.predict(msg_vec)[0]
    result = "Spam" if prediction == 1 else "Not Spam"

    sql = "INSERT INTO messages (message, prediction) VALUES (%s, %s)"
    val = (message, result)
    cursor.execute(sql, val)
    db.commit()

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)

