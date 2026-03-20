from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import sqlite3
from sqlalchemy import UniqueConstraint, exc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Student(db.Model):
    __table_args__ = (UniqueConstraint('name', 'date_of_birth', name='uix_name_date'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.name} - {self.date_of_birth}'

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/students')
def student():
    students = Student.query.all()
    output = []
    for student in students:
        student_data = {'name': student.name, 'date_of_birth': student.date_of_birth.strftime("%Y-%m-%d"), 'age': student.age}
        output.append(student_data)
    return {"students" : output}

@app.route('/students/<int:id>')
def student_by_id(id):
    student = Student.query.get_or_404(id)
    return {"name": student.name , "date_of_birth": student.date_of_birth.strftime("%Y-%m-%d"), "age": student.age}

@app.route('/students', methods=['POST'])
def add_student():
    try:
        student = Student(name=request.json['name'], date_of_birth=datetime.datetime.strptime(request.json['date_of_birth'], "%Y-%m-%d").date(), age=request.json['age'])
        db.session.add(student)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return {"error": "Student already exists"}
    return {"id": student.id}

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return {"message": "Student deleted"}

@app.route('/students/<int:id>', methods=['PATCH'])
def update_student(id):
    student = Student.query.get_or_404(id)
    student.name = request.json.get('name', student.name)
    student.date_of_birth = request.json.get('date_of_birth', student.date_of_birth)
    student.age = request.json.get('age', student.age)
    db.session.commit()
    return {"message": "Student updated"}