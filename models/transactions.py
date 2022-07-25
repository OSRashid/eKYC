from importlib.abc import Traversable
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, Float, DateTime, ForeignKey
import uuid
from db import Base



class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True),ForeignKey('customer.id'))
    identified = Column(Boolean, nullable=False)
    distance = Column(Float, nullable=False)
    live = Column(Boolean, nullable=False)
    liveProb = Column(Float, nullable=False)
    requestTime = Column(DateTime, nullable=False)
    responseTime = Column(DateTime, nullable=False)


def create_transaction(db, customer_id, identified, distance, live, liveProb, requestTime, responseTime):
    transaction = Transaction(
        customer_id=customer_id,
        identified=identified, 
        distance=distance,
        live=live,
        liveProb=liveProb,
        requestTime=requestTime,
        responseTime=responseTime
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transaction(db,id):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    return transaction