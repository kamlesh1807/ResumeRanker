#!/bin/bash

echo "Starting Celery Worker..."
cd /opt/website

celery -A website worker -l INFO  > /var/log/celeryWorker.log 2>&1 &

if [ $? -eq 0 ]; then
   echo "Celery Worker..."
else
   echo "Celery Worker Failed To Start..."
   exit 0
fi

echo "Starting Application.."
python manage.py migrate
python manage.py makemigrations jobs
python manage.py makemigrations profiles
python manage.py migrate
python manage.py runserver 0.0.0.0:${PORT}
