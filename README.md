# 🚀 FRO Reminder System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Project-Active-success)

---

## 📌 Overview

The **FRO Reminder System** is a modern web application built to manage student records and track critical document expiry dates (FRO, Passport, Visa). It helps institutions and individuals stay compliant by sending **automated reminders before deadlines**.

---

## ✨ Key Highlights

✔ Smart expiry tracking
✔ Automated email reminders
✔ Clean dashboard with real-time stats
✔ Scalable and modular architecture
✔ Easy to extend (SMS / WhatsApp ready)

---

## 🎯 Features

### 👨‍🎓 Student Management

* Add, edit, and delete students
* Maintain structured student records

### 📄 Document Management

* Support for multiple document types:

  * FRO
  * Passport
  * Visa
* Store issue & expiry dates
* Upload and manage files

### ⏳ Expiry Tracking System

* Automatic days calculation
* Status classification:

  * 🟢 Active
  * 🟡 Expiring Soon
  * 🔴 Expired

### 📧 Notification System

* Email alerts before expiry
* Configurable intervals:

```python
reminder_days = [30, 15, 10]
```

### ⚙️ Automation

* Daily background checks
* Auto-triggered reminders

### 🔍 Smart Search

* Search by:

  * Name
  * Roll Number
  * Course
  * Country

### 📊 Dashboard

* Total Students
* Expiring Documents
* Expired Documents

### 🧩 Extras

* Manual "Send Reminder" button
* Export data to CSV
* Clean UI with status indicators

---

## 🛠️ Tech Stack

| Layer    | Technology            |
| -------- | --------------------- |
| Backend  | Python, Flask         |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite                |
| Tools    | VS Code, Browser      |

---

## 🏗️ Architecture

```
Client (Browser)
       ↓
Frontend (HTML/CSS/JS)
       ↓
Backend (Flask App)
       ↓
Database (SQLite)
```

---

## 🔄 Development Model

This project follows the **Incremental Development Model** — building the system step-by-step.

### 📦 Development Phases

1. Student Management
2. Document Management
3. Expiry Tracking
4. Email Notifications
5. Automation
6. Search & Dashboard
7. Final Enhancements

---

## 🧠 Smart Design Decisions

* ✅ Unified **Document Table** (no redundancy)
* ✅ Centralized reminder logic (flexible config)
* ✅ File storage via paths (efficient & scalable)
* ✅ Extensible notification system

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/fro-reminder-system.git
cd fro-reminder-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate

# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```
/project-root
│── app.py
│── requirements.txt
│
├── /templates      # HTML files
├── /static         # CSS, JS, images
├── /uploads        # Uploaded documents
└── /database       # SQLite DB
```

---

## 🧪 Testing

* ✔ Unit Testing
* ✔ Integration Testing
* ✔ System Testing

---

## 🚀 Deployment Options

* Local Hosting
* Cloud Platforms:

  * Render
  * PythonAnywhere
  * Railway

---

## 🔮 Future Improvements

* 📱 SMS & WhatsApp notifications
* 🔐 Role-based login system
* ☁️ Cloud database (PostgreSQL/MySQL)
* 📊 Advanced analytics dashboard

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

## 💡 Final Note

This system is designed to be **simple, scalable, and production-ready**, making it ideal for student management and compliance tracking systems.

---

⭐ *If you found this useful, consider giving the repo a star!*

