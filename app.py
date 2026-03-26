from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os, sqlite3
#DB imports
from config import Config
from models import db, Student, Document, Course, Country

app = Flask(__name__)
app.secret_key = "secret-key- on-production"  # ← added

# Database configuration
app.config.from_object(Config)

db.init_app(app)

# Create tables (only for the first time use)
with app.app_context():
    db.create_all()  # Do not drop tables in production/dev, to preserve existing data

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

# return to view all students page
@app.route("/view")
def view_students():
    students = Student.query.all()
    # Sort by FRO expiry date
    def get_expiry(student):
        fro_doc = next((d for d in student.documents if d.doc_type == 'FRO'), None)
        return fro_doc.expiry_date if fro_doc else None
    from datetime import date
    students.sort(key=lambda s: get_expiry(s) or date(9999, 12, 31))
    today = date.today()
    return render_template("view.html", students=students, today=today)

# return to delete students page
@app.route("/delete")
def delete_students():
    students = Student.query.all()
    return render_template("delete.html", students=students)

@app.route("/delete/<roll_no>", methods=["POST"])
def delete_student(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    if not student:
        flash("Student not found", "error")
        return redirect(url_for('delete_students'))
    
    # Delete documents and files
    for doc in student.documents:
        if doc.file_name:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        db.session.delete(doc)
    
    db.session.delete(student)
    db.session.commit()
    
    flash("Student deleted successfully", "success")
    return redirect(url_for('delete_students'))

# Download route
@app.route("/download/<filename>")
def download_file(filename):
    downloads_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    file_path = os.path.join(downloads_folder, filename)

    if not os.path.isfile(file_path):
        flash(f"File not found: {filename}", "error")
        return redirect(url_for('view_students'))

    return send_from_directory(downloads_folder, filename, as_attachment=True)

# return to Edit students page
@app.route("/edit", methods=["GET"])
def edit_students():
    roll_no = request.args.get('roll_no')
    if roll_no:
        return redirect(url_for('edit_student', roll_no=roll_no))
    return render_template("edit.html")

@app.route("/edit/<roll_no>")
def edit_student(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    if not student:
        flash("Student not found", "error")
        return redirect(url_for('view_students'))
    return render_template("edit.html", student=student)

@app.route("/edit/<roll_no>", methods=["POST"])
def update_student(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    if not student:
        flash("Student not found", "error")
        return redirect(url_for('view_students'))
    
    # Update student fields
    student.name = request.form['name']
    student.phone_nr = request.form['phone']
    student.email = request.form['email']
    student.course_name = request.form['course']
    student.country_name = request.form['country']
    
    from datetime import date
    def parse_date(d):
        if not d:
            return None
        if isinstance(d, date):
            return d
        return date.fromisoformat(d)
    
    # Handle FRO dates - update document
    fro_issue = parse_date(request.form.get('fro_issue_date'))
    fro_expiry = parse_date(request.form.get('fro_expiry_date'))

    document = None
    if fro_issue and fro_expiry:
        document = Document.query.filter_by(roll_no=roll_no, doc_type='FRO').first()
        if document:
            document.issue_date = fro_issue
            document.expiry_date = fro_expiry
        else:
            document = Document(
                roll_no=roll_no,
                doc_type='FRO',
                issue_date=fro_issue,
                expiry_date=fro_expiry
            )
            db.session.add(document)
    
    # Handle document upload
    file = request.files.get('document')
    if file and file.filename:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if document:
            document.file_name = filename

    db.session.commit()

    flash("Student updated successfully", "success")
    return redirect(url_for('view_students'))

# Search endpoint
@app.route("/search")
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('home'))

    # Search by name or roll_no (case insensitive)
    students = Student.query.filter(
        (Student.name.ilike(f'%{query}%')) | (Student.roll_no.ilike(f'%{query}%'))
    ).all()
    
    from datetime import date
    today = date.today()
    return render_template("view.html", students=students, today=today, search_query=query)

# Handle Form Submission
@app.route("/submit", methods=["GET", "POST"])
def submit_student():
    if request.method == 'POST':
        # Get Data From HTML Form
        name = request.form['name']
        surname = "..."  # Placeholder
        roll_no = request.form['roll']
        phone_nr = request.form['phone']
        email = request.form['email']
        country_name = request.form['country']
        course_name = request.form['course']
        fro_issue = request.form.get('fro_issue')
        fro_expiry = request.form.get('fro_expiry')
        passport_issue = request.form.get('passport_issue')
        passport_expiry = request.form.get('passport_expiry')
        visa_issue = request.form.get('visa_issue')
        visa_expiry = request.form.get('visa_expiry')
        
        errors = []
        
        if len(name) < 3:
            errors.append("Enter valid name")
        if len(phone_nr) != 10:
            errors.append("Enter valid phone number")
        if len(email) < 5 or "@" not in email:
            errors.append("Enter valid email")
        if len(roll_no) < 7:
            errors.append("Enter valid roll number (at least 7 characters)")
        
        # Check for duplicates
        existing = Student.query.filter(
            (Student.email == email) | 
            (Student.roll_no == roll_no) | 
            (Student.phone_nr == phone_nr)
        ).all()
        
        existing_email = any(s.email == email for s in existing)
        existing_roll = any(s.roll_no == roll_no for s in existing)
        existing_phone = any(s.phone_nr == phone_nr for s in existing)   
        
        if existing_email:
            errors.append("A student with the same email already exists.")
        if existing_roll:
            errors.append("A student with the same roll number already exists.")
        if existing_phone:
            errors.append("A student with the same phone number already exists.")
        
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("add_student.html")
        
        # Create the student object
        student = Student(
            roll_no=roll_no,
            name=name,
            surname=surname,
            phone_nr=phone_nr,
            email=email,
            course_name=course_name,
            country_name=country_name
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Handle document uploads and dates
        fro_issue = request.form.get('fro_issue')
        fro_expiry = request.form.get('fro_expiry')
        passport_issue = request.form.get('passport_issue')
        passport_expiry = request.form.get('passport_expiry')
        visa_issue = request.form.get('visa_issue')
        visa_expiry = request.form.get('visa_expiry')
        
        file = request.files.get('document')
        filename = None
        if file and file.filename:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        
        from datetime import date

        def parse_date(d):
            if not d:
                return None
            if isinstance(d, date):
                return d
            return date.fromisoformat(d)

        fro_issue_date = parse_date(fro_issue)
        fro_expiry_date = parse_date(fro_expiry)
        passport_issue_date = parse_date(passport_issue)
        passport_expiry_date = parse_date(passport_expiry)
        visa_issue_date = parse_date(visa_issue)
        visa_expiry_date = parse_date(visa_expiry)

        # Create documents
        if fro_issue_date and fro_expiry_date:
            fro_doc = Document(
                roll_no=roll_no,
                doc_type='FRO',
                issue_date=fro_issue_date,
                expiry_date=fro_expiry_date,
                file_name=filename
            )
            db.session.add(fro_doc)

        if passport_issue_date and passport_expiry_date:
            passport_doc = Document(
                roll_no=roll_no,
                doc_type='Passport',
                issue_date=passport_issue_date,
                expiry_date=passport_expiry_date
            )
            db.session.add(passport_doc)

        if visa_issue_date and visa_expiry_date:
            visa_doc = Document(
                roll_no=roll_no,
                doc_type='Visa',
                issue_date=visa_issue_date,
                expiry_date=visa_expiry_date
            )
            db.session.add(visa_doc)

        db.session.commit()
        
        flash("Student added successfully! Please return to the dashboard.", "success")
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))
        

#Base models

if __name__ == "__main__":
    app.run(debug=True)