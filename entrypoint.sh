# Collect static files
python manage.py collectstatic --no-input

gunicorn npl_app.wsgi -b 0.0.0.0:80
