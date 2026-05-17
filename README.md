# 💰 SmartSpend – AI Based Personal Expense Tracker

## 🌐 Live Demo
👉 [SmartSpend Live](https://smartspend-i49p.onrender.com/login/)

A full-stack personal expense tracking web application built with Django (Python). Developed as a BCA 6th Semester college project.

---

## 🚀 Features

- 🔐 User Registration with Admin Approval System
- 🔑 Login / Logout with Password Show/Hide
- ➕ Add, Edit, Delete Expenses
- 📊 Dashboard with Chart.js Bar Chart (category-wise)
- 💰 Monthly Budget Setting & Tracking
- 🔔 3-Level Budget Alert System (80% / 90% / 100%)
- 🤖 AI Smart Insight on Dashboard (rule-based analysis)
- 📋 AI Spending Summary Page (category breakdown + tips)
- ⚙️ Admin Manage Panel (approve/decline users, monitor expenses)
- 📱 Fully Mobile Responsive

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Charts | Chart.js |
| Server | Gunicorn |
| Static Files | Whitenoise |
| Hosting | Render.com |
| Version Control | Git + GitHub |

---

## ⚙️ How to Run Locally

1. Clone the repo

git clone https://github.com/bhavyanandwana6-design/SmartSpend.git

3. Install dependencies

pip install -r requirements.txt

5. Run migrations

python manage.py migrate

7. Start server

python manage.py runserver

9. Open: `http://127.0.0.1:8000`

---

## 📁 Project Structure

SmartSpend/
├── expenses/
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── add_expense.html
│   │   ├── edit_expense.html
│   │   ├── ai_summary.html
│   │   └── manage_panel.html
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── smartspend/
│   └── settings.py
├── requirements.txt
├── Procfile
└── manage.py

---

## 👨‍💻 Developer

**Bhavya Nandwana** | BCA 6th Semester | NIBM
