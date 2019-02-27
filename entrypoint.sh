# Collect static files
python manage.py collectstatic

gunicorn npl_app.wsgi 0.0.0.0:80
