from __future__ import absolute_import, unicode_literals

from celery import task
import os

from django.conf import settings

@task
def create_backups():
    postgres_dump_path = settings.BASE_DIR + '/static/postgres.export.iati.cloud'

    if os.path.isfile(postgres_dump_path):
        os.remove(postgres_dump_path)

    dump_command = 'PGPASSWORD="{db_user_pass}" pg_dump -h {host} -U {db_user} oipa > {db_tar_output}'
    dump_command = dump_command.format(db_user_pass=os.getenv('OIPA_DB_PASSWORD'),
                                       host=settings.DATABASES['default']['HOST'],
                                       db_user=os.getenv('OIPA_DB_USER'), db_tar_output=postgres_dump_path)

    os.system(dump_command)
