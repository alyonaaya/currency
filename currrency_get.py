#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import sqlalchemy
import sys
import logging
from config import Config
from datetime import date, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from xml.etree import ElementTree as ET

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from currency_show import models


logging.basicConfig(filename="./my.log", level=logging.INFO)


def get_currency():
    try:
        currency = ET.parse(urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp"))
        for line in currency.findall('Valute'):
            id_v = line.get('ID')
            value = float(line.find('Value').text.replace(",", "."))
            num_code = int(line.find('NumCode').text)
            char_code = line.find('CharCode').text
            nominal = int(line.find('Nominal').text)
            name = line.find('Name').text

            yield id_v, value, num_code, char_code, nominal, name

    except ET.ParseError as pe:
        logging.error(pe.msg)
        sys.exit(pe.msg)
    except urllib.error.HTTPError as ue:
        logging.error(ue.msg)
        sys.exit(ue.msg)

    except ValueError as ve:
        logging.error(ve.args)
        sys.exit(-1)


if __name__ == "__main__":

    try:
        for values in get_currency():
            vid, value, num_code, char_code, nominal, name = values
            curr = models.Currencies(vid=vid, name=name)
            db_curr = models.Currencies.query.filter_by(vid=vid).all()
            if len(db_curr) == 0:
                db.session.add(curr)
            rate = models.Rates(fvid=vid, value=value/nominal)
            db.session.add(rate)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as ie:
        sys.exit(ie.args)
