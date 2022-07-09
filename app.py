from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models.client import valid_signup, signup_user, valid_login
from db import db
from utils.verification import verifyUser
import numpy as np
import cv2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kyc:kyc_password@localhost/kyc_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret key'

db.init_app(app)
migrate = Migrate(app, db)

@app.post('/signup')
def signup():
    try:
        document = request.files['document']
        selfie = request.files['selfie']
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        location = request.form['location']
        address = request.form['address']
        customerToken = request.form['customerToken']
    except:
        return "required data missing",400
    
    if valid_signup(email,password):
        document = np.fromfile(document,np.uint8)
        document = cv2.imdecode(document,cv2.IMREAD_COLOR)
        selfie = np.fromfile(selfie,np.uint8)
        selfie = cv2.imdecode(selfie,cv2.IMREAD_COLOR)
        verification = verifyUser(document,selfie)
        if verification['verified']:
            user_id = signup_user(
                email,
                password,
                firstname,
                lastname,
                birthdate,
                location,
                address,
                customerToken
            )
        else:
            return jsonify(verification),400
    else:
        return "invalid email or password",400
    return "files uploaded",200

@app.post('/login')
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        customerToken = request.form['customerToken']
    except:
        return "required data missing",400
    user = valid_login(email,password,customerToken)
    if user is not None:
        return str(user.id)
    else:
        return "incorrect username or password",400

@app.post('/verify')
def verify():
    try:
        document = request.files['document']
        selfie = request.files['selfie']
        id = request.form['id']  
        backend = request.form['backend']
    except:
        return "required data missing",400
    document = np.fromfile(document,np.uint8)
    document = cv2.imdecode(document,cv2.IMREAD_COLOR)
    selfie = np.fromfile(selfie,np.uint8)
    selfie = cv2.imdecode(selfie,cv2.IMREAD_COLOR)
    verification = verifyUser(document,selfie)
    # if verification['verified']:
    #     return "verified",200
    # else:
    #     return "unauthorized user",404

    return jsonify(verification),200
        

        

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
