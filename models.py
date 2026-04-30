from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initialize SQLAlchemy instance
db = SQLAlchemy()


# stores program information (e.g., Computer Science, Data Science)
class Program(db.Model):
    __tablename__ = "programs"

    program_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(100), unique=True, nullable=False)

    students = db.relationship("Student", back_populates="program")


# stores possible student status values (active, graduated, etc.)
class StudentStatus(db.Model):
    __tablename__ = "student_statuses"

    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(20), unique=True, nullable=False)

    students = db.relationship("Student", back_populates="status")


# lookup table for how enrollment records were created
class RecordSource(db.Model):
    __tablename__ = "record_sources"

    source_id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(50), unique=True, nullable=False)

    enrollments = db.relationship("Enrollment", back_populates="source")


# stores instructor information (separated to avoid repetition)
class Instructor(db.Model):
    __tablename__ = "instructors"

    instructor_id = db.Column(db.Integer, primary_key=True)
    instructor_name = db.Column(db.String(100), unique=True, nullable=False)

    courses = db.relationship("Course", back_populates="instructor")


# main student table with references to program and status
class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.program_id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("student_statuses.status_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    program = db.relationship("Program", back_populates="students")
    status = db.relationship("StudentStatus", back_populates="students")

    # relationships for linked data
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    submissions = db.relationship("Submission", back_populates="student", cascade="all, delete-orphan")


# course table linked to instructor
class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey("instructors.instructor_id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    instructor = db.relationship("Instructor", back_populates="courses")

    # relationships
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", back_populates="course", cascade="all, delete-orphan")


# linking table between students and courses (many-to-many)
class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    progress_percent = db.Column(db.Numeric(5, 2), default=0.00, nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey("record_sources.source_id"), nullable=False)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    source = db.relationship("RecordSource", back_populates="enrollments")


# assignments created under each course
class Assignment(db.Model):
    __tablename__ = "assignments"
    __table_args__ = (
        db.UniqueConstraint("course_id", "title", name="uq_course_title"),
    )

    assignment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    course = db.relationship("Course", back_populates="assignments")

    # one assignment can have many submissions
    submissions = db.relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")


# stores assignment submissions and grading details
class Submission(db.Model):
    __tablename__ = "submissions"
    __table_args__ = (
        db.UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student"),
    )

    submission_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.assignment_id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    score = db.Column(db.Numeric(5, 2))
    grader_note = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    assignment = db.relationship("Assignment", back_populates="submissions")
    student = db.relationship("Student", back_populates="submissions")


# keeps track of important system actions (like submission creation)
class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    log_id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    reference_table = db.Column(db.String(50), nullable=False)
    reference_id = db.Column(db.Integer, nullable=False)
    event_note = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)