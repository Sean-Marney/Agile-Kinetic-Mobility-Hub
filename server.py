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

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/blog")
def blog():
    if request.method =='GET':
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        query = "SELECT * FROM tblBlogPosts"
        cur.execute(query)
        data = cur.fetchall()
        conn.close()
        return render_template('blog.html', data=data)

@app.route("/blog/management", methods = ['POST','GET'])
def addBlogPost():
    if request.method =='GET':
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        query = "SELECT * FROM tblBlogPosts"
        cur.execute(query)
        data = cur.fetchall()
        conn.close()
        return render_template('blogManagement.html', data=data)
    if request.method =='POST':
        title = request.form.get('title', default="Error")
        message = request.form.get('message', default="Error")
        print("Inserting new blog post...")
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            today = date.today()
            cursor.execute("INSERT INTO tblBlogPosts ('date', 'title', 'message') VALUES (?,?,?)",(today.strftime("%d/%m/%Y"), title, message))
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
