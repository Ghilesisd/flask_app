from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField, fields
from wtforms.fields.simple import PasswordField

from wtforms.validators import DataRequired,Email,length,EqualTo,ValidationError

#from app import User

def email_existe():
   # email=User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('email already exists')

class RegistrationForm(FlaskForm):
    nom=StringField('nom', validators=[DataRequired(),length(3,15,message='between 3 to 15 characters')])
   
    email=StringField('email', validators=[DataRequired(),Email(), email_existe])
   
    password=PasswordField('password',validators=[DataRequired(),length(5),EqualTo('confirm', message='password must match')])

    confirm=PasswordField('confirm',validators=[DataRequired()])

    submit= SubmitField('register')



    



