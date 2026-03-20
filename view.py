from app import app
from models import Student

with app.app_context():
    students = Student.query.all()
    for s in students:
        print(s.roll_no, s.name, s.surname, s.phone_nr, s.email, s.course_id, s.country_id)