
from utils.FaceNet import  loadModel
from utils.detection import detect_face
from utils.detectors import findEuclideanDistance
from utils.antispoof import antispoof
import cv2
import numpy as np
from keras.preprocessing import image
from PIL import Image
import tensorflow as tf

model = loadModel()

tf_version = tf.__version__
tf_major_version = int(tf_version.split(".")[0])
tf_minor_version = int(tf_version.split(".")[1])
input_shape = model.layers[0].input_shape
    
if type(input_shape) is list:
    input_shape = input_shape[0][1:3]
else:
    input_shape = input_shape[1:3]

if tf_major_version == 2 and tf_minor_version >= 5:
    x = input_shape[0]; y = input_shape[1]
    input_shape = (y, x)

def preprocessing(img,target_size=(160,160)):
    face, _ = detect_face(img)
    if face is not None:
        if face.shape[0] > 0 and face.shape[1] > 0:
            factor_0 = target_size[0] / face.shape[0]
            factor_1 = target_size[1] / face.shape[1]
            factor = min(factor_0, factor_1)
            dsize = (int(face.shape[1] * factor), int(face.shape[0] * factor))
            face_resized = cv2.resize(face, dsize)
            # Then pad the other side to the target size by adding black pixels
            diff_0 = target_size[0] - face_resized.shape[0]
            diff_1 = target_size[1] - face_resized.shape[1]
            face_resized = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2), (diff_1 // 2, diff_1 - diff_1 // 2), (0, 0)), 'constant')

        if face_resized.shape[0:2] != target_size:
            face_resized = cv2.resize(face_resized, target_size)
        face_resized = image.img_to_array(face_resized) 
        face_resized = np.expand_dims(face_resized, axis = 0)
        mean, std = face_resized.mean(), face_resized.std() #facenet
        face_processed = (face_resized - mean) / std  #facenet
    face = Image.fromarray(np.uint8(face)).convert('RGB')
    return face, face_processed

def verifyUser(document, selfie):
    # 1) preprocess face
    if document is not None and selfie is not None:
        _, document = preprocessing(document,target_size=input_shape)
        face, selfie = preprocessing(selfie,target_size=input_shape)
        live = False
        liveProb = antispoof(face)
        if liveProb>0.5:
            live = True
        document_representation = model.predict(document)[0].tolist()
        selfie_representation = model.predict(selfie)[0].tolist()
        distance = findEuclideanDistance(document_representation, selfie_representation)
        distance = np.float64(distance)
        # 3) decide
        threshold = 10
        if distance <= threshold:
            identified = True
        else:
            identified = False
    else:
        identified = False
        distance = 1000000000
    verification = {
        "verified": identified,
        "distance": distance,
        "threshold": threshold,
        'live': live,
        'liveProb': liveProb.item()
    }
    return verification
   
