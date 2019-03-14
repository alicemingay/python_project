from flask import Flask, render_template, request
import requests

app = Flask("app")

@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True)
