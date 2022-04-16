from application import app, db
from application.forms import PaymentForm, UserForm
from application.models import Payments, Users
from flask import render_template, request, redirect, url_for

@app.route('/')
def index():
    all_users = Users.query.all()
    return render_template('index.html', all_users = all_users)

@app.route('/new_payment/<int:uid>', methods=['GET', 'POST'])
def new_payment(uid):
    form = PaymentForm()

    if request.method == 'POST':
        payment = Payments(
            user_id = uid,
            place_of_purchase = form.place_of_purchase.data,
            item_price = form.item_price.data,
            item_purchased = form.item_purchased.data
        )
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('index',uid=uid))

    return render_template('new_payment.html', form = form)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = UserForm()

    if request.method == 'POST':
        user = Users(
            user_name = form.user_name.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('new_user.html', form = form)