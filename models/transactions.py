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



class Transaction(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # TODO: add transaction date, transaction response