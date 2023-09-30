from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp, NumberRange
from website.models import *
from flask_wtf.recaptcha import RecaptchaField

class RegisterForm(FlaskForm):
    #username validation

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    #email address validation
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
        
    
    def validate_phone_number(self, phone_number_to_check):
        phone_number = User.query.filter_by(phone_number=phone_number_to_check.data).first()
        if phone_number:
            raise ValidationError('Phone number already exists! Please try a different phone number')
    

    #checks if the user has met all the conditions with their credentials in creating their account
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    phone_number = StringField(label='Phone number: ', validators=[DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    #takes in input from the user of their login credentials
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class InputData(FlaskForm):
    date_recorded = DateField(label='Date')
    average_container_weight = DecimalField(label='Average container weight: ')
    vessel_waiting_time = IntegerField(label="Vessel Waiting time: ")
    world_value = IntegerField(label="World value: ")
    singapore_value = IntegerField(label="Singapore Value: ")
    no_of_ships = IntegerField('Number of ships: ')
    no_of_containers = IntegerField("Number of containers: ")
    continue_button = SubmitField('Continue')


class Notepad(FlaskForm):
    text_description = TextAreaField(validators=[DataRequired()])
    submit_note = SubmitField("Submit note")