# QUICK START GUIDE - Student Dropout Prediction & Counselling System

## 🚀 Easiest Way to Run (Windows)

### Option 1: Double-click start.bat
1. **Double-click** the `start.bat` file
2. Wait for setup to complete
3. Open browser and go to **http://localhost:5000**
4. Done! ✅

### Option 2: Manual Commands
Open Command Prompt in the project folder and run:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

---

## 🔑 Default Login Credentials

| Role     | Username / Register No | Password    |
|----------|------------------------|-------------|
| Admin    | admin                  | admin123    |
| Staff    | staff                  | staff123    |
| Student  | REG-2023-001           | student123  |

---

## 📱 Access on Mobile

1. Find your IP address:
   - Windows: Run `ipconfig` in terminal
   - Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On mobile browser, enter:
   ```
   http://YOUR_IP:5000
   ```
   Example: http://192.168.1.100:5000

**Note:** Both laptop and mobile must be on same Wi-Fi.

---

## 🎯 What to Do Next

### As Admin:
1. Login with admin credentials
2. View dashboard statistics
3. Manage students (add/edit/delete)
4. View all students with filters
5. Check counselling sessions
6. Generate reports

### As Staff:
1. Login with staff credentials  
2. View assigned students
3. Schedule counselling sessions
4. Add session notes

### As Student:
1. Login with student credentials
2. View your profile
3. Check counselling history
4. Use AI Chat for support

---

## ⚙️ Common Issues

**Problem:** Port 5000 already in use  
**Solution:** 
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Problem:** Module not found  
**Solution:** Make sure virtual environment is activated
```powershell
.\venv\Scripts\activate
```

**Problem:** Database errors  
**Solution:** Delete database.db and run init_db.py again
```powershell
del database.db
python init_db.py
```

---

## 🛑 To Stop the Server

Press **Ctrl+C** in the terminal window running the Flask app.

---

## 📁 Project Structure

```
project-root/
├── app.py              # Main Flask application
├── init_db.py          # Database setup
├── requirements.txt    # Dependencies
├── start.bat          # Quick start script
├── README-SETUP.md    # Detailed instructions
├── templates/         # HTML files
└── static/           # CSS, JS, images
```

---

## 🔒 Security Note

This is a **development/demo version**. For production:
- Change the secret key in app.py
- Use password hashing
- Enable HTTPS
- Add CSRF protection

---

**Need Help?** Check the detailed README-SETUP.md file.

**Happy Coding!** 🎉
