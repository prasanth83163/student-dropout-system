# Student Dropout Prediction & Counselling System
## Flask Backend Integration - Setup & Run Instructions

### Prerequisites
- Python 3.8 or higher installed
- pip (Python package manager)

---

## Step-by-Step Setup Instructions

### Step 1: Install Python (if not already installed)
1. Download Python from https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Click "Install Now"
4. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

### Step 2: Navigate to Project Directory
Open Command Prompt or PowerShell and navigate to the project folder:
```powershell
cd "d:\qoder project"
```

### Step 3: Create Virtual Environment (Recommended)
A virtual environment keeps dependencies isolated:
```powershell
python -m venv venv
```

Activate the virtual environment:
- **Windows:**
  ```powershell
  .\venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Required Dependencies
Install Flask and other required packages:
```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Werkzeug (security utilities)

### Step 5: Initialize the Database
Run the database initialization script to create tables and sample data:
```powershell
python init_db.py
```

You should see output like:
```
Initializing database for Student Dropout Prediction & Counselling System...
------------------------------------------------------------
✓ Database tables created successfully!
✓ Sample data inserted successfully!
============================================================
DATABASE INITIALIZED SUCCESSFULLY!
============================================================

Default Login Credentials:
------------------------------------------------------------
Admin:   username = admin,    password = admin123
Staff:   username = staff,    password = staff123
Student: username = REG-2023-001, password = student123
============================================================
```

### Step 6: Start the Flask Application
Run the Flask app:
```powershell
python app.py
```

You should see:
```
============================================================
STUDENT DROPOUT PREDICTION & COUNSELLING SYSTEM
============================================================

Starting Flask development server...

Access the application at:
  Local:   http://localhost:5000
  Network: http://YOUR_LOCAL_IP:5000

To find your local IP address:
  Windows: Run 'ipconfig' in terminal
  Look for 'IPv4 Address' under your network adapter

Press Ctrl+C to stop the server
============================================================
```

### Step 7: Access the Application

#### On Desktop Browser:
1. Open your web browser
2. Go to: **http://localhost:5000**
3. You should see the landing page with login options

#### On Mobile Browser (Same Wi-Fi Network):
1. Find your local IP address:
   - **Windows:** Open Command Prompt and type `ipconfig`
   - Look for "IPv4 Address" under your active network adapter (e.g., `192.168.1.100`)
   
2. On your mobile device, open a browser and enter:
   ```
   http://YOUR_LOCAL_IP:5000
   ```
   Example: `http://192.168.1.100:5000`

3. The app should load on your mobile device!

**Note:** Both your laptop and mobile must be on the **same Wi-Fi network**.

---

## Default Login Credentials

### Admin Login
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system access, manage students and staff

### Staff Login
- **Username:** `staff`
- **Password:** `staff123`
- **Access:** View assigned students, conduct counselling sessions

### Student Login
- **Register Number:** `REG-2023-001`
- **Password:** `student123`
- **Access:** View own profile, counselling history, use AI chat

**Other sample student accounts:** REG-2023-002 through REG-2023-010 (all with password: `student123`)

---

## Features Implemented

### ✅ Authentication System
- Admin, Staff, and Student login with session management
- Secure password handling
- Role-based access control

### ✅ Dashboard Features
- **Admin Dashboard:** Overall statistics, risk distribution, department analytics
- **Staff Dashboard:** Assigned students, upcoming sessions
- **Student Dashboard:** Personal info, counselling history

### ✅ Student Management
- View all students with filtering
- Add new students
- Update student information
- Delete students
- Search functionality

### ✅ Counselling Module
- Schedule counselling sessions
- View counselling history
- Add session notes
- Track follow-up requirements
- AI Chat counselling (mock AI with keyword-based responses)

### ✅ Reports & Analytics
- Department-wise risk distribution
- Student statistics
- Counselling session reports
- Trend analysis

### ✅ API Endpoints
- `/api/dashboard` - Dashboard statistics
- `/api/students` - Student data
- `/api/counselling` - Counselling sessions
- `/api/reports` - Analytics data
- `/api/chat` - AI chat responses

---

## Project Structure

```
project-root/
├── app.py                  # Main Flask application
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (created after running init_db.py)
├── templates/            # HTML templates
│   ├── index 1.html
│   ├── admin-login.html
│   ├── admin-dashboard.html
│   ├── staff-login.html
│   ├── student-login.html
│   ├── view-all-students.html
│   ├── counselling.html
│   ├── ai-chat-counselling.html
│   ├── ai-chat-simple.html
│   └── reports-analytics.html
└── static/              # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

---

## Important Notes

### Security Warning ⚠️
This is a **development/demo setup**. For production use:
1. Change the `secret_key` in `app.py`
2. Implement proper password hashing (bcrypt, argon2)
3. Use HTTPS instead of HTTP
4. Add CSRF protection
5. Implement rate limiting
6. Use environment variables for sensitive data

### Database Reset
To reset the database to initial state:
1. Delete `database.db` file
2. Run `python init_db.py` again

### Stopping the Server
Press `Ctrl+C` in the terminal to stop the Flask server.

### Troubleshooting

**Port already in use:**
```powershell
# Kill process using port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Module not found error:**
```powershell
# Make sure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

**Database errors:**
```powershell
# Make sure you ran init_db.py first
python init_db.py
```

**Can't access from mobile:**
- Check firewall settings
- Ensure both devices are on same Wi-Fi
- Verify you're using the correct IP address
- Make sure Flask is running with `host='0.0.0.0'`

---

## Next Steps

1. **Explore the Application:**
   - Login as admin and explore the dashboard
   - Add/edit/delete students
   - View counselling sessions
   - Try the AI chat feature

2. **Customize Data:**
   - Add real student data through the admin panel
   - Update staff information
   - Modify departments as needed

3. **Extend Functionality:**
   - Add real AI integration for chat
   - Implement email notifications
   - Add more detailed reports
   - Create data export features

---

## Support

For any issues or questions:
1. Check the console for error messages
2. Verify all steps were followed correctly
3. Ensure Python version is 3.8+
4. Make sure virtual environment is activated

---

**Built with Flask + SQLite**  
**Student Dropout Prediction & Counselling System**  
© 2026 - All Rights Reserved
