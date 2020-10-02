release: python manage.py migrate --noinput
web: gunicorn SICAP.wsgi:application --log-file -