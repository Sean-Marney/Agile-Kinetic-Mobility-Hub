import os
import json
import sqlite3
from flask import Flask, redirect, request,render_template, jsonify
from datetime import date


DATABASE = "agileKinetic.db"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/static/index.html", code=302)

@app.route("/contact", methods=['POST'])
def contact():
    return render_template("contact.html")

@app.route("/blog/AddBlogPost", methods = ['POST','GET'])
def addBlogPost():
    if request.method =='GET':
        return render_template("blogPost.html")
    if request.method =='POST':
        message = request.form.get('message', default="Error")
        print("Inserting new blog post...")
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            today = date.today()
            cursor.execute("INSERT INTO tblBlogPosts ('date', 'message') VALUES (?,?)",(today.strftime("%d/%m/%Y"), message))
            connection.commit()
            print("Insertion Successful.")
            outputMessage = "Blog post added successfully"
        except Exception as e:
            connection.rollback()
            print("Insertion of blog post failed, rollback requested: " + str(e))
            outputMessage = "Failed to add new blog post"
        finally:
            connection.close()
            return outputMessage

if __name__ == "__main__":
    app.run(debug=True)
