Student Management System
A web-based application built with Flask and SQLite that manages students, teachers, and principals in a school environment. It supports role-based authentication and allows different levels of data access and manipulation based on user roles.

🚀 Features
Role-based Login System:

Principal can view, add, update, and delete students and teachers.

Teachers can view and manage students in their assigned batch.

Students can log in and view their personal academic data.

Functional Dashboards:

Principal Dashboard

Teacher Dashboard (filtered by batch)

Student Dashboard

Data Management:

Add, update, delete teachers

Add, update, delete students

View lists of all teachers and students (for Principal only)

🧰 Tech Stack
Backend: Python, Flask

Database: SQLite (with WAL mode for better concurrency)

Frontend: HTML, Jinja2 Templates

Authentication: Session-based login
