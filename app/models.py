from datetime import datetime
from app import db

class Grouporder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Orders', backref=db.backref('order', uselist=True, lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupId = db.Column(db.Integer, db.ForeignKey('grouporder.id'), nullable=False)
    username = db.Column(db.String(64))
    orderName = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    size = db.Column(db.String(20))

    def __repr__(self):
        return '<User {}>'.format(self.username)

