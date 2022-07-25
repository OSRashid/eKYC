from uuid import UUID
from utils.verification import verifyUser
import numpy as np
import cv2
from db import  SessionLocal, engine, Base
from fastapi import Depends, FastAPI, File, UploadFile, Request, Form
from models.transactions import create_transaction
from models.customer import get_customer, create_customer
from sqlalchemy.orm import Session
import datetime
from logs.log import log_request, log_error

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Item:
    def __init__(
        self,
        id: UUID = Form(...),
        token: str = Form(...),
        selfie: UploadFile = File(...),
        document: UploadFile = File(...)
    ):
        self.id = id
        self.token = token
        self.selfie = selfie
        self.document = document



@app.post('/verify')
async def verify(request: Request,item: Item = Depends(), db: Session = Depends(get_db)):
    log_request(request)
    start_time = datetime.datetime.now()
    try:
        customer = get_customer(db,item.id)
        if customer.token != item.token:
            return {'error': 'invalid token'}
        if customer.expiration < datetime.datetime.now():
            return {'error': 'token expired'}
    except Exception as e:
        log_error('customer not found',e)
        return {'error': 'invalid customer'}
    try:
        selfie = await item.selfie.read()
        selfie = np.fromstring(selfie,np.uint8)
        selfie = cv2.imdecode(selfie,cv2.IMREAD_COLOR)
    except:
        log_error('verify endpoint', e)
        return {'error': "didn't upload selfie"}
    try:
        document = await item.document.read()
        document = np.fromstring(document,np.uint8)
        document = cv2.imdecode(document,cv2.IMREAD_COLOR)        
    except Exception as e:
        log_error('verify endpoint', e)
        return {'error': "didn't upload document"}
    verification = verifyUser(document,selfie)
    end_time = datetime.datetime.now()
    transaction = create_transaction(
        db,
        customer.id,
        verification['verified'],
        verification['distance'],
        verification['live'],
        verification['liveProb'],
        start_time,
        end_time
    )
    verification['transaction_id'] = transaction.id
    cv2.imwrite('filestore\\{}_selfie.jpg'.format(transaction.id),selfie)
    cv2.imwrite('filestore\\{}_document.jpg'.format(transaction.id),document)
    return verification
        

# TODO: add unit tests
# TODO: switch MTCNN and FaceNet from tensorflow to pytorch