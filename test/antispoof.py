from utils.antispoof import antispoof
from utils.detection import detect_face
import os
from PIL import Image
import cv2
live_path = 'D:\\university\\GP\\eKYC deploy\\test\\live'
spoof_path = 'D:\\university\\GP\\eKYC deploy\\test\\spoof'

live_files = os.listdir(live_path)
spoof_files = os.listdir(spoof_path)

cm = [[0,0],[0,0]]

for file in live_files:
    filepath = os.path.join(live_path,file)
    img = cv2.imread(filepath)
    face, _ = detect_face(img)
    if face is not None:
        face = Image.fromarray(cv2.cvtColor(face,cv2.COLOR_BGR2RGB))
        liveProb = antispoof(face)
    else:
        liveProb = 0
    if liveProb >0.5:
        cm[0][0] += 1
    else:
        cm[1][0] += 1

for file in spoof_files:
    filepath = os.path.join(spoof_path,file)
    img = cv2.imread(filepath)
    face, _ = detect_face(img)
    if face is not None:
        face = Image.fromarray(cv2.cvtColor(face,cv2.COLOR_BGR2RGB))
        liveProb = antispoof(face)
    else:
        liveProb = 0
    if liveProb < 0.5:
        cm[1][1] += 1
    else:
        cm[0][1] += 1

N = len(live_files)+len(spoof_files)

print(cm)
print("accuracy: ",(cm[0][0]+cm[1][1])/N)
TP = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
precision = TP/(TP+FP)
recall = TP/(TP+FN)
F1 = 2*(precision*recall)/(precision+recall)
print("precision: ",precision)
print("recall:",recall)
print("F1-score: ",F1)