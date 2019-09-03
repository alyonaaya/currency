FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY currency_show currency_show
COPY migrations migrations
COPY currency_show.py currency_get.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP currency_show.py

EXPOSE 5000
ENTRYPOINT ["sh","./boot.sh"]
