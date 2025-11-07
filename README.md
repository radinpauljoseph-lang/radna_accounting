run virtual env: 
    venv\Scripts\activate
python manage.py runserver or
python ./radna_accounting/manage.py runserver
python ./radna_accounting/manage.py runserver 0.0.0.0:8000


run unit test:
(venv) C:\radna_accounting\radna_accounting>pytest -v -o log_cli=true -o log_cli_level=INFO radna_accounting radna_accounting/test/unit

sequential test:
    pytest --html=report.html -v -o log_cli=true -o log_cli_level=INFO unit
parallel test:
    pytest --html=report.html -v -o log_cli=true -o log_cli_level=INFO -n 10 unit

delete pycache folders:
    for /d /r %i in (.pytest_cache, __pycache__) do @if exist "%i" rmdir /s /q "%i"
    