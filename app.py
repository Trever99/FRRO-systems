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
    ##Thread issue solution with conn
    
     conn = sqlite3.connect(r"C:\Users\EazyPC\OneDrive\Documents\A.PROJECTS\FRRO managment system\FRRO-systems\students.db")
     cursor = conn.cursor()
    #  data = request.form

     file = request.files['document']
     filename = file.filename
     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
     if request.method == 'POST':
        
        #Get Data From HTML Form
        name = request.form['name']
        surname = "..."
        roll_no = request.form['roll']
        phone_nr = request.form['phone']
        email = request.form['email']
        country_name = request.form['country']
        course_name = request.form['course']
        
        if len(name) < 3:
            message = "enter valid name"
            return render_template("add_student.html", message=message)
        elif len(phone_nr) != 10:
            message = "enter valid phone number"
            return render_template("add_student.html", message=message)
        elif len(email) < 5 or "@" not in email:
            message = "enter valid email"
            return render_template("add_student.html", message=message)
        elif len(roll_no) < 7:
            message = "enter valid roll number(at least 7 characters)"
            return render_template("add_student.html", message=message)
        else:
        
       
        
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
        #validation and error handling can be added here (e.g., check for empty fields, validate email format, etc.)
          existing = Student.query.filter(
            (Student.email == email) | 
            (Student.roll_no == roll_no) | 
            (Student.phone_nr == phone_nr)
          )
        
        ## Checking if the fields exists
          existing_email = any(s.email == email for s in existing)
          existing_roll = any(s.roll_no == roll_no for s in existing)
          existing_phone = any(s.phone_nr == phone_nr for s in existing)   
        
        # If any of the fields already exists, show an error message
      
          if existing_email:
            message = "A student with the same email already exists."
            return render_template("add_student.html", message=message)
          elif existing_roll:
            message = "A student with the same roll number already exists."
            return render_template("add_student.html", message=message)
          elif existing_phone:
            message = "A student with the same phone number already exists."
            return render_template("add_student.html", message=message)
    
          else:
        # Add student to the database
           db.session.add(student)
           db.session.commit()
           return render_template("add_student.html", message="Student added successfully! Please return to the dashboard.")
          return redirect(url_for('add_student'))
        
     

#Base models

if __name__ == "__main__":
    app.run(debug=True)