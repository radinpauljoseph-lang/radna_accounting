# Project Setup, Running, and Testing Guide

## 🔧 Activate Virtual Environment

```bash
venv\Scripts\activate
```

## 🚀 Run the Django Server

Choose any of the commands below:

```bash
python manage.py runserver
```

Or specify the project directory:

```bash
python ./radna_accounting/manage.py runserver
```

Run on all network interfaces (useful for LAN/WiFi access):

```bash
python ./radna_accounting/manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Run Unit Tests

### Standard Test Execution

```bash
pytest -v -o log_cli=true -o log_cli_level=INFO radna_accounting radna_accounting/test/unit
```

### Sequential Tests (with HTML report)

```bash
pytest --html=report.html -v -o log_cli=true -o log_cli_level=INFO unit
```

### Parallel Tests (10 workers)

```bash
pytest --html=report.html -v -o log_cli=true -o log_cli_level=INFO -n 10 radna_accounting/radna_accounting/test/unit
```

---

## 🧹 Clean Cache Files

Delete all `__pycache__` and `.pytest_cache` folders on Windows:

```bash
for /d /r %i in (.pytest_cache, __pycache__, assets) do @if exist "%i" rmdir /s /q "%i"
```
