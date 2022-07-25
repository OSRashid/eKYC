from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Column, DateTime
import uuid
from db import Base
from sqlalchemy.orm import relationship
import random
import string
import datetime

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(80), nullable=False)
    token = Column(String(150),nullable=False)
    expiration = Column(DateTime,nullable=False)   
    transactions = relationship('Transaction')



def get_customer(db,id):
    customer = db.query(Customer).filter(Customer.id == id).first()
    return customer

def create_customer(db,name):
    token = ''.join((random.choice(string.ascii_letters+string.digits+string.punctuation)) for x in range(10))
    customer = Customer(name=name, token=token, expiration=datetime.datetime.now()+datetime.timedelta(days=30))
    db.add(customer)
    db.commit()
    db.refresh(customer)
