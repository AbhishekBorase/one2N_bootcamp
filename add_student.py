from application import app, db, Student
import datetime

def add_student(name, dob):
    with app.app_context():
        db.create_all()
        s = Student(name=name, date_of_birth=dob)
        db.session.add(s)
        db.session.commit()
        print("Added:", s)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        name = sys.argv[1]
        try:
            dob = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        except ValueError:
            print("Date must be YYYY-MM-DD")
            sys.exit(1)
        add_student(name, dob)
    else:
        print("Usage: python add_student.py NAME YYYY-MM-DD")