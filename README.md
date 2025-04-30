# 🏫 Student Management System

A web-based Student Management System built using **Flask** and **SQLite**. This application provides secure, role-based access for principals, teachers, and students to manage and view academic information.

## 🚀 Features

- **Role-Based Authentication**:
  - 🔑 **Principal**: Add, update, delete, and view all students and teachers.
  - 👩‍🏫 **Teacher**: Add, update, delete, and view students in their assigned batch.
  - 👨‍🎓 **Student**: View personal academic information only.

- **Dashboards**:
  - Principal Dashboard
  - Teacher Dashboard (with filtered student data)
  - Student Dashboard

- **Data Operations**:
  - Add/Update/Delete Teachers
  - Add/Update/Delete Students
  - View all users (for principal)

## 🧰 Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite (WAL mode enabled)
- **Frontend**: HTML + Jinja Templates
- **Session Management**: Flask sessions

## 📁 Project Structure

student-management-system/ │ ├── templates/ │ ├── login.html │ ├── principal_dashboard.html │ ├── teacher_dashboard.html │ ├── student_dashboard.html │ ├── add_teacher.html │ ├── add_student.html │ ├── view_teachers.html │ └── view_students.html │ ├── static/ │ └── (Optional CSS or JS files) │ ├── school_management_demo.db # SQLite Database ├── app.py # Main Flask App └── README.md # Project Documentation
