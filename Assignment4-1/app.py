from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def my_root():
    name = "Maryam"
    return render_template("index.html",  name=name)
 