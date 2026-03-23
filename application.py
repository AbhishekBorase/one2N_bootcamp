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
    return 'Hello, Welcome to bootcamp!'

@app.route('/healthcheck')
def health():
    return 'Health check passed!', 200


@app.route('/deletestudent/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}, 204
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400

@app.route('/updatestudent/<int:id>', methods=['PATCH'])
def update_student(id):
    try:
        student = Student.query.get_or_404(id)
        student.name = request.json.get('name', student.name)
        student.date_of_birth = request.json.get('date_of_birth', student.date_of_birth)
        student.age = request.json.get('age', student.age)
        db.session.commit()
        return {"message": "Student updated"}, 204
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


try:
    from api.v1 import bp as api_v1_bp
    from api.v2 import bp as api_v2_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    app.register_blueprint(api_v2_bp, url_prefix='/api/v2')
except Exception as e:
    print(f"Error occurred while registering blueprints: {e}")