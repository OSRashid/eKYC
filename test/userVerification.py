import requests
import time

url = 'http://localhost:5000/verify'
path = 'dataset/'
users_count = 20
request_count = 0
detection_failed = 0
verified = 0
live = 0
with open('output.csv','w') as f:
	f.write('verified,distance,live,liveProb, faceDepth\n')
start = time.time()
for i in range(users_count):
    response = requests.post(url,files={'selfie':open(path+'document/'+str(i+1)+'.jpg','rb'),'document':open(path+'image/'+str(i+1)+'.jpg','rb')},data={'id':'b7d65094-2e5b-4a05-8e6e-9ffb913ebaf5','backend':'mtcnn'})
    verification = response.json()
    if verification['distance'] == 10000000:
        detection_failed += 1
    if verification['verified']:
        verified += 1
    if verification['live']:
        live += 1
    request_count += 1
    verification['averageFaceDepth'] = 0
    with open('output.csv', 'a') as f:
        f.write("{},{},{},{},{}\n".format(verification['verified'],verification['distance'],verification['live'],verification['liveProb'],verification['averageFaceDepth']))
    print("request number: ",request_count,'/',users_count,'percentage: ',(request_count/(users_count))*100,'%')
end = time.time()
print("accuracy: ",(verified)/(users_count))
print("live accuracy: ",(live)/(users_count))
print("testing time: ",end-start)
print("detection fails: ",detection_failed)