# Student Assignment Tracker (DBMS Project 3)

## Description

This project is a full-stack database application built using Flask, SQLAlchemy, and SQLite.

The goal of the system is to manage students, courses, enrollments, assignments, and submissions in a simple academic setting. While building this project, I focused on applying database concepts such as normalization, relationships, validation, and transactions in a practical way.

---

## Key Insight

- The dashboard provides a quick summary of key data such as the number of students, courses, submissions, and the average scores.
- This makes it easier for instructors to get an overall view of student performance and track progress without going through individual records.

---

## My GitHub Repository Link

https://github.com/r387k939/HemanthKumar


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

## Technologies Used

- Python with Flask
- SQLAlchemy
- SQLite
- HTML with Jinja templates
- Bootstrap for the user interface

---

## Core Functionality

### 1. CRUD Operations

- Students and Courses support full create, read, update, and delete operations
- Enrollments, Assignments, and Submissions are created and viewed through forms

### 2. Relationships

- Students and Courses have a many-to-many relationship through the Enrollment table
- Each Course can have multiple Assignments
- Each Student can have multiple Submissions

### 3. Transaction Handling

When a submission is recorded, the following steps happen together:

- A submission record is inserted
- An activity log entry is created
- The student’s course progress is recalculated

If any step fails, the transaction is rolled back.

### 4. Validation

- Empty fields are not allowed
- Email must be unique
- Duplicate enrollments are prevented
- Scores must be within the valid range
- Dates are validated, including reasonable year limits
- End date cannot be before start date

---

## Installation Instructions on Mac OS

### 1. Clone the repository

```bash
git clone https://github.com/r387k939/HemanthKumar.git
cd HemanthKumar
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

This project uses SQLite for easy setup and grading.

The application automatically creates the database the first time it starts by running `final_schema.sql`.

If needed, the existing local database can be reset with:

```bash
rm -f instance/project3.db
```

Then run the app again:

```bash
python app.py
```

---

## How to Run the Project on Mac :

```bash
git clone https://github.com/r387k939/HemanthKumar.git
cd HemanthKumar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open browser:

```
http://127.0.0.1:5000/
```

## Installation Instructions on Mac OS

### 1. Clone the repository

git clone https://github.com/r387k939/HemanthKumar.git

cd HemanthKumar


### 2. Create and activate a virtual environment

Open Command Prompt inside the project folder and type below :

python -m venv venv

venv\Scripts\activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Run the application

python app.py


### 5. Opening in your favourite Browser

http://127.0.0.1:5000





