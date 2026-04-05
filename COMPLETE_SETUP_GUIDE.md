# 🎯 COMPLETE SETUP GUIDE - Visual Step-by-Step

## Welcome! 👋

This guide will help you set up and run the **Student Dropout Prediction & Counselling System** with Flask backend.

---

## 📋 What You Need (5 minutes)

### Requirements:
- ✅ Windows/Mac/Linux computer
- ✅ Python 3.8 or higher
- ✅ Web browser (Chrome, Firefox, Edge)
- ✅ (Optional) Mobile phone for testing on same Wi-Fi

---

## 🚀 STEP 1: Install Python (if needed)

### Windows Users:
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.x.x"
3. **IMPORTANT:** ✅ Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for installation to complete

### Verify Installation:
Open Command Prompt and type:
```
python --version
```
You should see something like: `Python 3.11.5`

---

## 📁 STEP 2: Project is Already Set Up!

All files have been created in:
```
d:\qoder project\
```

### Files Created:
```
✅ app.py                  - Main Flask application
✅ init_db.py              - Database setup script  
✅ requirements.txt        - Dependencies list
✅ start.bat               - Quick start (Windows)
✅ templates/              - All your HTML files
✅ static/                 - CSS, JS, images folders
✅ Documentation files     - Multiple guides
```

---

## ⚡ STEP 3: Quick Start (Easiest Method)

### For Windows Users:

1. **Double-click** this file: `start.bat`
   ```
   📁 d:\qoder project\start.bat
   ```

2. The script will automatically:
   - Create virtual environment
   - Install required packages
   - Initialize database
   - Show you the access URLs

3. Wait until you see:
   ```
   ============================================================
   Starting Flask Application...
   ============================================================
   
   Access the application at:
     Local:  http://localhost:5000
     Network: http://192.168.x.x:5000
   
   Default Login Credentials:
     Admin:   username = admin,    password = admin123
     Staff:   username = staff,    password = staff123
     Student: username = REG-2023-001, password = student123
   ```

4. **Keep this window open!** The server is now running.

---

## 🌐 STEP 4: Open the Application

### On Desktop:
1. Open your web browser
2. Type in address bar: **http://localhost:5000**
3. Press Enter
4. You should see the landing page! ✅

### On Mobile (Same Wi-Fi):
1. Find your laptop's IP address:
   - Windows: Open Command Prompt
   - Type: `ipconfig`
   - Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On mobile browser, type:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

3. App loads on mobile too! 📱

---

## 🔐 STEP 5: Login and Explore

### Try These Logins:

#### Admin Access:
1. Click "Admin Login"
2. Username: `admin`
3. Password: `admin123`
4. Click "Sign In"
5. Explore admin dashboard with statistics!

#### Staff Access:
1. Click "Staff Login"
2. Username: `staff`
3. Password: `staff123`
4. See assigned students and sessions

#### Student Access:
1. Click "Student Login"
2. Register Number: `REG-2023-001`
3. Password: `student123`
4. View profile and try AI chat!

---

## 🎮 STEP 6: What Can You Do?

### As Admin:
- ✅ View total students: 2,456 (sample data)
- ✅ See risk distribution charts
- ✅ Department-wise analytics
- ✅ Add/Edit/Delete students
- ✅ View all counselling sessions
- ✅ Generate reports

### As Staff:
- ✅ View assigned students
- ✅ Schedule counselling sessions
- ✅ Add session notes
- ✅ Track follow-ups

### As Student:
- ✅ View personal information
- ✅ Check counselling history
- ✅ Use AI Chat for support
- ✅ Talk about stress, anxiety, studies

---

## 🛑 How to Stop

When you're done:
1. Go to the terminal/command prompt where Flask is running
2. Press: **Ctrl + C**
3. Server stops ✅

---

## 🔄 Next Time You Want to Run

### Super Easy Method:
Just double-click: `start.bat`

It remembers everything and starts quickly!

---

## 📊 Sample Data Included

The system comes pre-loaded with:

### Students:
- 10 sample students (REG-2023-001 to REG-2023-010)
- Different departments
- Various risk levels (High, Medium, Low)
- Realistic attendance and marks

### Staff:
- 3 staff members
- Different roles (Counsellor, Faculty, Senior Counsellor)

### Counselling Sessions:
- 6 scheduled/completed sessions
- Various types (Academic, Career, Personal)
- Session notes included

---

## 🎨 Your Frontend is Safe!

### What Stayed the Same:
- ✅ All designs unchanged
- ✅ Colors preserved
- ✅ Layout identical
- ✅ Animations working
- ✅ Responsive design intact

### What Changed (Minimal):
- Added backend connections
- Login forms now work
- Navigation links updated
- AI chat functional

**Your beautiful frontend looks exactly the same!** ✨

---

## ⚠️ Troubleshooting

### Problem: "Python not found"
**Solution:** Install Python from python.org and add to PATH

### Problem: "Port 5000 already in use"
**Solution:** 
```
netstat -ano | findstr :5000
taskkill /PID <NUMBER> /F
```

### Problem: "Module not found"
**Solution:**
```
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: "Can't access from mobile"
**Solution:**
- Check both devices on same Wi-Fi
- Verify IP address is correct
- Check firewall settings

---

## 📚 Documentation Files

Three helpful guides included:

1. **QUICKSTART.md** - Quick reference (1 page)
2. **README-SETUP.md** - Detailed instructions (3 pages)
3. **BACKEND_SUMMARY.md** - Complete technical details (4 pages)

---

## 🎯 Success Checklist

Before moving forward, ensure:

- [ ] Python installed and working
- [ ] Virtual environment created (venv folder exists)
- [ ] Dependencies installed (no errors)
- [ ] Database initialized (database.db created)
- [ ] Flask server running (no errors in terminal)
- [ ] Can access http://localhost:5000
- [ ] Can login as admin
- [ ] Can see dashboard

If all checked ✅, you're all set! 🎉

---

## 💡 Pro Tips

1. **Keep terminal open** while using the app
2. **Bookmark** localhost:5000 in browser
3. **Save credentials** somewhere safe
4. **Try different logins** to see all features
5. **Test AI chat** - it responds to keywords!
6. **Check mobile view** - works great!

---

## 🚀 Ready to Explore?

You now have a fully working Flask + SQLite application with:
- ✅ User authentication
- ✅ Dashboard with statistics
- ✅ Student management
- ✅ Counselling system
- ✅ AI chat feature
- ✅ Reports and analytics
- ✅ Mobile accessibility

**Enjoy your upgraded system!** 🎊

---

## 📞 Need More Help?

1. Check the detailed README-SETUP.md
2. Review BACKEND_SUMMARY.md for technical details
3. Look at console output for error messages
4. Verify all steps were followed

---

**Made with ❤️ for easy learning!**

© 2026 Student Dropout Prediction & Counselling System
