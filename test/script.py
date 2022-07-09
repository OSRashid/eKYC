import cv2
from sklearn.metrics import confusion_matrix
# from utils.FaceNet import  loadModel
# from utils.detection import detect_face
# from utils.detectors import findEuclideanDistance
import numpy as np
import tensorflow as tf
# from utils.verification import preprocessing
import time

tf_version = tf.__version__
tf_major_version = int(tf_version.split(".")[0])
tf_minor_version = int(tf_version.split(".")[1])
# from utils.dlib import loadModel
import dlib
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('utils/dlib/shape_predictor_5_face_landmarks.dat')
model = dlib.face_recognition_model_v1('utils/dlib/dlib_face_recognition_resnet_model_v1.dat')
users_count = 17
confusion_matrix = [[0,0],[0,0]]
detection_failed = 0
request_count = 0
# input_shape = model.layers[0].input_shape
# if type(input_shape) is list:
#         input_shape = input_shape[0][1:3]
# else:
#     input_shape = input_shape[1:3]

# if tf_major_version == 2 and tf_minor_version >= 5:
#     x = input_shape[0]; y = input_shape[1]
#     input_shape = (y, x)
start = time.time()
threshold = 0.6
# docs = []
# selfies = []
# docs_reps = []
# selfies_reps = []
# for i in range(users_count):
#     docs.append(preprocessing(detect_face(cv2.imread(f"../dataset/document/{i+1}.jpg"))))
#     selfies.append(preprocessing(detect_face(cv2.imread(f"../dataset/image/{i+1}.jpg"))))
    
for i in range(1,users_count+1):
    doc = cv2.imread('dataset/document/'+str(i)+'.jpg')
    doc = cv2.cvtColor(doc, cv2.COLOR_BGR2RGB)
    # doc, _ = detect_face(doc,detector='dlib')
    # if doc is not None:
    #     bgr_doc = cv2.cvtColor(doc, cv2.COLOR_RGB2BGR)
        # cv2.imwrite('output\A{}.jpg'.format(i),doc)
    # doc = preprocessing(doc,method='dlib',target_size=input_shape)

    for j in range(1,users_count+1):
        selfie = cv2.imread('dataset/image/'+str(j)+'.jpg')
        selfie = cv2.cvtColor(selfie, cv2.COLOR_BGR2RGB)
        if selfie is not None and doc is not None:
            selfie_dets = detector(selfie,1)
            doc_dets = detector(doc,1)
            selfie_det = selfie_dets[0]
            doc_det = doc_dets[0]
            selfie_shape = sp(selfie,selfie_det)
            doc_shape = sp(doc,doc_det)
            selfie_chip = dlib.get_face_chip(selfie,selfie_shape,size=150)
            doc_chip = dlib.get_face_chip(doc,doc_shape,size=150)
            selfie_rep = model.compute_face_descriptor(selfie_chip)
            selfie_rep = np.array(selfie_rep)
            selfie_rep = np.expand_dims(selfie_rep, axis = 0)[0]
            doc_rep = model.compute_face_descriptor(doc_chip)
            doc_rep = np.array(doc_rep)
            doc_rep = np.expand_dims(doc_rep, axis = 0)[0]
            distance = np.linalg.norm(selfie_rep-doc_rep)
            # selfie, _  = detect_face(selfie,detector='dlib')
            # if selfie is not None:
            #     bgr_selfie = cv2.cvtColor(selfie, cv2.COLOR_RGB2BGR)
                # cv2.imwrite('output\B{}.jpg'.format(j),selfie)
            # selfie = preprocessing(selfie, method='dlib',target_size=input_shape)
            # try:
            #     with tf.device('/cpu:0'):
            #         document_representation = model.predict(doc)[0].tolist()
            #         selfie_representation = model.predict(selfie)[0].tolist()
            #         distance = findEuclideanDistance(document_representation, selfie_representation)
            # except:
            #     print("no face detected")
            #     identified = False
            #     distance = 10000000
            #     verification = {
            #         "verified": identified,
            #         "distance": distance,
            #     }
            distance = np.float64(distance)
            # 3) decide
            if distance <= threshold:
                identified = True
            else:
                identified = False
        else:
            identified = False
            distance = 10000000
        verification = {
            "verified": identified,
            "distance": distance,
            "threshold": threshold,
            "model": "FaceNet",
            "backend": "mtcnn",
            "metric": "euclidean"
        }
        if verification['distance'] == 10000000:
            detection_failed += 1
        if i == j:
            if verification['verified']:
                confusion_matrix[0][0] += 1
            else:
                confusion_matrix[1][0] += 1
        else:
            if verification['verified']:
                confusion_matrix[0][1] += 1
            else:
                confusion_matrix[1][1] += 1
        request_count += 1
        print("request number: ",request_count,'/',users_count**2,'percentage: ',(request_count/(users_count**2))*100,'%')
end = time.time()
print(confusion_matrix)
print("accuracy: ",(confusion_matrix[0][0]+confusion_matrix[1][1])/(users_count*users_count))
print("testing time: ",end-start)
TP = confusion_matrix[0][0]
FP = confusion_matrix[0][1]
FN = confusion_matrix[1][0]
precision = TP/(TP+FP)
recall = TP/(TP+FN)
F1 = 2*(precision*recall)/(precision+recall)
print("precision: ",precision)
print("recall:",recall)
print("F1-score: ",F1)
print("detection fails: ",detection_failed)