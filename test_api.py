import pytest
import datetime
from application import app, db

@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    # teardown
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_get_students(client):
    resp = client.get('/api/v1/students')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'students' in data
    assert isinstance(data['students'], list)

def test_create_student(client):
    new_student = {
        'name': 'Test Student',
        'date_of_birth': '2000-01-01',
        'age': 24
    }
    resp = client.post('/api/v1/addstudent', json=new_student)
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data
    student_id = data['id']

    # Cleanup
    del_resp = client.delete(f'/deletestudent/{student_id}')
    assert del_resp.status_code == 204

def test_create_duplicate_student(client):
    new_student = {
        'name': 'Duplicate Student',
        'date_of_birth': '2000-01-01',
        'age': 24
    }
    # Create first time
    r1 = client.post('/api/v1/addstudent', json=new_student)
    assert r1.status_code == 201
    sid = r1.get_json()['id']

    # Create duplicate
    r2 = client.post('/api/v1/addstudent', json=new_student)
    assert r2.status_code == 400
    data = r2.get_json()
    assert 'error' in data

    # Cleanup
    del_resp = client.delete(f'/deletestudent/{sid}')
    assert del_resp.status_code == 204