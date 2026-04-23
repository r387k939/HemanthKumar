# Student Assignment Tracker - DBMS Project 3

## Project Description
This project is a small full-stack academic tracking system built for a database management course. It is meant for instructors, teaching assistants, or department staff who want to manage students, courses, enrollments, assignments, and submissions from one interface.

The application uses a normalized relational schema and demonstrates the exact items required in the project sheet:
- Python 3
- Flask backend
- SQLite database
- SQLAlchemy ORM
- HTML, CSS, Bootstrap, and Jinja2 templates
- Git with incremental commits
- AI usage disclosure

## Core Features
1. **Multi-table CRUD**
   - Students: create, read, update, delete
   - Courses: create, read, update, delete
   - Enrollments: create and view
   - Assignments: create and view
   - Submissions: create and view

2. **Relationship Management**
   - Many-to-many relationship between Students and Courses through Enrollments
   - One-to-many relationship between Courses and Assignments
   - One-to-many relationship between Students and Submissions

3. **Transaction Logic**
   - When a submission is recorded, the app:
     1. inserts the submission,
     2. inserts a matching activity log row,
     3. recalculates enrollment progress,
     all inside one transaction block.

4. **Validation**
   - Empty strings are blocked
   - Duplicate student email addresses are blocked
   - Duplicate student-course enrollments are blocked
   - Max score must be positive
   - Score must stay between 0 and the assignment max score
   - End date cannot be earlier than the start date

5. **Summary Dashboard**
   - Uses aggregate functions such as `COUNT` and `AVG`
   - Displays high-level counts and course-level summary metrics

## Folder Structure
```text
dbms_project3_submission/
├── app.py
├── models.py
├── final_schema.sql
├── seed_data.sql
├── requirements.txt
├── README.md
├── NORMALIZATION.md
├── AI_LOG.md
├── GIT_HISTORY.md
├── .gitignore
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── students.html
│   ├── student_form.html
│   ├── courses.html
│   ├── course_form.html
│   ├── enrollments.html
│   ├── enrollment_form.html
│   ├── assignments.html
│   ├── assignment_form.html
│   ├── submissions.html
│   ├── submission_form.html
│   └── relationships.html
└── docs/
    └── submission_notes.pdf
```

## Installation Instructions
### 1. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

## Database Setup
This project uses SQLite for easy grading and setup.

The application automatically creates the database the first time it starts by running `final_schema.sql`.

If you want to inspect the schema manually:
```bash
sqlite3 instance/project3.db < final_schema.sql
```

## Usage
### Start the server
```bash
python app.py
```

### Open in the browser
```text
http://127.0.0.1:5000/
```

## Main Pages
- `/` - Landing page
- `/dashboard` - Summary dashboard
- `/students` - Student CRUD
- `/courses` - Course CRUD
- `/enrollments` - Enrollment listing and creation
- `/assignments` - Assignment listing and creation
- `/submissions` - Submission listing and transaction-based insertion
- `/relationships` - Relationship view

## Suggested Demo Flow
1. Open the dashboard and verify aggregate counts.
2. Add a new student.
3. Add a new course.
4. Enroll a student in a course.
5. Add an assignment for that course.
6. Record a submission for the enrolled student.
7. Open the relationship page and show that linked records display correctly.

## Git / Version Control Notes
The included repository history was created as a sequence of small course-style commits instead of one large upload. See `GIT_HISTORY.md` or run:
```bash
git log --oneline
```

## Submission Reminder
If your instructor expects a hosted Git link, push this folder to GitHub or GitLab after extraction:
```bash
git remote add origin <your-repository-url>
git push -u origin main
```
Then paste that repository URL into your final course submission.
