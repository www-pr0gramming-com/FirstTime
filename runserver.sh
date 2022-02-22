python manage.py collectstatic --no-input	
python manage.py migrate
gunicorn main:application --bind 0.0.0.0:8080 --worker-tmp-dir /dev/shm