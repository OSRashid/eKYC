# TODO: switch flask to fastAPI
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from db import db
from utils.verification import verifyUser
import numpy as np
import cv2

# from fastapi import FastAPI
# app = FastAPI()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kyc:kyc_password@localhost/kyc_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret key'

# db.init_app(app)
# migrate = Migrate(app, db)


@app.post('/verify')
def verify():
    try:
        document = request.files['document']
        selfie = request.files['selfie']
        id = request.form['id']
    except:
        return "required data missing",400
    document = np.fromfile(document,np.uint8)
    document = cv2.imdecode(document,cv2.IMREAD_COLOR)
    selfie = np.fromfile(selfie,np.uint8)
    selfie = cv2.imdecode(selfie,cv2.IMREAD_COLOR)
    verification = verifyUser(document,selfie)
    # TODO: save transaction to database
    # TODO: add log function to log request and response to log file
    return jsonify(verification),200
        

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000,debug=True)


# TODO: add unit tests
# TODO: switch MTCNN and FaceNet from tensorflow to pytorch