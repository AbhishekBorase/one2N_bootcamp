from flask import Blueprint, request
from application import Student, db
import datetime
from sqlalchemy import exc

bp = Blueprint('api_v1', __name__)


@bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    output = []
    for s in students:
        output.append({
            'id': s.id,
            'name': s.name,
            'date_of_birth': s.date_of_birth.strftime("%Y-%m-%d"),
            'age': s.age,
        })
    return {'students': output}


@bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    s = Student.query.get_or_404(id)
    return {
        'id': s.id,
        'name': s.name,
        'date_of_birth': s.date_of_birth.strftime("%Y-%m-%d"),
        'age': s.age,
    }


@bp.route('/addstudent', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    try:
        s = Student(
            name=data['name'],
            date_of_birth=datetime.datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date(),
            age=data.get('age'),
        )
        db.session.add(s)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return {'error': 'Student already exists'}, 400
    return {'id': s.id}, 201

