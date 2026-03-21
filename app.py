from flask import Flask, render_template, request, redirect, url_for
import os, sqlite3
#DB imports
from config import Config
from models import db, Student, Document

app = Flask(__name__)
# Database configuration
app.config.from_object(Config)

db.init_app(app)

# Create tables (only for the first time use)
with app.app_context():
    db.create_all()

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

#Return to Dashboard
@app.route("/index")
def index():
    return render_template("index.html")

# Search endpoint
@app.route("/search")
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('home'))

    #  real DB search logic not ready.
    # For now this echoes the search query.
    message = f"Search requested for: '{query}'. (Search data not yet implemented!!! .)"
    return render_template("index.html", search_query=query, message=message)

# Handle Form Submission
@app.route("/submit", methods=["GET", "POST"])
def submit_student():
     data = request.form

     file = request.files['document']
     filename = file.filename
     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
     if request.method == 'POST':
        
        #Get Data From HTML Form
        name = request.form['name']
        surname = "Default"
        roll_no = request.form['roll']
        phone_nr = request.form['phone']
        email = request.form['email']
        
        country_name = request.form['country']
        course_name = request.form['course']
        
        #Create the student object
        student = Student(
            roll_no=roll_no,
            name=name,
            surname=surname,
            phone_nr=phone_nr,
            email=email,
            course_id=1,  # Placeholder, should be set based on course_name
            country_id=1  # Placeholder, should be set based on country_name
        )
        #Add to DB
        db.session.add(student)
        db.session.commit()
        
        return redirect(url_for('add_student'))

    # For now, it will just print the data (we will connect DB later)
    # print("Student Data:", data)
    # print("File uploaded:", filename)

     return "Student added successfully! Please return to the dashboard."

#Base models

if __name__ == "__main__":
    app.run(debug=True)