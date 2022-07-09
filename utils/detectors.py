import cv2
import math
from PIL import Image
import numpy as np
from mtcnn import MTCNN


FaceDetector = MTCNN()
def mtcnn(img, align = True):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resp = []
    detected_face = None
    img_region = [0, 0, img.shape[0], img.shape[1]]
    detections = FaceDetector.detect_faces(img_rgb)
    if len(detections) > 0:
        for detection in detections:
            x, y, w, h = detection["box"]
            detected_face = img[int(y):int(y+h), int(x):int(x+w)]
            img_region = [x, y, w, h]
            if align:
                keypoints = detection["keypoints"]
                left_eye = keypoints["left_eye"]
                right_eye = keypoints["right_eye"]
                detected_face = alignment_procedure(detected_face, left_eye, right_eye)
            resp.append((detected_face, img_region))
    return resp

def alignment_procedure(img, left_eye, right_eye):
	#this function aligns given face in img based on left and right eye coordinates
	left_eye_x, left_eye_y = left_eye
	right_eye_x, right_eye_y = right_eye
	#-----------------------
	#find rotation direction
	if left_eye_y > right_eye_y:
		point_3rd = (right_eye_x, left_eye_y)
		direction = -1 #rotate same direction to clock
	else:
		point_3rd = (left_eye_x, right_eye_y)
		direction = 1 #rotate inverse direction of clock
	#-----------------------
	#find length of triangle edges
	a = findEuclideanDistance(np.array(left_eye), np.array(point_3rd))
	b = findEuclideanDistance(np.array(right_eye), np.array(point_3rd))
	c = findEuclideanDistance(np.array(right_eye), np.array(left_eye))
	#-----------------------
	#apply cosine rule
	if b != 0 and c != 0: #this multiplication causes division by zero in cos_a calculation
		cos_a = (b*b + c*c - a*a)/(2*b*c)
		angle = np.arccos(cos_a) #angle in radian
		angle = (angle * 180) / math.pi #radian to degree
		#-----------------------
		#rotate base image
		if direction == -1:
			angle = 90 - angle
		img = Image.fromarray(img)
		img = np.array(img.rotate(direction * angle))
	#-----------------------
	return img #return img anyway

def findEuclideanDistance(source_representation, test_representation):
    if type(source_representation) == list:
        source_representation = np.array(source_representation)
    if type(test_representation) == list:
        test_representation = np.array(test_representation)
    euclidean_distance = np.linalg.norm(source_representation - test_representation)
    return euclidean_distance

def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

def l2_normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))