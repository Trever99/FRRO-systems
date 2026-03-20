from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------Students----------------------------
class Student(db.Model):
    __tablename__ = 'students'
    
    roll_no = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False) 
    
    phone_nr = db.Column(db.String(10),nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)   
    
    course_id = db.Column(db.Integer,db.ForeignKey('courses.course_id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.country_id'), nullable=False)
        
    #Relationships ... Connecting the tables
    documents = db.relationship('Document', backref='student', lazy=True)

    def __repr__(self):
        return f"<Student {self.roll_no}>"
    
    
    
    # ----------------------------Courses----------------------------
class Course(db.Model):
    __tablename__ = 'courses'
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(20),nullable=False)
    
    def __repr__(self):
        return f"<Course {self.course_name}>"
    
    
# ----------------------------Countries----------------------------

class Country(db.Model):
    __tablename__ = 'countries'
    
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<Country {self.country_name}>"
    
# ----------------------------Documents----------------------------

class Document(db.Model):
    __tablename__ = 'documents'
    
    doc_id = db.Column(db.Integer, primary_key=True)
    
    roll_no = db.Column(db.Integer, db.ForeignKey('students.roll_no'), nullable=False)
    
    doc_type = db.Column(db.String(50), nullable=False) #Passport / Vissa / FRRO
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date,nullable=False)
    
    def __repr__(self):
        return f"<Document {self.document_name}>"
    

    
    