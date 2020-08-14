#!/usr/bin/env bash

cd /s106_da/ || exit 1
python manage.py migrate
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8089 --access-log /var/log/s106_da/daphne_access.log project.asgi:application
