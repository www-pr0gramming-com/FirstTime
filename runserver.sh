python manage.py collectstatic --no-input	
python manage.py migrate
gunicorn --worker-tmp-dir /dev/shm main.wsgi:application --bind 0.0.0.0:8080 