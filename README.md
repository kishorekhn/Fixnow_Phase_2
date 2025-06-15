# Django Project Setup Guide

> **Python Version:** 3.13.2  
> **pip Version:** 25.0.1

---

## ✅ Steps to Run Django Server

### 1. Create Python Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

---

### 3. Setup Database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

---

### 4. Run the Django Server

```bash
python3 manage.py runserver
```

> You can also specify a port:  
> Example: `python3 manage.py runserver 8001`

---

## 🔁 Before Pushing the Code

If you install or update any packages, update the `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

---

## 📝 Notes

- Make sure your virtual environment is activated before running any commands.
- Always apply migrations after pulling latest code.
- Keep `requirements.txt` updated for smooth team collaboration.
