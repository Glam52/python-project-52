run:
	poetry run python manage.py runserver
PORT = 8000
start:
	poetry run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)