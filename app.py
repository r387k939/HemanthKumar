from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import (
    ActivityLog,
    Assignment,
    Course,
    Enrollment,
    Instructor,
    Program,
    RecordSource,
    Student,
    StudentStatus,
    Submission,
    db,
)


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "project3.db"


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-key-for-course-project"

    db.init_app(app)

    with app.app_context():
        initialize_database()

    register_routes(app)
    return app


def initialize_database():
    if DB_PATH.exists():
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    sql_text = (BASE_DIR / "final_schema.sql").read_text(encoding="utf-8")
    raw_connection = db.engine.raw_connection()

    try:
        raw_connection.executescript(sql_text)
        raw_connection.commit()
    finally:
        raw_connection.close()


def to_date(raw_value, field_label):
    try:
        parsed_date = datetime.strptime(raw_value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError(f"{field_label} must be a valid date in YYYY-MM-DD format.")

    if parsed_date.year < 2020 or parsed_date.year > 2035:
        raise ValueError(f"{field_label} year must be between 2020 and 2035.")

    return parsed_date


def clean_required(raw_value, field_label):
    value = (raw_value or "").strip()
    if not value:
        raise ValueError(f"{field_label} cannot be empty.")
    return value


def to_positive_int(raw_value, field_label):
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_label} must be a whole number.")

    if value <= 0:
        raise ValueError(f"{field_label} must be greater than zero.")

    return value


def to_score(raw_value, max_score):
    if raw_value in (None, ""):
        return None

    try:
        score = float(raw_value)
    except ValueError:
        raise ValueError("Score must be numeric.")

    if score < 0 or score > max_score:
        raise ValueError(f"Score must be between 0 and {max_score}.")

    return score


def recalculate_progress(student_id, course_id):
    assignment_total = (
        db.session.query(func.count(Assignment.assignment_id))
        .filter(Assignment.course_id == course_id)
        .scalar()
        or 0
    )

    if assignment_total == 0:
        percent_value = 0.00
    else:
        completed_total = (
            db.session.query(func.count(Submission.submission_id))
            .join(Assignment, Assignment.assignment_id == Submission.assignment_id)
            .filter(
                Submission.student_id == student_id,
                Assignment.course_id == course_id,
            )
            .scalar()
            or 0
        )
        percent_value = round((completed_total / assignment_total) * 100, 2)

    enrollment = Enrollment.query.filter_by(
        student_id=student_id,
        course_id=course_id,
    ).first()

    if enrollment:
        enrollment.progress_percent = percent_value


