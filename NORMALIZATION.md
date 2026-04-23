# Normalization Report

## 1. Starting Point
The original schema from the earlier database project contained these tables:

- students(student_id, full_name, email, program_name, student_status, created_at)
- courses(course_id, course_name, instructor_name, start_date, end_date, created_at)
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, record_source)
- assignments(assignment_id, course_id, title, max_score, due_date, created_at)
- submissions(submission_id, assignment_id, student_id, submitted_at, score, grader_note, last_updated)

## 2. Functional Dependencies in the Original Schema
### students
- student_id -> full_name, email, program_name, student_status, created_at
- email -> full_name, program_name, student_status, created_at (business rule assumed: email should identify one student)

### courses
- course_id -> course_name, instructor_name, start_date, end_date, created_at

### enrollments
- enrollment_id -> student_id, course_id, enrollment_date, progress_percent, record_source
- (student_id, course_id) -> enrollment_date, progress_percent, record_source

### assignments
- assignment_id -> course_id, title, max_score, due_date, created_at
- (course_id, title) -> max_score, due_date, created_at

### submissions
- submission_id -> assignment_id, student_id, submitted_at, score, grader_note, last_updated
- (assignment_id, student_id) -> submitted_at, score, grader_note, last_updated

## 3. Potential Anomalies in the Original Structure
Even though the original design was already fairly close to 3NF, it still had some data-maintenance issues.

### A. Update anomaly
- `program_name`, `student_status`, `instructor_name`, and `record_source` were stored as plain text in multiple rows.
- If the spelling of a program or instructor changed, the same correction would have to be applied in many places.
- That creates a risk of inconsistent values such as `Computer Science`, `computer science`, and `Comp. Science`.

### B. Insertion anomaly
- A new program, status value, instructor, or record source could not be stored independently before a related student, course, or enrollment existed.
- In other words, reference values were mixed into transactional tables.

### C. Deletion anomaly
- If the last student in a program were deleted, the only visible trace of that program could disappear.
- If the last course taught by an instructor were removed, the instructor name would also vanish from the dataset.

## 4. Decomposition Steps Toward a Cleaner 3NF Design
The base structure already avoided obvious repeating groups, so the main improvement was to separate reusable lookup values from operational records.

### Step 1: Normalize student descriptors
Original:
- students(student_id, full_name, email, program_name, student_status, created_at)

Decomposed into:
- programs(program_id, program_name)
- student_statuses(status_id, status_name)
- students(student_id, full_name, email, program_id, status_id, created_at)

Why:
- `program_name` and `student_status` describe controlled categories, not independent student facts.
- Storing lookup IDs reduces repeated text and improves consistency.

### Step 2: Normalize instructor details from courses
Original:
- courses(course_id, course_name, instructor_name, start_date, end_date, created_at)

Decomposed into:
- instructors(instructor_id, instructor_name)
- courses(course_id, course_name, instructor_id, start_date, end_date, created_at)

Why:
- Instructor names are reusable reference values.
- If one instructor teaches multiple courses, a single row in `instructors` is easier to manage than repeated text values across courses.

### Step 3: Normalize enrollment source values
Original:
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, record_source)

Decomposed into:
- record_sources(source_id, source_name)
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, source_id)

Why:
- `record_source` is a controlled label and belongs in a small reference table.

### Step 4: Strengthen candidate keys and integrity rules
The final version also adds:
- `UNIQUE(email)` on students
- `UNIQUE(student_id, course_id)` on enrollments
- `UNIQUE(course_id, title)` on assignments
- `UNIQUE(assignment_id, student_id)` on submissions

Why:
- These constraints match the logical meaning of the data and prevent duplicate rows that would weaken the design.

## 5. Why the Final Design Is in 3NF
The final schema satisfies 3NF because:
1. Each table has a primary key.
2. Every non-key attribute depends on the whole key.
3. Non-key attributes do not depend on other non-key attributes inside the same table.

Examples:
- In `students`, `full_name`, `email`, and `created_at` depend on `student_id`; descriptive categories are referenced through `program_id` and `status_id`.
- In `courses`, course details depend on `course_id`, and instructor information is stored separately in `instructors`.
- In `enrollments`, the record captures a student-course relationship with its own facts; source information is referenced through `source_id`.

## 6. Final Relational Schema Used by the Python Application
- programs(program_id PK, program_name UNIQUE)
- student_statuses(status_id PK, status_name UNIQUE)
- record_sources(source_id PK, source_name UNIQUE)
- instructors(instructor_id PK, instructor_name UNIQUE)
- students(student_id PK, full_name, email UNIQUE, program_id FK, status_id FK, created_at)
- courses(course_id PK, course_name, instructor_id FK, start_date, end_date, created_at)
- enrollments(enrollment_id PK, student_id FK, course_id FK, enrollment_date, progress_percent, source_id FK, UNIQUE(student_id, course_id))
- assignments(assignment_id PK, course_id FK, title, max_score, due_date, created_at, UNIQUE(course_id, title))
- submissions(submission_id PK, assignment_id FK, student_id FK, submitted_at, score, grader_note, last_updated, UNIQUE(assignment_id, student_id))
- activity_logs(log_id PK, event_type, reference_table, reference_id, event_note, created_at)

## 7. Small Design Note
`activity_logs` was added as an application support table for transaction tracing in Part II. It is not part of the original classroom schema, but it helps demonstrate transactional behavior in a clean and auditable way.

## 8. Conclusion
The original project database was already organized reasonably well, but the final revision improves consistency by separating repeated descriptive values into lookup tables and by adding stronger uniqueness constraints. The resulting structure is easier to maintain, safer against anomalies, and better aligned with a production-style Flask application.
