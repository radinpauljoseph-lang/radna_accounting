# 📦 Project Setup, Running, and Testing Guide

---

## 🔧 Activate Virtual Environment

### Windows
```bash
.venv\Scripts\activate
```

### macOS / Linux
```bash
source .venv/bin/activate
```

---

## 🚀 Run the Django Server

### Default (localhost)
```bash
python manage.py runserver
```

### Expose to Network (LAN/WiFi)
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Run Unit Tests

### 📌 Prerequisite

Make sure your project root is included in `PYTHONPATH`:

### Windows (CMD)
```bash
set PYTHONPATH=C:\radna_accounting
```

### Windows (PowerShell)
```bash
$env:PYTHONPATH="C:\radna_accounting"
```

### macOS / Linux
```bash
export PYTHONPATH=$(pwd)
```

### 🧵 Sequential Tests (with HTML report)
```bash
pytest --html=report.html -v -o log_cli=true -o log_cli_level=INFO
```

---

### ⚡ Parallel Tests (10 workers)
```bash
pytest --html=report.html -v -o log_cli=true -o log_cli_level=INFO -n 10
```

> 💡 Requires `pytest-xdist`:
```bash
pip install pytest-xdist
```

---

## 🧹 Clean Cache Files

### Windows
```bash
for /d /r %i in (.pytest_cache, __pycache__) do @if exist "%i" rmdir /s /q "%i"
```

### macOS / Linux
```bash
find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +
```

---

## ✅ Notes

- Ensure your virtual environment is activated before running any commands.
- Always set `PYTHONPATH` correctly to avoid import errors.
- Use parallel testing (`-n`) only if your tests are independent.