def register_routes(app):
    @app.route("/")
    def home():
        recent_logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(8).all()
        return render_template("home.html", recent_logs=recent_logs)

    @app.route("/dashboard")
    def dashboard():
        counts = {
            "students": Student.query.count(),
            "courses": Course.query.count(),
            "enrollments": Enrollment.query.count(),
            "assignments": Assignment.query.count(),
            "submissions": Submission.query.count(),
        }

        avg_score = db.session.query(func.round(func.avg(Submission.score), 2)).scalar()
        avg_progress = db.session.query(func.round(func.avg(Enrollment.progress_percent), 2)).scalar()

        course_snapshot = (
            db.session.query(
                Course.course_name,
                func.count(Enrollment.enrollment_id).label("student_count"),
                func.count(Assignment.assignment_id).label("assignment_count"),
                func.round(func.avg(Enrollment.progress_percent), 2).label("avg_progress"),
            )
            .outerjoin(Enrollment, Enrollment.course_id == Course.course_id)
            .outerjoin(Assignment, Assignment.course_id == Course.course_id)
            .group_by(Course.course_id, Course.course_name)
            .order_by(Course.course_name.asc())
            .all()
        )

        return render_template(
            "dashboard.html",
            counts=counts,
            avg_score=avg_score,
            avg_progress=avg_progress,
            course_snapshot=course_snapshot,
        )

    @app.route("/students")
    def students():
        student_rows = Student.query.order_by(Student.full_name.asc()).all()
        return render_template("students.html", students=student_rows)

    @app.route("/students/new", methods=["GET", "POST"])
    def add_student():
        programs = Program.query.order_by(Program.program_name.asc()).all()
        statuses = StudentStatus.query.order_by(StudentStatus.status_name.asc()).all()

        if request.method == "POST":
            try:
                student = Student(
                    full_name=clean_required(request.form.get("full_name"), "Full name"),
                    email=clean_required(request.form.get("email"), "Email").lower(),
                    program_id=int(request.form.get("program_id")),
                    status_id=int(request.form.get("status_id")),
                )

                db.session.add(student)
                db.session.commit()

                flash("Student added successfully.", "success")
                return redirect(url_for("students"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("Email must be unique, and all required dropdown values must be valid.", "danger")

        return render_template(
            "student_form.html",
            student=None,
            programs=programs,
            statuses=statuses,
        )

    @app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
    def edit_student(student_id):
        student = Student.query.get_or_404(student_id)
        programs = Program.query.order_by(Program.program_name.asc()).all()
        statuses = StudentStatus.query.order_by(StudentStatus.status_name.asc()).all()

        if request.method == "POST":
            try:
                student.full_name = clean_required(request.form.get("full_name"), "Full name")
                student.email = clean_required(request.form.get("email"), "Email").lower()
                student.program_id = int(request.form.get("program_id"))
                student.status_id = int(request.form.get("status_id"))

                db.session.commit()

                flash("Student details updated.", "success")
                return redirect(url_for("students"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("Update failed. Check unique email values and dropdown selections.", "danger")

        return render_template(
            "student_form.html",
            student=student,
            programs=programs,
            statuses=statuses,
        )

    @app.route("/students/<int:student_id>/delete", methods=["POST"])
    def delete_student(student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()

        flash("Student deleted.", "warning")
        return redirect(url_for("students"))

    @app.route("/courses")
    def courses():
        course_rows = Course.query.order_by(Course.course_name.asc()).all()
        return render_template("courses.html", courses=course_rows)

    @app.route("/courses/new", methods=["GET", "POST"])
    def add_course():
        instructors = Instructor.query.order_by(Instructor.instructor_name.asc()).all()

        if request.method == "POST":
            try:
                course = Course(
                    course_name=clean_required(request.form.get("course_name"), "Course name"),
                    instructor_id=int(request.form.get("instructor_id")),
                    start_date=to_date(request.form.get("start_date"), "Start date"),
                    end_date=to_date(request.form.get("end_date"), "End date"),
                )

                if course.end_date < course.start_date:
                    raise ValueError("End date cannot be earlier than the start date.")

                db.session.add(course)
                db.session.commit()

                flash("Course created.", "success")
                return redirect(url_for("courses"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("Could not save the course. Please review your data.", "danger")

        return render_template("course_form.html", course=None, instructors=instructors)

    @app.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
    def edit_course(course_id):
        course = Course.query.get_or_404(course_id)
        instructors = Instructor.query.order_by(Instructor.instructor_name.asc()).all()

        if request.method == "POST":
            try:
                course.course_name = clean_required(request.form.get("course_name"), "Course name")
                course.instructor_id = int(request.form.get("instructor_id"))
                course.start_date = to_date(request.form.get("start_date"), "Start date")
                course.end_date = to_date(request.form.get("end_date"), "End date")

                if course.end_date < course.start_date:
                    raise ValueError("End date cannot be earlier than the start date.")

                db.session.commit()

                flash("Course updated.", "success")
                return redirect(url_for("courses"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("Update failed. Please review the course details.", "danger")

        return render_template("course_form.html", course=course, instructors=instructors)

    @app.route("/courses/<int:course_id>/delete", methods=["POST"])
    def delete_course(course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()

        flash("Course deleted.", "warning")
        return redirect(url_for("courses"))

    @app.route("/enrollments")
    def enrollments():
        enrollment_rows = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).all()
        return render_template("enrollments.html", enrollments=enrollment_rows)

    @app.route("/enrollments/new", methods=["GET", "POST"])
    def add_enrollment():
        students = Student.query.order_by(Student.full_name.asc()).all()
        courses = Course.query.order_by(Course.course_name.asc()).all()
        sources = RecordSource.query.order_by(RecordSource.source_name.asc()).all()

        if request.method == "POST":
            try:
                enrollment = Enrollment(
                    student_id=int(request.form.get("student_id")),
                    course_id=int(request.form.get("course_id")),
                    enrollment_date=to_date(request.form.get("enrollment_date"), "Enrollment date"),
                    source_id=int(request.form.get("source_id")),
                    progress_percent=0.00,
                )

                db.session.add(enrollment)
                db.session.commit()

                flash("Enrollment created.", "success")
                return redirect(url_for("enrollments"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("That student is already enrolled in the selected course.", "danger")

        return render_template(
            "enrollment_form.html",
            enrollment=None,
            students=students,
            courses=courses,
            sources=sources,
        )

    @app.route("/assignments")
    def assignments():
        assignment_rows = Assignment.query.order_by(Assignment.due_date.asc()).all()
        return render_template("assignments.html", assignments=assignment_rows)

    @app.route("/assignments/new", methods=["GET", "POST"])
    def add_assignment():
        courses = Course.query.order_by(Course.course_name.asc()).all()

        if request.method == "POST":
            try:
                assignment = Assignment(
                    course_id=int(request.form.get("course_id")),
                    title=clean_required(request.form.get("title"), "Title"),
                    max_score=to_positive_int(request.form.get("max_score"), "Max score"),
                    due_date=to_date(request.form.get("due_date"), "Due date"),
                )

                db.session.add(assignment)
                db.session.commit()

                flash("Assignment added.", "success")
                return redirect(url_for("assignments"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("An assignment with that title already exists for this course.", "danger")

        return render_template("assignment_form.html", assignment=None, courses=courses)

    @app.route("/submissions")
    def submissions():
        submission_rows = Submission.query.order_by(Submission.submitted_at.desc()).all()
        return render_template("submissions.html", submissions=submission_rows)

    @app.route("/submissions/new", methods=["GET", "POST"])
    def add_submission():
        assignments = Assignment.query.order_by(Assignment.title.asc()).all()
        students = Student.query.order_by(Student.full_name.asc()).all()

        if request.method == "POST":
            try:
                assignment_id = int(request.form.get("assignment_id"))
                student_id = int(request.form.get("student_id"))

                assignment = Assignment.query.get_or_404(assignment_id)

                score_value = to_score(request.form.get("score"), assignment.max_score)
                note_text = (request.form.get("grader_note") or "").strip()

                submission = Submission(
                    assignment_id=assignment_id,
                    student_id=student_id,
                    score=score_value,
                    grader_note=note_text,
                    submitted_at=datetime.utcnow(),
                    last_updated=datetime.utcnow(),
                )

                db.session.add(submission)
                db.session.flush()

                db.session.add(
                    ActivityLog(
                        event_type="submission_created",
                        reference_table="submissions",
                        reference_id=submission.submission_id,
                        event_note=(
                            f"Submission stored for student #{student_id} "
                            f"on assignment #{assignment_id}."
                        ),
                    )
                )

                recalculate_progress(student_id, assignment.course_id)

                db.session.commit()

                flash("Submission recorded and progress updated in one transaction.", "success")
                return redirect(url_for("submissions"))

            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "danger")

            except IntegrityError:
                db.session.rollback()
                flash("A submission for this student and assignment already exists.", "danger")

            except Exception as exc:
                db.session.rollback()
                flash(f"Unexpected error while recording submission: {exc}", "danger")

        return render_template(
            "submission_form.html",
            assignments=assignments,
            students=students,
        )

    @app.route("/relationships")
    def relationships():
        course_rows = Course.query.order_by(Course.course_name.asc()).all()
        return render_template("relationships.html", courses=course_rows)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)