#!/usr/bin/env python3

from currency_show import app, db, models
from datetime import date, timedelta
from flask import render_template, url_for
from flask import request
import json


# Page names

WEEK = "week"
DAY = "day"

@app.route("/")
def index():
    name_id = []
    try:
        currencies = models.Currencies.query.all()
        for cur in currencies:
            name_id.append((cur.name, url_for(WEEK, id=cur.vid)))
        return render_template("index.html", name_id=name_id)
    except IOError:
        pass


@app.route("/{}".format(WEEK), methods=['GET'])
def week():
    vid = request.args.get("id")
    weak_ago = date.today() - timedelta(days=7)
    rates = models.Rates.query.filter_by(fvid=vid).filter(models.Rates.date >= weak_ago).all()
    date_val = []
    name = models.Currencies.query.filter_by(vid=vid).all()[0].name
    for rate in rates:
        date_val.append((rate.date, rate.value))
    return render_template("{}.html".format(WEEK), vid=vid, data=name, date_value=date_val)


@app.route("/{}".format(DAY))
def day():
    jobj = []
    for curr, rate in db.session.query(models.Currencies, models.Rates).filter(models.Currencies.vid ==
                                    models.Rates.fvid).filter(models.Rates.date == date.today()):
        jobj.append((curr.name, rate.value))

    return json.dumps(jobj)



