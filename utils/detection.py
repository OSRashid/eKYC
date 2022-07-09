from utils.detectors import mtcnn


def detect_face(img):	
	obj = mtcnn(img)
	if len(obj) > 0:
		face, region = obj[0] #discard multiple faces
	else: #len(obj) == 0
		face = None
		region = [0, 0, img.shape[0], img.shape[1]]
	return face, region
