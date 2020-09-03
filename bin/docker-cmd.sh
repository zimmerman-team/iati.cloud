#!/bin/bash
set -e

# run migrations
/app/src/OIPA/manage.py migrate --noinput

# generate static files
/app/src/OIPA/manage.py collectstatic --noinput

# create superuser
/app/src/OIPA/manage.py shell -c \
"from django.contrib.auth.models import User; \
User.objects.create_superuser('oipa', 'oipa', 'oipa') \
if not User.objects.filter(username='oipa').exists() \
else 'Superuser already exists . . .'"

# run Django as a wsgi process
/app/src/bin/wait-for-postgres.sh -- /venv/bin/uwsgi \
    --chdir=/app/src/OIPA \
    --module=OIPA.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=OIPA.settings \
    --master \
    --pidfile=/tmp/uwsgi.pid \
    --thunder-lock \
    --http 0.0.0.0:8000 \
    --buffer-size 32768 \
    --processes=3 \
    --uid=1000 \
    --gid=1000 \
    --vacuum \
    --harakiri=120 \
    --home=/venv
