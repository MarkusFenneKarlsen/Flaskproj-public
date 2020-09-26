from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from app.models import User
import phonenumbers as pn

class RegistrationForm(FlaskForm):
    username = StringField('Brukernavn', validators=[Required(), Length(min=5, max=20)])
    email = StringField('Email', validators= [Required(), Email()])
    password = PasswordField('Passord', validators=[Required(), Length(min=8)])
    confirm_password = PasswordField('Bekreft Passord', validators=[Required(), EqualTo('password')])
    tlf = StringField('Telefonnummer', validators=[Required()])
    addr = StringField('Addresse', validators=[Required(), Length(min=5)])
    submit = SubmitField('Registrer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dette brukernavnet er allerede i bruk, vennligst bruk et annet brukernavn')

    def validate_email(self, email):
        user = User.query.filter_by(useremail=email.data).first()
        if user:
            raise ValidationError('Denne epost addressen er allerede i bruk, vennligst bruk en annen epost')

    def validate_tlf(self, tlf):
        user = User.query.filter_by(usertlf=tlf.data).first()
        if user:
            raise ValidationError('Dette telefonnummeret er allerede i bruk, vennligst bruk et annet telefonnummer')
        if len(str(tlf.data)) >= 9 or len(str(tlf.data)) <= 7:
         raise ValidationError('telefonnummeret må ha 8 siffer')
        number = pn.parse(tlf.data, "NO")
        if not pn.is_possible_number(number):
            raise ValidationError('telefonnummeret må ha 8 siffer, og være et mulig telefonnummer')

class LoginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[Required(), Length(min=5, max=20)])
    password = PasswordField('Passord', validators=[Required(), Length(min=8)])
    submit = SubmitField('Logg inn')
