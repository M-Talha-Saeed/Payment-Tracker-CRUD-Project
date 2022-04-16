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
        return redirect(url_for('user_payments',uid=uid))

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

@app.route('/user_payments/<int:uid>')
def user_payments(uid):
    all_payments = Payments.query.filter_by(user_id=uid).all()
    return render_template('user_payments.html', all_payments = all_payments)

@app.route('/update_user/<int:uid>', methods = ['GET', 'POST'])
def update_user(uid):
    user = Users.query.get(uid)
    form = UserForm()

    if request.method == "POST":
        user.user_name = form.user_name.data
        db.session.commit()
        return redirect(url_for('index'))

    form.user_name.data = user.user_name

    return render_template('new_user.html', form = form)

@app.route('/update_payment/<int:pid>', methods = ['GET', 'POST'])
def update_payment(pid):
    payment = Payments.query.get(pid)
    form = PaymentForm()

    if request.method == "POST":
        payment.place_of_purchase = form.place_of_purchase.data
        payment.item_price = form.item_price.data
        payment.item_purchased = form.item_purchased.data
        db.session.commit()
        return redirect(url_for('index'))

    form.place_of_purchase.data = payment.place_of_purchase
    form.item_price.data = payment.item_price
    form.item_purchased.data = payment.item_purchased

    return render_template('new_payment.html', form = form)

@app.route('/delete_user/<int:uid>')
def delete_user(uid):
    user = Users.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_payment/<int:pid>')
def delete_payment(pid):
    payment = Payments.query.get(pid)
    db.session.delete(payment)
    db.session.commit()
    return redirect(url_for('index'))