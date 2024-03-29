#!/bin/sh
source venv/bin/activate

mkdir dbdata
flask db upgrade

venv/bin/python currency_get.py
echo '0 12 * * * /app/venv/bin/python /app/currency_get.py' >> /etc/crontabs/root
crond -b

exec gunicorn -b :5000 --access-logfile - --error-logfile - currency_show:app