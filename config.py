import os , sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database connection (for direct SQL queries if needed)
# conn = sqlite3.connect(os.path.join(BASE_DIR, 'students.db'))
# cursor = conn.cursor()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'students.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    