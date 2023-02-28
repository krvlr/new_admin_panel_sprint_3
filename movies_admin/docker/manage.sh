#!/bin/bash
CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]
then
    touch /$CONTAINER_FIRST_STARTUP
    echo "First time container starting commands"
    python3 manage.py migrate --fake movies 0001_initial
    python3 manage.py migrate
    python3 manage.py createsuperuser --username admin --no-input
    python3 manage.py collectstatic --no-input --clear
    python3 sqlite_to_postgres/load_data.py
    python3 sqlite_to_postgres/test_load_data.py
else
    echo "Containter restarting commands"
    echo "No commands"
fi
uwsgi --strict --ini uwsgi/uwsgi.ini