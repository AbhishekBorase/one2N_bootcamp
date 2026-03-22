from flask import Blueprint, request
from application import Student, db
import datetime
from sqlalchemy import exc

bp = Blueprint('api_v2', __name__)


def _is_adult(age):
    try:
        return int(age) >= 18
    except Exception:
        return False


@bp.route('/students', methods=['GET'])
def get_students_v2():
    students = Student.query.all()
    output = []
    for s in students:
        output.append({
            'id': s.id,
            'name': s.name,
            'dob': s.date_of_birth.strftime("%Y-%m-%d"),
            'age': s.age,
            'is_adult': _is_adult(s.age),
        })
    return {'students': output, 'version': 'v2'}


@bp.route('/students/<int:id>', methods=['GET'])
def get_student_v2(id):
    s = Student.query.get_or_404(id)
    return {
        'id': s.id,
        'name': s.name,
        'dob': s.date_of_birth.strftime("%Y-%m-%d"),
        'age': s.age,
        'is_adult': _is_adult(s.age),
        'version': 'v2',
    }


@bp.route('/addstudent', methods=['POST'])
def create_student_v2():
    data = request.get_json() or {}
    try:
        s = Student(
            name=data['name'],
            date_of_birth=datetime.datetime.strptime(data['dob'], "%Y-%m-%d").date(),
            age=data.get('age'),
        )
        db.session.add(s)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return {'error': 'Student already exists'}, 400
    return {'id': s.id, 'version': 'v2'}, 201
