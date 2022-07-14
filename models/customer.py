from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Customer(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(150),nullable=False)
    # TODO: add timestamp column for the expiration date of the key
    def __init__(self,name,token):
        self.name = name
        self.token = token
    
    def setToken(self,token):
        self.token = token


def create_customer(name):
    token = str(uuid.uuid4())
    customer = Customer(name,token)
    db.session.add(customer)
    db.session.commit()
    
