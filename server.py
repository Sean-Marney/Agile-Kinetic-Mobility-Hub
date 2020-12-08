import os
import json
import sqlite3
from flask import Flask, redirect, request,render_template, jsonify, send_from_directory
from datetime import date
from werkzeug.utils import secure_filename

#constants
UPLOAD_FOLDER = 'uploads'
DATABASE = "agileKinetic.db"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'svg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#returns blog posts from database
def getBlogPosts():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM tblBlogPosts"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

@app.route("/")
def index():
    if request.method =='GET':
        return redirect("/static/index.html", code=302)

@app.route("/contact")
def contact():
    return render_template("contact.html")

#renders blog posts page
@app.route("/blog")
def blog():
    if request.method =='GET':
        return render_template('blog.html', data=getBlogPosts())

@app.route("/blog/management", methods = ['POST','GET'])
def blogPosts():
    if request.method =='GET':
        return render_template('blogManagement.html', data=getBlogPosts())

@app.route("/blog/management/add", methods = ['POST','GET'])
def addBlogPost():
    if request.method =='POST':
        title = request.form.get('title', default="Error")
        message = request.form.get('message', default="Error")
        image = request.form.get('image', default="Error")
        print("Inserting new blog post...")
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            today = date.today()
            cursor.execute("INSERT INTO tblBlogPosts ('date', 'title', 'message', 'image') VALUES (?,?,?,?)",(today.strftime("%d/%m/%Y"), title, message, image))
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


@app.route("/blog/management/delete", methods = ['POST','GET'])
def deleteBlogPost():
    if request.method =='POST':
        id = request.form.get('id', default="Error")
        print("Delete blog post...")
        try:
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            today = date.today()
            cursor.execute("DELETE FROM tblBlogPosts WHERE id=?",[id])
            connection.commit()
            print("Delete successful")
            outputMessage = "Blog post deleted successfully"
        except Exception as e:
            connection.rollback()
            print("Deletion of blog post failed, rollback requested: " + str(e))
            outputMessage = "Failed to delete blog post"
        finally:
            connection.close()
            return outputMessage

#code to upload file to server
#amended from Flask Documentation
#accessed 05/12/2020
#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/blog/management/media", methods = ['POST','GET'])
def addBlogImage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            basedir = os.path.abspath(os.path.dirname(__file__))
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            return "Success"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#End of amended code

if __name__ == "__main__":
    app.run(debug=True)
