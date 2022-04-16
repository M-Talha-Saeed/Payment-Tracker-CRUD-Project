from application import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(30), nullable = False, unique = True)
    payments = db.relationship('Payments', backref= 'paymentsbr')

class Payments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    place_of_purchase = db.Column(db.String(30), nullable=False)
    item_price = db.Column(db.String(30), nullable=False)
    item_purchased = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
