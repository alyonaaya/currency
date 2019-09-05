#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import logging
from config import Config
from datetime import date, timedelta
from flask import Flask
from flask_migrate import Migrate
from xml.etree import ElementTree as ET

app = Flask(__name__)
app.config.from_object(Config)
from currency_show import models, db
migrate = Migrate(app, db)


logging.basicConfig(filename="./currency_get.log", level=logging.INFO)


def get_currency():
    try:
        currency = ET.parse(urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp"))
        for line in currency.findall('Valute'):
            vid = line.get('ID')
            value = float(line.find('Value').text.replace(",", "."))
            num_code = int(line.find('NumCode').text)
            char_code = line.find('CharCode').text
            nominal = int(line.find('Nominal').text)
            name = line.find('Name').text

            yield vid, value, num_code, char_code, nominal, name

    except ET.ParseError as pe:
        logging.error(pe.msg)
    except urllib.error.HTTPError as ue:
        logging.error(ue.msg)
    except ValueError as ve:
        logging.error(ve.args)


def save_currency():
    for values in get_currency():
        vid, value, num_code, char_code, nominal, name = values
        curr = models.Currencies(vid=vid, name=name)
        db_curr = models.Currencies.query.filter_by(vid=vid).all()
        db_rate = models.Rates.query.filter_by(fvid=vid).filter_by(date=date.today()).all()
        if len(db_curr) == 0:
            db.session.add(curr)
        if len(db_rate) == 0:
            rate = models.Rates(fvid=vid, value=value)
            db.session.add(rate)
        else:
            db_rate[0].value = value
            db.session.add(db_rate[0])
    db.session.commit()


def delete_old_data(days=7):
    days_ago = date.today() - timedelta(days=days)
    rates = models.Rates.query.filter(models.Rates.date < days_ago).all()
    rates_count = len(rates)
    for rate in rates:
        db.session.delete(rate)
    db.session.commit()
    logging.info("Delete {} entries\n".format(rates_count))


if __name__ == "__main__":
    save_currency()
    delete_old_data()
