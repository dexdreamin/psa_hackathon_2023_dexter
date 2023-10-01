from website import bcrypt
from website import db, login_manager
from datetime import datetime
import random
import string
from uuid import uuid4
import shelve
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    admin = db.Column(db.Integer())
    username = db.Column(db.String(length=120))
    # the id unique to each user so that flask can identify each in{{ m3 }}idual user
    password_hash = db.Column(db.String(length=60),
                              nullable=False, unique=True)
    profile_pic = db.Column(db.Text, nullable=True)

    @property
    def password(self):
        return self.password

    # return password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    # hashes the password entered by users creating new accounts

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        # return true or false

class PSA_datalake(db.Model):
    __tablename__ = "PSA datalake"
    id = db.Column(db.Integer, primary_key=True)
    date_recorded = db.Column(db.Integer)
    average_container_weight = db.Column(db.Float(precision=2))
    vessel_waiting_time = db.Column(db.Integer)
    world_value = db.Column(db.Integer)
    singapore_value = db.Column(db.Integer)
    no_of_ships = db.Column(db.Integer)
    no_of_containers = db.Column(db.Integer)

class Notes_database(db.Model):
    __tablename__ = "Notes_database"
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text())


class Settings(db.Model):
    __tablename__ = "Settings"
    id = db.Column(db.Integer, primary_key=True)
    dockhands = db.Column(db.Integer, default=1)
    truckdrivers = db.Column(db.Integer, default=1)
    supervisors = db.Column(db.Integer, default=1)