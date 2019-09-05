from currency_show import db


class Rates(db.Model):
    fvid = db.Column(db.Integer, db.ForeignKey('currencies.vid'), primary_key=True)
    date = db.Column(db.Date, primary_key=True, default=db.func.current_timestamp())
    value = db.Column(db.Float)

    def __repr__(self):
        return '<Rates {}>'.format(self.fvid)


class Currencies(db.Model):
    vid = db.Column(db.String(16), unique=True, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return '<Currency {}>'.format(self.vid)
