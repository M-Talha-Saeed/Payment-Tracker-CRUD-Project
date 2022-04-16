from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from application import app, db
from flask import url_for, redirect
from application.models import Users, Payments
from datetime import datetime

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:letmein4321@10.68.128.3/flask-db',
            SECRET_KEY='Test_Secret_Key',
            WTF_CSRF_ENABLED = False
        )
        return app

    def setUp(self):
        db.create_all()
        user1 = Users(user_name = "talha")
        user2 = Users(user_name = "john")
        payment1 = Payments(user_id = 1, place_of_purchase = "Game", item_price = "£30", item_purchased = "fifa")
        payment2 = Payments(user_id = 2, place_of_purchase = "Next", item_price = "£30", item_purchased = "shirt")
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(payment1)
        db.session.add(payment2)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestAddPayment(TestBase):
    def test_view_payment(self):
        response = self.client.get(url_for('new_payment', uid = 1))
        self.assertEqual(response.status_code, 200)
    
    def test_payment_post(self):
        response = self.client.post(
            url_for('new_payment', uid = 1), 
            data = dict(
                place_of_purchase = "Game",
                item_price = "£30",
                item_purchased = "fifa"
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_payment_post_redirect(self):
        response = self.client.post(
            url_for('new_payment', uid = 1), 
            data = dict(
                place_of_purchase = "London",
                item_price = "£40",
                item_purchased = "Jeans"
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Payments.query.all()), 3)
        self.assertIn(b'Place of purchase', response.data)

class TestAddUser(TestBase):
    def test_view_user(self):
        response = self.client.get(url_for('new_user'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_post(self):
        response = self.client.post(
            url_for('new_user'),
            data = dict(
                user_name = "Joe"
            )
        )
        self.assertEqual(response.status_code,302)
    
    def test_user_post_redirect(self):
        response = self.client.post(
            url_for('new_user'),
            data = dict(
                user_name = "Joe"
            ),
            follow_redirects = True
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(Users.query.all()), 3)
        self.assertIn(b'Welcome to your Payment Tracker', response.data)

class TestDelete(TestBase):
    def test_user_delete(self):
        response = self.client.get(url_for('delete_user', uid = 1))
        self.assertNotIn(b'Welcome to your Payment Tracker', response.data)

    def test_payment_delete(self):
        response = self.client.get(url_for('delete_payment', pid = 1))
        self.assertNotIn(b'Place of purchase', response.data)

class TestUpdate(TestBase):
    def test_user_edit(self):
        response = self.client.post(
            url_for('update_user', uid = 1),
            data = dict(
                user_name = "Joe"
            ),
            follow_redirects = True
        )
        self.assertIn(b'Joe', response.data)
  
    def test_payment_edit(self):
        response = self.client.post(
            url_for('update_payment', pid = 1), 
            data = dict(
                place_of_purchase = "Game1",
                item_price = "Game1",
                item_purchased = "Game1"
            ),
            follow_redirects = True
        )
        self.assertNotIn(b'Game1', response.data)





    
    