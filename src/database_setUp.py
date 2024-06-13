from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
engine = create_engine('sqlite:///my_database.db')  # Replace with your database URL
Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)  # Define the email column as unique

# Create the database tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Example data (you can remove this if you're not using it)
students = [
    {'name': 'Alicccce Johnson', 'email': 'alice.johnnnson@example.com'},
    {'name': 'Boccccb Smith', 'email': 'bob.smittttth@example.com'},
    {'name': 'Chacccrlie Brown', 'email': 'charlyyyyyie.brown@example.com'}
]

# Insert students into the database (you can remove this if you're not using it)
for student_data in students:
    new_student = Student(name=student_data['name'], email=student_data['email'])
    session.add(new_student)
session.commit()
session.close()

# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)