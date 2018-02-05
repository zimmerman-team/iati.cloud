#!/bin/bash
set -e

# run migrations
/app/src/OIPA/manage.py migrate --noinput

# generate static files
/app/src/OIPA/manage.py collectstatic --noinput

# export (docker) env vars to '/tmp/environment' file for uwsgi (ini) to read
/usr/bin/env > /tmp/environment

# run Django as a wsgi process
/app/src/bin/wait-for-postgres.sh -- /venv/bin/uwsgi --ini /app/src/etc/uwsgi/uwsgi-production.ini
