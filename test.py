from app import app
from models import db, Student, Course, Country, Document
from datetime import date

with app.app_context():
    course = Course(course_name="BCA")
    country = Country(country_name="India")

    db.session.add_all([course, country])
    db.session.commit()

    student = Student(
        roll_no="1",
        name="John",
        surname="Doe",
        phone_nr="1234567890",
        email="john.doe@example.com",
        course_name=course.course_name,
        country_name=country.country_name
    )

    db.session.add(student)
    db.session.commit()

    doc = Document(
        roll_no=1,
        doc_type="passport",
        issue_date=date(2022, 1, 1),
        expiry_date=date(2032, 1, 1)
    )

    db.session.add(doc)
    db.session.commit()