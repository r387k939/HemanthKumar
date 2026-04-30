# Normalization Report

## 1. Initial Database Structure

At the beginning of the project, the database consisted of the following main tables:

- students(student_id, full_name, email, program_name, student_status, created_at)  
- courses(course_id, course_name, instructor_name, start_date, end_date, created_at)  
- enrollments(enrollment_id, student_id, course_id, enrollment_date, progress_percent, record_source)  
- assignments(assignment_id, course_id, title, max_score, due_date, created_at)  
- submissions(submission_id, assignment_id, student_id, submitted_at, score, grader_note, last_updated)  

Although this structure worked functionally, some fields such as program name, instructor name, and status were stored repeatedly as plain text. This created redundancy and increased the risk of inconsistent data.

---

## 2. Functional Dependencies

### Students
- student_id → full_name, email, program_name, student_status, created_at  
- email → student_id, full_name, program_name, student_status, created_at  

### Courses
- course_id → course_name, instructor_name, start_date, end_date, created_at  

### Enrollments
- enrollment_id → student_id, course_id, enrollment_date, progress_percent, record_source  
- (student_id, course_id) → enrollment_date, progress_percent, record_source  

### Assignments
- assignment_id → course_id, title, max_score, due_date, created_at  
- (course_id, title) → max_score, due_date, created_at  

### Submissions
- submission_id → assignment_id, student_id, submitted_at, score, grader_note, last_updated  
- (assignment_id, student_id) → submitted_at, score, grader_note, last_updated  

---

## 3. Data Anomalies Identified

### Update Issues
Some values like program names, instructor names, and record sources were stored directly in multiple rows.

For example, if the program name “Computer Science” needed to be updated, every record containing that value would need to be changed. Missing even one row would lead to inconsistent data.

---

### Insertion Issues
In the original structure, certain data could not be added independently.

For instance, a new program such as “Cybersecurity” could not be stored unless a student was already associated with it. Similarly, an instructor could not be added unless a course existed for them.

---

### Deletion Issues
Deleting records could accidentally remove useful information.

For example, deleting the last student in a program would remove the only occurrence of that program. The same issue applies to instructors when their last course is removed.

---

## 4. Normalization Process

### Step 1: Separating Program and Status

Originally, program and status were stored as text inside the students table.

To fix this, they were moved into separate lookup tables:

- programs(program_id, program_name)  
- student_statuses(status_id, status_name)  

The students table was updated to reference these using foreign keys.

This removes duplication and ensures consistency.

---

### Step 2: Separating Instructor Data

Instructor names were originally stored directly in the courses table.

This was improved by creating:

- instructors(instructor_id, instructor_name)  

The courses table now stores instructor_id instead of repeating names.

---

### Step 3: Handling Record Source Properly

The enrollment source field (like manual or import) was stored as plain text.

A new table was created:

- record_sources(source_id, source_name)  

The enrollments table now references this using source_id, avoiding inconsistencies.

---

### Step 4: Adding Constraints

To strengthen data integrity, the following constraints were added:

- Unique email for students  
- Unique student-course pair in enrollments  
- Unique assignment title per course  
- Unique submission per student per assignment  

These constraints prevent duplicate or invalid data entries.

---

## 5. Final Database Structure

The final schema includes:

- programs  
- student_statuses  
- record_sources  
- instructors  
- students  
- courses  
- enrollments  
- assignments  
- submissions  
- activity_logs  

Each table has a clear purpose, and relationships are maintained using foreign keys.

---

## 6. Why This Design Is in 3NF

The final database design meets Third Normal Form because:

- Each table has a clearly defined primary key  
- All non-key attributes depend only on the primary key  
- There are no indirect (transitive) dependencies  
- Repeated values are moved into separate lookup tables  
- Relationships are handled using foreign keys  

For example:
- Student details depend only on student_id  
- Course details depend only on course_id  
- Enrollment records represent relationships between students and courses  

---

## 7. How This Connects to the Application

The Flask application is built on top of this normalized structure.

- Student pages use students, programs, and statuses  
- Course pages use courses and instructors  
- Enrollment pages connect students and courses  
- Submission logic updates progress and logs activity  

This confirms that the application directly uses the normalized schema.

---


## ER Diagram (Simplified)

Students → Enrollments → Courses  
Courses → Assignments → Submissions  
Submissions → Activity Logs


## 8. Conclusion

The initial design had repeated values that could cause update, insertion, and deletion problems.  

After normalization, the database is more organized, avoids duplication, and maintains data consistency.

The final structure follows Third Normal Form and supports the application effectively.