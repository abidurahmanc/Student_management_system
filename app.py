from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3

# admin id:admin
# admin password:admin123

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def get_db_connection():
    conn = sqlite3.connect('school_management_demo.db', timeout=10)  # Increased timeout
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode
    return conn


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check principal login
    cursor.execute("SELECT * FROM principals WHERE id = ? AND password = ?", (id, password))
    principal = cursor.fetchone()
    if principal:
        session['user_id'] = principal['id']
        session['role'] = 'principal'
        return jsonify({'success': True, 'redirect': url_for('principal_dashboard')})

    # Check teacher login
    cursor.execute("SELECT * FROM teachers WHERE id = ? AND password = ?", (id, password))
    teacher = cursor.fetchone()
    if teacher:
        session['user_id'] = teacher['id']
        session['role'] = 'teacher'
        return jsonify({'success': True, 'redirect': url_for('teacher_dashboard')})

    # Check student login
    cursor.execute("SELECT * FROM students WHERE id = ? AND password = ?", (id, password))
    student = cursor.fetchone()
    if student:
        session['user_id'] = student['id']
        session['role'] = 'student'
        return jsonify({'success': True, 'redirect': url_for('student_dashboard')})

    conn.close()
    return jsonify({'success': False, 'message': 'Invalid ID or Password'})


@app.route('/principal_dashboard')
def principal_dashboard():
    if 'role' not in session or session['role'] != 'principal':
        return redirect(url_for('index'))
    return render_template('principal_dashboard.html')

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT batch FROM teachers WHERE id = ?", (session['user_id'],))
    teacher = cursor.fetchone()
    cursor.execute("SELECT * FROM students WHERE batch = ?", (teacher['batch'],))
    students = cursor.fetchall()
    conn.close()
    
    return render_template('teacher_dashboard.html', students=students, batch=teacher['batch'])

@app.route('/student_dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (session['user_id'],))
    student = cursor.fetchone()
    conn.close()
    
    return render_template('student_dashboard.html', student=student)
@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if 'role' not in session or session['role'] != 'principal':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        qualification = request.form['qualification']
        place = request.form['place']
        batch = request.form['batch']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO teachers (id, name, password, qualification, place, batch) VALUES (?, ?, ?, ?, ?, ?)",
                      (id, name, password, qualification, place, batch))
        conn.commit()

        cursor.close()
        conn.close()
        flash('Teacher added successfully')
        return redirect(url_for('principal_dashboard'))

    return render_template('add_teacher.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'role' not in session or session['role'] not in ['principal', 'teacher']:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        batch = request.form['batch']
        python_mark = request.form['python_mark']
        english_mark = request.form['english_mark']
        statistics_mark = request.form['statistics_mark']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO students (id, name, password, batch, python_mark, english_mark, statistics_mark) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (id, name, password, batch, python_mark, english_mark, statistics_mark))
        conn.commit()

        cursor.close()
        conn.close()
        flash('Student added successfully')

        if session['role'] == 'principal':
            return redirect(url_for('principal_dashboard'))
        return redirect(url_for('teacher_dashboard'))

    return render_template('add_student.html')
@app.route('/view_teachers')
def view_teachers():
    if 'role' not in session or session['role'] != 'principal':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('view_teachers.html', teachers=teachers)

@app.route('/view_students')
def view_students():
    if 'role' not in session or session['role'] != 'principal':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('view_students.html', students=students)

@app.route('/update_teacher/<id>', methods=['GET', 'POST'])
def update_teacher(id):
    if 'role' not in session or session['role'] != 'principal':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        qualification = request.form['qualification']
        place = request.form['place']
        batch = request.form['batch']

        cursor.execute("""
            UPDATE teachers 
            SET name = ?, qualification = ?, place = ?, batch = ? 
            WHERE id = ?
        """, (name, qualification, place, batch, id))
        conn.commit()

        cursor.close()
        conn.close()
        flash('Teacher updated successfully')
        return redirect(url_for('view_teachers'))

    cursor.execute("SELECT * FROM teachers WHERE id = ?", (id,))
    teacher = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('add_teacher.html', teacher=teacher, update=True)

@app.route('/delete_teacher/<id>')
def delete_teacher(id):
    if 'role' not in session or session['role'] != 'principal':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teachers WHERE id = ?", (id,))
    # cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    flash('Teacher deleted successfully')
    
    return redirect(url_for('view_teachers'))

@app.route('/update_student/<id>', methods=['GET', 'POST'])
def update_student(id):
    if 'role' not in session or session['role'] not in ['principal', 'teacher']:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        batch = request.form['batch']
        python_mark = request.form['python_mark']
        english_mark = request.form['english_mark']
        statistics_mark = request.form['statistics_mark']

        cursor.execute("""
            UPDATE students 
            SET name = ?, batch = ?, python_mark = ?, english_mark = ?, statistics_mark = ? 
            WHERE id = ?
        """, (name, batch, python_mark, english_mark, statistics_mark, id))
        conn.commit()

        cursor.close()
        conn.close()
        flash('Student updated successfully')

        if session['role'] == 'principal':
            return redirect(url_for('view_students'))
        return redirect(url_for('teacher_dashboard'))

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('add_student.html', student=student, update=True)

@app.route('/delete_student/<id>')
def delete_student(id):
    if 'role' not in session or session['role'] not in ['principal', 'teacher']:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    # cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    flash('Student deleted successfully')
    
    if session['role'] == 'principal':
        return redirect(url_for('view_students'))
    return redirect(url_for('teacher_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
