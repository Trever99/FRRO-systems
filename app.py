from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Folder to store uploaded documents
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

# Show Add Student Form
@app.route("/add")
def add_student():
    return render_template("add_student.html")

# Handle Form S`ubmission
@app.route("/submit", methods=["POST"])
def submit_student():
    data = request.form

    file = request.files['document']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # For now, just print data (we'll connect DB later)
    print("Student Data:", data)
    print("File uploaded:", filename)

    return "Student added successfully!"

if __name__ == "__main__":
    app.run(debug=True)