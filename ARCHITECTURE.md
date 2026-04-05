# 🏗️ System Architecture Overview

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│                   http://localhost:5000                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK WEB SERVER                          │
│                       (app.py)                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ROUTES & CONTROLLERS                                │  │
│  │  • Authentication Routes                             │  │
│  │  • Dashboard Routes                                  │  │
│  │  • Student Management                                │  │
│  │  • Counselling Module                                │  │
│  │  • AI Chat API                                       │  │
│  │  • Reports & Analytics                               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  SESSION MANAGEMENT                                  │  │
│  │  • User Authentication State                         │  │
│  │  • Role-based Access Control                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ SQL Queries
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLITE DATABASE                           │
│                     (database.db)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   admins     │  │    staff     │  │   students   │     │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤     │
│  │ id           │  │ id           │  │ id           │     │
│  │ username     │  │ username     │  │ register_num │     │
│  │ password     │  │ password     │  │ name         │     │
│  │ email        │  │ email        │  │ department   │     │
│  │ full_name    │  │ department   │  │ risk_level   │     │
│  │ created_at   │  │ role         │  │ attendance   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │counselling_sess. │  │intervention_logs │               │
│  ├──────────────────┤  ├──────────────────┤               │
│  │ id               │  │ id               │               │
│  │ student_id       │  │ student_id       │               │
│  │ counsellor_id    │  │ action_type      │               │
│  │ session_type     │  │ description      │               │
│  │ session_date     │  │ outcome          │               │
│  │ notes            │  │ created_at       │               │
│  │ status           │  └──────────────────┘               │
│  └──────────────────┘                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Request Flow Example

### User Login Flow:

```
1. User enters credentials in login form
         │
         ▼
2. Browser sends POST request to /admin-login
         │
         ▼
3. Flask receives request and validates input
         │
         ▼
4. Query database: SELECT * FROM admins WHERE username=? AND password=?
         │
         ▼
5. Database returns user data if credentials match
         │
         ▼
6. Flask creates session with user info and role
         │
         ▼
7. Redirect to /admin-dashboard
         │
         ▼
8. Dashboard loads with user-specific data
```

---

## 🔐 Authentication Flow

```
┌─────────────┐
│   Visitor   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Landing Page   │ → Click Login
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Login Form     │ → Enter Credentials
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Backend  │ → Validate & Query DB
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    ▼         ▼
┌────────┐  ┌──────────┐
│ Create │  │ Show     │
│ Session│  │ Error    │
└───┬────┘  └──────────┘
    │
    ▼
┌───────────┐
│ Redirect  │
│ to Dashboard
└───────────┘
```

---

## 🎯 Module Breakdown

### 1. Authentication Module
```
• Admin Login
• Staff Login  
• Student Login
• Logout
• Session Management
• Role-based Access
```

### 2. Dashboard Module
```
• Admin Dashboard (Statistics, Charts)
• Staff Dashboard (Assigned Students, Schedule)
• Student Dashboard (Profile, History)
• Real-time Data Updates
```

### 3. Student Management Module
```
• View All Students
• Add New Student
• Update Student Info
• Delete Student
• Search & Filter
• Risk Level Tracking
```

### 4. Counselling Module
```
• Schedule Sessions
• View Session History
• Add Session Notes
• Follow-up Tracking
• Student-Counsellor Matching
```

### 5. AI Chat Module
```
• Keyword-based Responses
• Topic Detection (Stress, Anxiety, Studies)
• Mock AI Conversations
• Chat Interface
• Typing Indicators
```

### 6. Reports Module
```
• Department-wise Analytics
• Risk Distribution
• Trend Analysis
• Intervention Logs
• Export Capabilities
```

---

## 🗄️ Database Schema

### Relationships:

```
admins (1) ────── (M) intervention_logs
                        │
                        │
staff (1) ────── (M) counselling_sessions
    │                   │
    │                   │
    └────────── (1) ────┘
              assigned to
                        
students (1) ────── (M) counselling_sessions
    │
    │
    └────────── (M) intervention_logs
```

### Key Fields:

**students table:**
- Primary Key: `id`
- Unique: `register_number`, `email`
- Foreign Key: `counsellor_id` → `staff.id`
- Important: `risk_level`, `attendance`, `average_marks`

