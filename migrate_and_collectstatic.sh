#!/usr/bin/env bash

/usr/local/bin/python manage.py migrate

/usr/local/bin/python manage.py collectstatic --noinput

/usr/bin/memcached -u root -d -m 64 -c 1024 -l 127.0.0.1,::1 -o modern,drop_privileges

echo "Exited $0"