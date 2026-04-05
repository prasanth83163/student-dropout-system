"""
Student Dropout Prediction & Counselling System - Flask Backend
Main application file with all routes and backend logic.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

DATABASE = 'database.db'


# ==================== DATABASE HELPER FUNCTIONS ====================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def close_db_connection(conn):
    if conn:
        conn.close()


# ==================== AUTHENTICATION DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def staff_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] not in ['admin', 'staff']:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    return render_template('index 1.html')


# ==================== LOGIN ROUTES ====================

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        admin = conn.execute(
            'SELECT * FROM admins WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        close_db_connection(conn)

        if admin:
            session['user_id'] = admin['id']
            session['username'] = admin['username']
            session['user_role'] = 'admin'
            session['full_name'] = admin['full_name']
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin-login.html', error='Invalid credentials')

    return render_template('admin-login.html')


@app.route('/staff-login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        staff = conn.execute(
            'SELECT * FROM staff WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        close_db_connection(conn)

        if staff:
            session['user_id'] = staff['id']
            session['username'] = staff['username']
            session['user_role'] = 'staff'
            session['full_name'] = staff['full_name']
            return redirect(url_for('staff_dashboard'))
        else:
            return render_template('staff-login.html', error='Invalid credentials')

    return render_template('staff-login.html')


@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        register_number = request.form.get('registerNumber')
        password = request.form.get('password')

        conn = get_db_connection()
        student = conn.execute(
            'SELECT * FROM students WHERE register_number = ? AND password = ?',
            (register_number, password)
        ).fetchone()
        close_db_connection(conn)

        if student:
            session['user_id'] = student['id']
            session['username'] = student['register_number']
            session['user_role'] = 'student'
            session['full_name'] = student['name']
            return redirect(url_for('student_dashboard'))
        else:
            return render_template('student-login.html', error='Invalid credentials')

    return render_template('student-login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ==================== DASHBOARD ROUTES ====================

@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()

    total_students = conn.execute(
        'SELECT COUNT(*) FROM students'
    ).fetchone()[0]

    high_risk = conn.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level = 'High'"
    ).fetchone()[0]

    medium_risk = conn.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level = 'Medium'"
    ).fetchone()[0]

    low_risk = conn.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level = 'Low'"
    ).fetchone()[0]

    total_staff = conn.execute(
        'SELECT COUNT(*) FROM staff'
    ).fetchone()[0]

    counselling_sessions = conn.execute(
        'SELECT COUNT(*) FROM counselling_sessions'
    ).fetchone()[0]

    all_students = conn.execute('''
        SELECT id, name, register_number, department, year, attendance, average_marks, risk_level, status
        FROM students
        ORDER BY name
    ''').fetchall()

    high_risk_students = conn.execute('''
        SELECT id, name, register_number, department, year, attendance, average_marks, risk_level, status
        FROM students
        WHERE risk_level = 'High'
        ORDER BY name
    ''').fetchall()

    recent_counselling = conn.execute('''
        SELECT
            cs.session_type,
            cs.session_date,
            cs.status as counselling_status,
            s.name as student_name,
            s.register_number,
            s.risk_level,
            st.full_name as counsellor_name
        FROM counselling_sessions cs
        LEFT JOIN students s ON cs.student_id = s.id
        LEFT JOIN staff st ON cs.counsellor_id = st.id
        ORDER BY cs.session_date DESC
        LIMIT 10
    ''').fetchall()

    department_distribution = conn.execute('''
        SELECT
            department,
            SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) as high_count,
            SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) as medium_count,
            SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) as low_count
        FROM students
        GROUP BY department
        ORDER BY department
    ''').fetchall()

    close_db_connection(conn)

    return render_template(
        'admin-dashboard.html',
        total_students=total_students,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        total_staff=total_staff,
        counselling_sessions=counselling_sessions,
        all_students=all_students,
        high_risk_students=high_risk_students,
        recent_counselling=recent_counselling,
        department_distribution=department_distribution
    )

@app.route('/staff-dashboard')
@login_required
def staff_dashboard():
    if session.get('user_role') != 'staff':
        return redirect(url_for('index'))

    conn = get_db_connection()

    assigned_students = conn.execute(
        'SELECT COUNT(*) FROM students'
    ).fetchone()[0]

    high_risk = conn.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level = 'High'"
    ).fetchone()[0]

    medium_risk = conn.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level = 'Medium'"
    ).fetchone()[0]

    low_risk = conn.execute(
        "SELECT COUNT(*) FROM students WHERE risk_level = 'Low'"
    ).fetchone()[0]

    high_risk_students = conn.execute('''
        SELECT id, name, register_number, department, year, attendance, average_marks, risk_level, status
        FROM students
        WHERE risk_level = 'High'
        ORDER BY name
        LIMIT 10
    ''').fetchall()

    all_students = conn.execute('''
        SELECT id, name, register_number, department, year, attendance, average_marks, risk_level, status
        FROM students
        ORDER BY name
    ''').fetchall()

    close_db_connection(conn)

    return render_template(
        'staff-dashboard.html',
        assigned_students=assigned_students,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        high_risk_students=high_risk_students,
        all_students=all_students
    )


@app.route('/student-dashboard')
@login_required
def student_dashboard():
    if session.get('user_role') != 'student':
        return redirect(url_for('index'))

    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (session['user_id'],)
    ).fetchone()

    counselling_history = conn.execute('''
        SELECT cs.*, st.full_name as counsellor_name
        FROM counselling_sessions cs
        LEFT JOIN staff st ON cs.counsellor_id = st.id
        WHERE cs.student_id = ?
        ORDER BY cs.session_date DESC
        LIMIT 10
    ''', (session['user_id'],)).fetchall()

    close_db_connection(conn)

    return render_template(
        'student-dashboard.html',
        student=student,
        counselling_history=counselling_history
    )


# ==================== PAGE ROUTES FOR SIDEBAR / NAVIGATION ====================

@app.route('/view-all-students')
@login_required
def view_all_students():
    if session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('index'))

    conn = get_db_connection()

    department = request.args.get('department')
    risk_level = request.args.get('risk_level')
    year = request.args.get('year')
    search = request.args.get('search')

    query = 'SELECT * FROM students WHERE 1=1'
    params = []

    if department:
        query += ' AND department = ?'
        params.append(department)
    if risk_level:
        query += ' AND risk_level = ?'
        params.append(risk_level)
    if year:
        query += ' AND year = ?'
        params.append(year)
    if search:
        query += ' AND (name LIKE ? OR register_number LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    query += ' ORDER BY name'

    students = conn.execute(query, params).fetchall()
    close_db_connection(conn)

    return render_template('view-all-students.html', students=students)


@app.route('/api/students')
@login_required
def students_redirect():
    return redirect(url_for('view_all_students'))


@app.route('/high-risk-students')
@login_required
def high_risk_students():
    if session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('index'))

    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students WHERE risk_level = 'High' ORDER BY name"
    ).fetchall()
    close_db_connection(conn)

    return render_template('view-all-students.html', students=students)


@app.route('/counselling')
@login_required
def counselling_page():
    if session.get('user_role') not in ['admin', 'staff', 'student']:
        return redirect(url_for('index'))

    conn = get_db_connection()

    if session.get('user_role') == 'student':
        sessions = conn.execute('''
            SELECT cs.*, st.full_name as counsellor_name
            FROM counselling_sessions cs
            LEFT JOIN staff st ON cs.counsellor_id = st.id
            WHERE cs.student_id = ?
            ORDER BY cs.session_date DESC
        ''', (session['user_id'],)).fetchall()
    else:
        sessions = conn.execute('''
            SELECT cs.*, s.name as student_name, s.register_number, st.full_name as counsellor_name
            FROM counselling_sessions cs
            JOIN students s ON cs.student_id = s.id
            LEFT JOIN staff st ON cs.counsellor_id = st.id
            ORDER BY cs.session_date DESC
        ''').fetchall()

    close_db_connection(conn)
    return render_template('counselling.html', sessions=sessions)


@app.route('/counselling-logs')
@login_required
def counselling_logs():
    return redirect(url_for('counselling_page'))


@app.route('/reports')
@login_required
def reports_page():
    if session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('index'))
    return render_template('reports-analytics.html')


@app.route('/reports-analytics')
@login_required
def reports_analytics():
    if session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('index'))
    return render_template('reports-analytics.html')


@app.route('/voice-counselling')
@login_required
def voice_counselling():
    return render_template('voice-counselling.html')


@app.route('/ai-chat-counselling')
@login_required
def ai_chat_counselling():
    return render_template('ai-chat-counselling.html')


@app.route('/ai-chat-simple')
@login_required
def ai_chat_simple():
    return render_template('ai-chat-simple.html')


@app.route('/manage-staff')
@login_required
def manage_staff():
    if session.get('user_role') != 'admin':
        return redirect(url_for('index'))
    return render_template('staff-dashboard.html')



    


# ==================== STUDENT MANAGEMENT ROUTES ====================

@app.route('/api/students', methods=['GET'])
@login_required
def api_get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    close_db_connection(conn)

    students_list = [dict(student) for student in students]
    return jsonify(students_list)


@app.route('/students/add', methods=['POST'])
@login_required
def add_student():
    if session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('index'))

    data = request.form
    conn = None

    try:
        attendance = float(data.get('attendance', 0))
        marks = float(data.get('average_marks', 0))

        if attendance < 50 or marks < 40:
            risk_level = 'High'
        elif attendance < 75 or marks < 60:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO students (
                register_number, password, name, email, phone,
                department, year, attendance, average_marks, risk_level, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('register_number'),
            data.get('password', 'student123'),
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('department'),
            int(data.get('year')),
            attendance,
            marks,
            risk_level,
            'Active'
        ))
        conn.commit()
        close_db_connection(conn)

        return redirect(url_for('view_all_students'))

    except Exception as e:
        if conn:
            close_db_connection(conn)
        return f"Error adding student: {str(e)}", 400


@app.route('/students/update/<int:id>', methods=['POST'])
@admin_required
def update_student(id):
    data = request.form

    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE students SET
                name = ?, email = ?, phone = ?, department = ?,
                year = ?, attendance = ?, average_marks = ?,
                risk_level = ?, status = ?
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('department'),
            int(data.get('year')),
            float(data.get('attendance')),
            float(data.get('average_marks')),
            data.get('risk_level'),
            data.get('status'),
            id
        ))
        conn.commit()
        close_db_connection(conn)

        return jsonify({'success': True, 'message': 'Student updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/students/delete/<int:id>', methods=['POST'])
@admin_required
def delete_student(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        close_db_connection(conn)

        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== COUNSELLING ROUTES ====================

@app.route('/api/counselling', methods=['GET'])
@login_required
def api_get_counselling():
    conn = get_db_connection()

    if session.get('user_role') == 'student':
        sessions = conn.execute('''
            SELECT cs.*, st.full_name as counsellor_name
            FROM counselling_sessions cs
            LEFT JOIN staff st ON cs.counsellor_id = st.id
            WHERE cs.student_id = ?
            ORDER BY cs.session_date DESC
        ''', (session['user_id'],)).fetchall()
    else:
        sessions = conn.execute('''
            SELECT cs.*, s.name as student_name, s.register_number, st.full_name as counsellor_name
            FROM counselling_sessions cs
            JOIN students s ON cs.student_id = s.id
            LEFT JOIN staff st ON cs.counsellor_id = st.id
            ORDER BY cs.session_date DESC
        ''').fetchall()

    close_db_connection(conn)

    sessions_list = [dict(row) for row in sessions]
    return jsonify(sessions_list)


@app.route('/counselling/add', methods=['POST'])
@login_required
def add_counselling_session():
    data = request.form

    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO counselling_sessions
            (student_id, counsellor_id, session_type, session_date, notes, status, follow_up_required)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(data.get('student_id')),
            session['user_id'] if session.get('user_role') == 'staff' else None,
            data.get('session_type'),
            data.get('session_date'),
            data.get('notes'),
            'Scheduled',
            1 if data.get('follow_up_required') else 0
        ))
        conn.commit()
        close_db_connection(conn)

        return jsonify({'success': True, 'message': 'Counselling session added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== AI CHAT ROUTES ====================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.json
    user_message = data.get('message', '').lower()

    responses = {
        'stress': "I understand you're feeling stressed. This is common among students. Try breaking tasks into smaller steps, maintain a regular sleep schedule, and don't hesitate to reach out to your counsellor.",
        'anxiety': "Anxiety can be challenging, but remember you're not alone. Practice deep breathing exercises, focus on what you can control, and consider scheduling a counselling session.",
        'depressed': "I hear that you're feeling down. It's important to talk to someone about this. Please consider reaching out to your counsellor or a trusted faculty member.",
        'study': "Effective studying requires good time management. Try the Pomodoro technique (25 min study + 5 min break), create a dedicated study space, and review material regularly.",
        'attendance': "Attendance is important for academic success. If you're struggling to attend classes, let's discuss the challenges and find solutions together.",
        'marks': "Academic performance can be improved with the right strategies. Consider forming study groups, attending office hours, and seeking help from tutors.",
        'default': "Thank you for sharing. I'm here to listen and support you. Would you like to schedule a counselling session to discuss this further?"
    }

    response = responses['default']
    for keyword in responses:
        if keyword in user_message:
            response = responses[keyword]
            break

    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })


# ==================== REPORTS & ANALYTICS ROUTES ====================

@app.route('/api/reports', methods=['GET'])
@login_required
def api_get_reports():
    conn = get_db_connection()

    dept_risk = conn.execute('''
        SELECT department, risk_level, COUNT(*) as count
        FROM students
        GROUP BY department, risk_level
        ORDER BY department
    ''').fetchall()

    trend_data = conn.execute('''
        SELECT
            strftime('%Y-%m', created_at) as month,
            COUNT(*) as count
        FROM students
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    ''').fetchall()

    close_db_connection(conn)

    return jsonify({
        'department_risk': [dict(row) for row in dept_risk],
        'trend': [dict(row) for row in trend_data]
    })


@app.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard_stats():
    conn = get_db_connection()

    stats = {
        'total_students': conn.execute('SELECT COUNT(*) FROM students').fetchone()[0],
        'active_students': conn.execute("SELECT COUNT(*) FROM students WHERE status = 'Active'").fetchone()[0],
        'high_risk': conn.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'High'").fetchone()[0],
        'medium_risk': conn.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'Medium'").fetchone()[0],
        'low_risk': conn.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'Low'").fetchone()[0],
        'counselling_sessions': conn.execute('SELECT COUNT(*) FROM counselling_sessions').fetchone()[0],
        'staff_count': conn.execute('SELECT COUNT(*) FROM staff').fetchone()[0]
    }

    close_db_connection(conn)
    return jsonify(stats)
@app.route('/add-student')
@login_required
def add_student_page():
    if session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('index'))
    return render_template('add-student.html')


@app.route('/save-voice-note', methods=['POST'])
@login_required
def save_voice_note():
    if session.get('user_role') != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json()
    notes = data.get('notes', '').strip()

    if not notes:
        return jsonify({'success': False, 'message': 'Notes are empty'}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO counselling_sessions
        (student_id, counsellor_id, session_type, session_date, notes, status, follow_up_required)
        VALUES (?, ?, ?, date('now'), ?, ?, ?)
    ''', (
        session['user_id'],
        None,
        'Voice Counselling',
        notes,
        'Completed',
        0
    ))
    conn.commit()
    close_db_connection(conn)

    return jsonify({'success': True, 'message': 'Counselling notes saved successfully'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('index 1.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return "Internal server error", 500


# ==================== MAIN EXECUTION ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("STUDENT DROPOUT PREDICTION & COUNSELLING SYSTEM")
    print("=" * 60)
    print("\nStarting Flask development server...")
    print("\nAccess the application at:")
    print("  Local:   http://localhost:5000")
    print("  Network: http://YOUR_LOCAL_IP:5000")
    print("\nTo find your local IP address:")
    print("  Windows: Run 'ipconfig' in terminal")
    print("  Look for 'IPv4 Address' under your network adapter")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)