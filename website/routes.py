from website import *
from flask import render_template, redirect, url_for, flash, request, Response, session, send_from_directory, jsonify, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import text
from website.Forms import *
from website.models import *
from flask_login import login_user, logout_user, login_required, current_user
import re
import shelve
from werkzeug.utils import secure_filename
import PIL
import os
from uuid import uuid1, uuid4
# from flask_recaptcha import ReCaptcha
from markupsafe import Markup
# csrf
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

class csrfform(FlaskForm):
    country_name = StringField('country_name')


# end csrf
bcrypt = Bcrypt()
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mailbottesting8@gmail.com'
app.config['MAIL_PASSWORD'] = 'ulyjlirkskxgrkqb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = False
csrf = CSRFProtect()
csrf.init_app(app)



def check_password_strength(password):
    if len(password) < 8:
        flash("Password is too short, at least 8 characters, try again",
              category='danger')
        return False
    elif re.search("[a-z]", password) is None:
        flash("Password is missing a lowercase letter, try again", category='danger')
        return False
    elif re.search("[A-Z]", password) is None:
        flash("Password is missing a uppercase letter, try again", category='danger')
        return False
    elif re.search("[0-9]", password) is None:
        flash("Password is missing a digit, try again", category='danger')
        return False
    elif re.search("[!@#\$%^&*()_\-+=\{\}\[\]:;\"'<>,.?/|\\~`]", password) is None:
        flash("Password is missing a special character, try again.", category='danger')
        return False
    else:
        return "True"

@app.route('/')
def index():
    csrf = csrfform()
    users = User.query.all()

    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login_page():
    admin_user()
    form = LoginForm()
    csrf = csrfform()

    attempted_user = User.query.filter_by(username=form.username.data).first()

    if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
        login_user(attempted_user)

    else:
        flash("Invalid username or password, please try again.", category='danger')
    

    return render_template('login.html', form=form, csrf=csrf)


