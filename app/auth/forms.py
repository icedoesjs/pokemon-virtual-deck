from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, URLField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    poke_name = StringField('PokemonName', validators=[DataRequired()])
    submit_btn = SubmitField()
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()
    
class CreateUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirmPassword', validators=[DataRequired()])
    first_name = StringField('firstName', validators=[DataRequired()])
    last_name = StringField('lastName', validators=[DataRequired()])
    avatar = URLField('Avatar', validators=None)
    submit = SubmitField()
    
class UserEditForm(FlaskForm):
    username = StringField('Username', validators=None)
    first_name = StringField('firstName', validators=None)
    last_name = StringField('lastName', validators=None)
    email = EmailField('Email', validators=None)
    password = PasswordField('password', validators=None)
    confirm_password = PasswordField('confirmPassword', validators=None)
    avatar = URLField('Avatar', validators=None)
    submit = SubmitField()