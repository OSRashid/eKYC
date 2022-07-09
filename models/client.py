from lib2to3.pgen2 import token
from random import random
from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from models.customer import Customer 
import string
from hashlib import sha256
import random
from werkzeug.security import generate_password_hash,check_password_hash



class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),nullable=False)
    birthdate = db.Column(db.String(80),nullable=False)
    location = db.Column(db.String(80),nullable=False)
    address = db.Column(db.String(80),nullable=False)
    firstname = db.Column(db.String(80),nullable=False)
    lastname = db.Column(db.String(80),nullable=False)
    customerId = db.Column(UUID(as_uuid=True),db.ForeignKey('customer.id'),nullable=False)
    salt = db.Column(db.String(10),nullable=False)

    def __init__(self,
        email,
        password,
        firstname,
        lastname,
        birthdate,
        location,
        address,
        customerToken):
        self.email = email
        self.birthdate = birthdate
        self.location = location
        self.address = address
        self.firstname = firstname
        self.lastname = lastname
        self.salt = "".join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k=10))
        self.password = sha256((password+self.salt).encode()).hexdigest()
        customer = Customer.query.filter_by(token=customerToken).first()
        if customer is None:
            return False
        self.customerId = customer.id

def valid_signup(em,password):
    user = Client.query.filter_by(email=em).first()
    if user is not None:
        return False
    else:
        if len(password)>8 and password.isalnum():
            return True
        return False

def signup_user(
    email,
    password,
    firstname,
    lastname,
    birthdate,
    location,
    address,
    customerToken):
    user = Client(
        email,
        password,
        firstname,
        lastname,
        birthdate,
        location,
        address,
        customerToken
    )
    db.session.add(user)
    db.session.commit()
    return user.id

def valid_login(em,password,customerToken):
    user = Client.query.filter_by(email=em).first()
    if user is not None:
        customer = Customer.query.filter_by(token=customerToken).first()
        if user.password == sha256((password+user.salt).encode()).hexdigest() and customerToken==customer.token:
            return user
    return None