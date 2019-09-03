#!/bin/sh
source venv/bin/activate
flask db upgrade

venv/bin/python currency_get.py

exec gunicorn -b :5000 --access-logfile - --error-logfile - currency_show:app