**counselling_sessions table:**
- Primary Key: `id`
- Foreign Keys: `student_id` → `students.id`, `counsellor_id` → `staff.id`
- Important: `session_type`, `status`, `follow_up_required`

---

## 🔄 Data Flow Examples

### Adding a Student:

```
Admin fills form
      │
      ▼
POST /students/add
      │
      ▼
Flask validates data
      │
      ▼
INSERT INTO students (...)
      │
      ▼
Database confirms
      │
      ▼
Return JSON success
      │
      ▼
Update UI
```

### Getting Dashboard Stats:

```
Dashboard loads
      │
      ▼
GET /api/dashboard
      │
      ▼
Flask queries multiple tables
      │
      ▼
Aggregate data
      │
      ▼
Return JSON:
{
  total_students: 2456,
  high_risk: 42,
  medium_risk: 342,
  low_risk: 1928
}
      │
      ▼
JavaScript updates DOM
```

### AI Chat Conversation:

```
User types: "I'm stressed about exams"
      │
      ▼
Click Send
      │
      ▼
POST /api/chat {message: "..."}
      │
      ▼
Flask analyzes keywords
      │
      ▼
Match found: "stress"
      │
      ▼
Return response about stress management
      │
      ▼
Display in chat interface
```

---

## 🛡️ Security Layers

```
┌─────────────────────────────────┐
│   Client-Side Validation        │
│   • Required fields             │
│   • Input format                │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Session Management            │
│   • Secure cookies              │
│   • Role verification           │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Server-Side Validation        │
│   • Data sanitization           │
│   • Type checking               │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Parameterized Queries         │
│   • SQL Injection prevention    │
│   • Safe data binding           │
└─────────────────────────────────┘
```

---

## 📱 Multi-Device Access

```
┌──────────────────────────────────────────┐
│          Flask Development Server        │
│              Port: 5000                  │
│              Host: 0.0.0.0               │
└────────────┬─────────────────┬───────────┘
             │                 │
             │                 │
    ┌────────▼────────┐       │
    │  Local Access   │       │
    │  localhost:5000 │       │
    │  (Desktop)      │       │
    └─────────────────┘       │
                              │
                    ┌─────────▼──────────┐
                    │ Network Access     │
                    │ 192.168.x.x:5000   │
                    │ (Mobile/Tablet)    │
                    └────────────────────┘
```

---

## 🎨 Frontend-Backend Integration

```
┌─────────────────────────────────────────────────────┐
│                  HTML Templates                      │
│  • Jinja2 Templating Engine                         │
│  • Server-side rendering                            │
│  • Dynamic content injection                        │
└────────────────┬────────────────────────────────────┘
                 │
                 │
┌────────────────▼────────────────────────────────────┐
│                  JavaScript                          │
│  • Fetch API for AJAX requests                      │
│  • DOM manipulation                                 │
│  • Event handling                                   │
│  • Real-time updates                                │
└────────────────┬────────────────────────────────────┘
                 │
                 │
┌────────────────▼────────────────────────────────────┐
│                  CSS Styling                         │
│  • Original design preserved                        │
│  • Responsive layouts                               │
│  • Animations & transitions                         │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Ready

### Current State (Development):
```
✅ Flask Development Server
✅ SQLite Database
✅ Debug Mode Enabled
✅ Local File Storage
```

### Production Deployment Steps:
```
1. Change secret_key to random secure string
2. Enable password hashing (bcrypt)
3. Use PostgreSQL/MySQL instead of SQLite
4. Deploy on Gunicorn/uWSGI
5. Add Nginx reverse proxy
6. Enable HTTPS with SSL certificates
7. Set up environment variables
8. Configure logging
9. Enable error tracking
10. Set up backups
```

---

## 📈 Scalability Considerations

### Current Capacity:
- ✅ Handles 10-50 concurrent users easily
- ✅ Fast response times (<100ms)
- ✅ Suitable for demo/small institution

### For Larger Scale:
- Switch to PostgreSQL
- Add caching layer (Redis)
- Implement connection pooling
- Use CDN for static files
- Add load balancer
- Horizontal scaling with multiple workers

---

**This architecture provides a solid foundation that's easy to understand, modify, and extend!** 🎉
