from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User

class LoginForm(Form):

    login = StringField('Login', description='Login', validators=[DataRequired("Enter login"),\
        Length(4, 24)])
    password = PasswordField('Password', description='Password', validators=[DataRequired("Enter password"), Length(8, 24)])
    remember_me = BooleanField('Remember me', default=False)


class RegistrationForm(Form):
    email = StringField('Email', description='Email', validators=[DataRequired(), Length(1, 64), Email()])
    login = StringField('Login', description='Login', validators=[DataRequired(), Length(4,24), \
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Letters, numbers, dots or _')])
    password = PasswordField('Password', description='Password', validators=[DataRequired()])


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


    def validate_login(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use')
