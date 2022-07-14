import requests
import time

url = 'http://localhost:4000/verify'
path = 'dataset/'
users_count = 19
request_count = 0
confusion_matrix = [[0,0],[0,0]]
detection_failed = 0
with open('output.csv','w') as f:
	f.write('verified,distance\n')
start = time.time()
for i in range(users_count):
    for j in range(users_count):
        response = requests.post(url,files={'document':open(path+'document/'+str(i+1)+'.jpg','rb'),'selfie':open(path+'image/'+str(j+1)+'.jpg','rb')},data={'id':'b7d65094-2e5b-4a05-8e6e-9ffb913ebaf5','backend':'mtcnn'})
        verification = response.json()
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
        verification['averageFaceDepth'] = 0
        with open('output.csv', 'a') as f:
            f.write("{},{},{},{},{}\n".format(verification['verified'],verification['distance'],verification['live'],verification['liveProb'],verification['averageFaceDepth']))
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
print("recall: ",recall)
print("F1-score: ",F1)
print("detection fails: ",detection_failed)
VAL = TP/users_count
FAR = FP/(users_count**2-users_count)
FRR = FN/users_count
print("VAL: ",VAL)
print("FAR: ",FAR)
print("FRR: ",FRR)
