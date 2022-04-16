from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    user_name = StringField(
        'User Name',
        validators = [DataRequired(), Length(max = 100)]
    )
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    place_of_purchase = StringField(
        'Place of purchase',
        validators = [DataRequired(), Length(max = 100)]
    )
    item_price = StringField(
        'Item Price',
        validators = [DataRequired(), Length(max = 100)]
    )
    item_purchased = StringField(
        'Item Purchased',
        validators = [DataRequired(), Length(max = 100)]
    )
    submit = SubmitField('Submit')
