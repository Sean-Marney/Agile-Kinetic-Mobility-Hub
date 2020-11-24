import os
import json
from flask import Flask, redirect, request,render_template, jsonify

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
def index():
    return redirect("/static/index.html", code=302)

@app.route("/contact", methods=['POST'])
def contact():
    return render_template("contact.html")
    

if __name__ == "__main__":
    app.run(debug=True)
