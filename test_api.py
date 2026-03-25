import pytest
import datetime
from application import app, db

@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_get_students(client):
    resp1 = client.get('/api/v1/students')
    resp2 = client.get('/api/v2/students')
    for resp in [resp1, resp2]:
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'students' in data
        assert isinstance(data['students'], list)

def test_create_student(client):
    new_student_v1 = {
        'name': 'Test Student',
        'date_of_birth': '2000-01-01',
        'age': 24
    }
    new_student_v2 = {
        'name': 'Test Student 2',
        'dob': '2000-01-01',
        'age': 24
    }
    resp1 = client.post('/api/v1/addstudent', json=new_student_v1)
    resp2 = client.post('/api/v2/addstudent', json=new_student_v2)
    for resp in [resp1, resp2]:
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        student_id = data['id']

        # Cleanup
        del_resp = client.delete(f'/deletestudent/{student_id}')
        assert del_resp.status_code == 200

def test_create_duplicate_student(client):
    new_student_v1 = {
        'name': 'Duplicate Student',
        'date_of_birth': '2000-01-01',
        'age': 24
    }
    new_student_v2 = {
        'name': 'Duplicate Student',
        'dob': '2000-01-01',
        'age': 24
    }

    for version, new_student in {"v1": new_student_v1, "v2": new_student_v2}.items():
    # Create first time
        r1 = client.post(f'/api/{version}/addstudent', json=new_student)
        assert r1.status_code == 201
        sid = r1.get_json()['id']

        # Create duplicate
        r2 = client.post(f'/api/{version}/addstudent', json=new_student)
        assert r2.status_code == 400
        data = r2.get_json()
        assert 'error' in data

        # Cleanup
        del_resp = client.delete(f'/deletestudent/{sid}')
        assert del_resp.status_code == 200