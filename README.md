# Student Assignment Tracker (DBMS Project 3)

## Description :

This project is a full-stack database application built using Flask, SQLAlchemy, and SQLite.

The goal of the system is to manage students, courses, enrollments, assignments, and submissions in a simple academic setting. While building this, I focused on applying database concepts like normalization, relationships, validation, and transactions in a practical way.

---

## Features

- Add, edit, and delete students
- Manage courses and instructors
- Enroll students into courses
- Create assignments for each course
- Record student submissions with scores
- Automatically update student progress
- Maintain activity logs for submissions
- View dashboard with basic summary metrics

---

## Technologies Used : 

- Python (Flask)
- SQLAlchemy
- SQLite
- HTML (Jinja templates)
- Bootstrap (for UI)

---

## Core Functionality

### 1. CRUD Operations
- Students and Courses support full CRUD operations  
- Enrollments, Assignments, and Submissions are created and viewed through forms  

### 2. Relationships
- Students and Courses have a many-to-many relationship through the Enrollment table  
- Each Course can have multiple Assignments  
- Each Student can have multiple Submissions  

### 3. Transaction Handling
When a submission is recorded, the following happens together:
- A submission record is inserted  
- An activity log entry is created  
- The student’s course progress is recalculated  

If any step fails, the transaction is rolled back.

### 4. Validation
- Empty fields are not allowed  
- Email must be unique  
- Duplicate enrollments are prevented  
- Scores must be within valid range  
- Dates are validated (including reasonable year limits)  
- End date cannot be before start date  

---

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


## GitHub Repository

https://github.com/r387k939/HemanthKumar

## Usage

 ## How to Run the Project

1. Navigate to the project folder:

```bash
cd hemanth_dbms_project3_submission
```

2. Start the server:

```bash
python app.py
```

3. Open in the browser:

```text
http://127.0.0.1:5000/
```