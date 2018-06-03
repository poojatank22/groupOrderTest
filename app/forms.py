from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, number_range, Email


class GroupOrderForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    n_friends = IntegerField('Number of Friends', validators=[DataRequired(), number_range(min=1)])
    placeOrder = SubmitField('Group Order')
    checkOrder = SubmitField('Check My Orders')


class OrderForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    orderName = StringField('Your Order', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired(), number_range(min=1)], default=1)
    size = RadioField('Size', choices=[('R', 'Regular'), ('L', 'Large')], default='R')
    submit = SubmitField('Place Order')


class Emails(FlaskForm):
    email = StringField('Enter Email', validators=[Email(), DataRequired()])


class ShareLinkForm(FlaskForm):
    users_email = StringField('Your Email', validators=[DataRequired(), Email()])
    recipients_emails = FieldList(FormField(Emails), min_entries=1)
    send_mail = SubmitField('Share Link')

