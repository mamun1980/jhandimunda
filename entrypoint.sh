#!/bin/bash

python manage.py migrate --no-input
python manage.py collectstatic --noinput
# python manage.py createsuperuser_if_none_exists --user=admin --password=Admin123
# echo "Admin username: admin and password: Admin123"


gunicorn core.wsgi --user www-data --bind 0.0.0.0:8010 &
nginx -g "daemon off;"