# one2N_bootcamp

# Student Registry (Flask + SQLAlchemy)

Simple Flask app using Flask-SQLAlchemy to store students in an SQLite database.

This app creates an API to perform the following operations.
- Add a new student.
- Get all students.
- Get a student with an ID.
- Update existing student information.
- Delete a student record.

**Quick Start**

- **Requirements:** Python 3.x, pip, make

- Install deps: (using makefile)

```bash
make venv
```

This will execute bellow comands for you in bash.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Run the app**

Use the makefile (preferred):

```bash
make run
```

This will automaticaly run the following comands in bash.

```bash
export FLASK_APP=application.py
export FLASK_ENV=development  # optional
flask run
```

The app exposes a root route and a `/students` placeholder route. See [application.py](application.py).

**Database**

- SQLite file: `students.db` (created in project root).
- Create tables manually:

```bash
flask shell
from application import Student, db
import datetime
stud2 = Student(name="Abhishek", date_of_birth=datetime.date(2001,4,30))
db.session.add(stud1)
db.session.commit()
```

**Add a student**

There is a helper script: [add_student.py](add_student.py)

```bash
python add_student.py "Alice" 2000-01-01
```

This script uses `app.app_context()` and will call `db.create_all()` before inserting.

**Unique constraint**

The `Student` model enforces a unique constraint on the combination of `name` and `date_of_birth`. Attempts to insert a duplicate pair will raise an `IntegrityError`.


**Migrations (recommended for schema changes)**

For production or evolving schemas use Flask-Migrate (Alembic) instead of deleting `students.db`.

**Relevant files**

- [application.py](application.py) — Flask app and `Student` model
- [add_student.py](add_student.py) — CLI script to add students
- [requirements.txt](requirements.txt) — Python dependencies

