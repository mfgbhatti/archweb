#!/usr/bin/env bash

./manage.py migrate

./manage.py collectstatic --noinput

exit 0