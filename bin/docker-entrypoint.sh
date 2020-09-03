#!/bin/bash
# wait-for-postgres.sh

################################################################################
# An entrypoint script for OIPA which waits for the database to start, then    #
# runs migrations and then executes given startup command for a Docker service #
################################################################################

set -e

cmd="$@"

until PGPASSWORD=${OIPA_DB_PASSWORD} psql -h "${OIPA_DB_HOST}" -U "${OIPA_DB_USER}" ${OIPA_DB_NAME} -c '\l' > /dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Caution sleeping for 5 secs . . ."
sleep 5

#Create superuser:
>&2 echo "Creating superuser . . ."

python /app/src/OIPA/manage.py shell -c \
"from django.contrib.auth.models import User; \
User.objects.create_superuser('oipa', 'oipa', 'oipa') \
if not User.objects.filter(username='oipa').exists() \
else 'Superuser already exists . . .'"

# Start dev server:
>&2 echo "\n\n\n*** Database is up - executing Docker container entrypoint (startup) command ***\n\n\n"
exec $cmd