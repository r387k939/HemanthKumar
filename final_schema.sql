PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS activity_logs;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS instructors;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS record_sources;
DROP TABLE IF EXISTS student_statuses;
DROP TABLE IF EXISTS programs;

CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_name TEXT NOT NULL UNIQUE
);

CREATE TABLE student_statuses (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT NOT NULL UNIQUE
);

CREATE TABLE record_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL UNIQUE
);

CREATE TABLE instructors (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_name TEXT NOT NULL UNIQUE
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    program_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (program_id)
        REFERENCES programs(program_id),

    FOREIGN KEY (status_id)
        REFERENCES student_statuses(status_id)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    instructor_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (instructor_id)
        REFERENCES instructors(instructor_id)
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT NOT NULL,
    progress_percent REAL NOT NULL DEFAULT 0.00
        CHECK (progress_percent BETWEEN 0 AND 100),
    source_id INTEGER NOT NULL,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    FOREIGN KEY (source_id)
        REFERENCES record_sources(source_id),

    UNIQUE (student_id, course_id)
);

CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    max_score INTEGER NOT NULL CHECK (max_score > 0),
    due_date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    UNIQUE (course_id, title)
);

CREATE TABLE submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    score REAL CHECK (score >= 0),
    grader_note TEXT,
    last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (assignment_id)
        REFERENCES assignments(assignment_id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    UNIQUE (assignment_id, student_id)
);

CREATE TABLE activity_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    reference_table TEXT NOT NULL,
    reference_id INTEGER NOT NULL,
    event_note TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO programs (program_name)
VALUES
    ('Computer Science'),
    ('Data Science'),
    ('Information Systems');

INSERT INTO student_statuses (status_name)
VALUES
    ('Active'),
    ('Probation'),
    ('Graduated');

INSERT INTO record_sources (source_name)
VALUES
    ('Manual Entry'),
    ('Import'),
    ('Advisor Request');

INSERT INTO instructors (instructor_name)
VALUES
    ('Dr. Alice Bennett'),
    ('Prof. Marcus Lee'),
    ('Dr. Nina Shah');

INSERT INTO students (
    full_name,
    email,
    program_id,
    status_id
)
VALUES
    ('Bhavana Srivatsavai', 'bhavana@example.edu', 1, 1),
    ('Rahul Verma', 'rahul@example.edu', 2, 1),
    ('Ananya Patel', 'ananya@example.edu', 1, 2),
    ('Chris Miller', 'chris@example.edu', 3, 1);

INSERT INTO courses (
    course_name,
    instructor_id,
    start_date,
    end_date
)
VALUES
    ('Database Management Systems', 1, '2026-01-12', '2026-05-04'),
    ('Machine Learning Foundations', 2, '2026-01-12', '2026-05-04'),
    ('Cloud Data Engineering', 3, '2026-01-12', '2026-05-04');

INSERT INTO enrollments (
    student_id,
    course_id,
    enrollment_date,
    progress_percent,
    source_id
)
VALUES
    (1, 1, '2026-01-15', 50.00, 1),
    (1, 2, '2026-01-15', 50.00, 1),
    (2, 1, '2026-01-16', 50.00, 2),
    (3, 1, '2026-01-18', 0.00, 3),
    (4, 3, '2026-01-17', 0.00, 1);

INSERT INTO assignments (
    course_id,
    title,
    max_score,
    due_date
)
VALUES
    (1, 'Normalization Audit', 100, '2026-02-10'),
    (1, 'SQL Lab', 100, '2026-03-01'),
    (2, 'Feature Selection Review', 100, '2026-02-20'),
    (2, 'Model Evaluation Exercise', 100, '2026-03-18'),
    (3, 'Pipeline Design Memo', 100, '2026-02-28');

INSERT INTO submissions (
    assignment_id,
    student_id,
    submitted_at,
    score,
    grader_note
)
VALUES
    (1, 1, '2026-02-09 11:15:00', 94, 'Well structured write-up.'),
    (2, 1, '2026-02-27 19:10:00', 97, 'Good SQL coverage.'),
    (1, 2, '2026-02-10 08:45:00', 88, 'Nice work, add more detail on FDs.');

INSERT INTO activity_logs (
    event_type,
    reference_table,
    reference_id,
    event_note
)
VALUES
    ('seed', 'students', 1, 'Initial sample data loaded'),
    ('seed', 'courses', 1, 'Initial sample data loaded'),
    ('seed', 'submissions', 1, 'Initial sample data loaded');