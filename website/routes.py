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
        flash('Password is too short, at least 8 characters, try again',
              category='error')
        return False
    elif re.search("[a-z]", password) is None:
        flash('Password is missing a lowercase letter, try again', category='error')
        return False
    elif re.search("[A-Z]", password) is None:
        flash('Password is missing a uppercase letter, try again', category='error')
        return False
    elif re.search("[0-9]", password) is None:
        flash('Password is missing a digit, try again', category='error')
        return False
    elif re.search("[!@#\$%^&*()_\-+=\{\}\[\]:;\"'<>,.?/|\\~`]", password) is None:
        flash('Password is missing a special character, try again.', category='error')
        return False
    else:
        return "True"

@app.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()
    users = User.query.all()

    attempted_user = User.query.filter_by(username=form.username.data).first()

    if request.method == 'POST':
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Login successfully!', category='success')
            return redirect(url_for('input_details'))

        else:
            flash('Invalid username or password, please try again.', category='error')

    return render_template('index.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    admin_user()
    form = LoginForm()
    csrf = csrfform()

    attempted_user = User.query.filter_by(username=form.username.data).first()

    if request.method == 'POST':
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Login successfully!', category='success')
            return redirect(url_for('input_details'))

        else:
            flash('Invalid username or password, please try again.', category='error')
    

    return render_template('login.html', form=form, csrf=csrf)

@login_required
@app.route('/input_details', methods=['GET', 'POST'])
def input_details():
    form = InputData()
    if request.method == 'POST':
        date_recorded = form.date_recorded.data
        average_container_weight = form.average_container_weight.data
        vessel_waiting_time = form.vessel_waiting_time.data
        world_value = form.world_value.data
        singapore_value = form.singapore_value.data
        no_of_ships = form.no_of_ships.data
        no_of_containers = form.no_of_containers.data

        new_record = PSA_datalake(date_recorded=date_recorded, average_container_weight=average_container_weight, vessel_waiting_time=vessel_waiting_time, world_value=world_value, singapore_value=singapore_value, no_of_ships=no_of_ships, no_of_containers=no_of_containers)
        db.session.add(new_record)
        db.session.commit()

        flash("Data added successfully!", category="success")
        return redirect(url_for('dashboard'))


    return render_template("input_details.html", form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = Notepad()
    if request.method == "POST":
        note = form.text_description.data
        new_record = Notes_database(note=note)
        db.session.add(new_record)
        db.session.commit()
        flash("Note added!", category="success")

    return render_template('notes.html', form=form)

@app.route('/AI')
def AI():
    return render_template("iframe.html")
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = Settings_form()
    
    return render_template("settings.html", form=form)

@app.route("/add_item", methods=["POST"])
def add_settings():
    form = Settings_form()
    if request.method == "POST":
        settings = Settings(number=form.no_of_items.data, unit=form.unit.data)
        db.session.add(settings)
        db.session.commit()
        flash("Settings added!", category="success")

    return redirect(url_for('settings'))


@app.route("/update_item", methods=["POST"])
def update_settings(id):
    form = Update_Quantity()
    if request.method == "POST":
        settings = Settings.query.filter_by(id=id).first()
        settings.unit = Update_Quantity.no_of_items.data
        db.session.commit()
        flash("Settings updated!", category="success")

    return redirect(url_for('settings'))


@app.route("/delete_item", methods=["POST"])
def delete_settings(id):
    if request.method == "POST":
        settings = Settings.query.filter_by(id=id).first()
        db.session.delete(settings)
        db.session.commit()
        flash("Deleted successfully!", category="success")

    return redirect(url_for('settings'))

@app.route("/resources")
def reosources():
    return render_template("resources.html")