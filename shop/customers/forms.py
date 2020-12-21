from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Customer


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField(
        'Email: ', [validators.DataRequired(), validators.Email()])
    password = PasswordField(
        'Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match!')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    state = StringField('state: ', [validators.DataRequired()])
    city = StringField('city: ', [validators.DataRequired()])
    contact = StringField('contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zipcode: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(
        ['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Customer.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")

    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class CustomerLoginForm(FlaskForm):
    email = StringField(
        'Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
