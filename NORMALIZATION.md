# Normalization Report

## 1. Original Schema Definition

The original schema from the previous database (Project 2.0) contained the following tables:

- students(student_id, full_name, email, program_name, student_status, created_at)
- courses(course_id, course_name, instructor_name, start_date, end_date, created_at)
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, record_source)
- assignments(assignment_id, course_id, title, max_score, due_date, created_at)
- submissions(submission_id, assignment_id, student_id, submitted_at, score, grader_note, last_updated)

---

## 2. Functional Dependencies in the Original Schema

### students
- student_id → full_name, email, program_name, student_status, created_at  
- email → full_name, program_name, student_status, created_at  
  (Assuming email uniquely identifies a student)

### courses
- course_id → course_name, instructor_name, start_date, end_date, created_at  

### enrollments
- enrollment_id → student_id, course_id, enrollment_date, progress_percent, record_source  
- (student_id, course_id) → enrollment_date, progress_percent, record_source  

### assignments
- assignment_id → course_id, title, max_score, due_date, created_at  
- (course_id, title) → max_score, due_date, created_at  

### submissions
- submission_id → assignment_id, student_id, submitted_at, score, grader_note, last_updated  
- (assignment_id, student_id) → submitted_at, score, grader_note, last_updated  

---


## 3. Potential Anomalies in the Original Structure

Even though the original design was already somewhat close to 3NF, I noticed a few practical issues while reviewing the schema, especially related to repeated values and maintainability.

### A. Update Anomaly

- Fields like `program_name`, `student_status`, `instructor_name`, and `record_source` were stored as plain text across multiple rows.
- If a value needed correction (for example, fixing a program name), it would require updating many records.
- This increases the risk of inconsistent values such as:
  - "Computer Science"
  - "computer science"
  - "Comp. Science"

---

### B. Insertion Anomaly

- It was not possible to store a new program, instructor, or record source independently.
- These values could only be added when inserting a related student, course, or enrollment.
- This makes the schema less flexible for managing reference data.

---

### C. Deletion Anomaly

- If the last student in a program is deleted, the program itself disappears from the system.
- Similarly, removing the last course taught by an instructor removes all trace of that instructor.

---

## 4. Decomposition Steps Toward 3NF

The original structure did not have repeating groups, but improvements were made by separating reusable values into dedicated lookup tables.

---

### Step 1: Normalize Student Attributes

**Original:**
- students(student_id, full_name, email, program_name, student_status, created_at)

**Decomposed into:**
- programs(program_id, program_name)  
- student_statuses(status_id, status_name)  
- students(student_id, full_name, email, program_id, status_id, created_at)

**Reason:**
- `program_name` and `student_status` are descriptive categories, not independent student facts.
- Using IDs reduces duplication and improves consistency.

---

### Step 2: Normalize Instructor Information

**Original:**
- courses(course_id, course_name, instructor_name, start_date, end_date, created_at)

**Decomposed into:**
- instructors(instructor_id, instructor_name)  
- courses(course_id, course_name, instructor_id, start_date, end_date, created_at)

**Reason:**
- Instructor names can repeat across multiple courses.
- Storing them in a separate table avoids redundancy and simplifies updates.

---

### Step 3: Normalize Enrollment Source

**Original:**
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, record_source)

**Decomposed into:**
- record_sources(source_id, source_name)  
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, source_id)

**Reason:**
- `record_source` is a controlled label and fits better as a lookup table.

---

### Step 4: Add Constraints and Keys

The final design includes the following constraints:

- UNIQUE(email) in students  
- UNIQUE(student_id, course_id) in enrollments  
- UNIQUE(course_id, title) in assignments  
- UNIQUE(assignment_id, student_id) in submissions  

**Reason:**
- These constraints prevent duplicate or inconsistent data.
- They reflect real-world rules of the system.

Additionally, these constraints were added after reviewing how the application behaves during testing, ensuring data integrity in real scenarios.

---

## 5. Why the Final Design is in 3NF

The final schema satisfies Third Normal Form (3NF) because:

1. Each table has a clearly defined primary key  
2. All non-key attributes depend on the whole key  
3. No non-key attribute depends on another non-key attribute  

### Examples:

- In `students`, attributes like `full_name` and `email` depend only on `student_id`, while descriptive data is referenced through foreign keys.
- In `courses`, course details depend only on `course_id`, and instructor data is stored separately.
- In `enrollments`, the table captures the relationship between a student and a course without redundant data.

---

## 6. NORMALIZATION REPORT

## Overview

The database is normalized to Third Normal Form (3NF).

---

## Functional Dependencies

- student_id → full_name, email, program_id, status_id
- course_id → course_name, instructor_id
- assignment_id → course_id, title, max_score

---

## 1NF

- All tables contain atomic values
- No repeating groups

---

## 2NF

- All non-key attributes depend on full primary key

---

## 3NF

- No transitive dependencies
- Lookup tables created:
  - programs
  - student_statuses
  - record_sources

---

## 6. Conclusion

The schema satisfies 3NF and prevents redundancy and anomalies.

## Git Hub Repository Link : " https://github.com/r387k939/HemanthKumar "