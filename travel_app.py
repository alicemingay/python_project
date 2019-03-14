from flask import Flask, render_template

app = Flask("app")

@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=TRUE)
