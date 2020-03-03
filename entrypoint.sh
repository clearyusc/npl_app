# Collect static files
python /code/manage.py collectstatic --no-input

gunicorn --workers=2 npl_app.wsgi -b 0.0.0.0:8000
