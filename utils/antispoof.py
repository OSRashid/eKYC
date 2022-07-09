import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.resnet import resnet18
from torchvision import transforms
import torch
import copy

class PatchNet(nn.Module):
    def __init__(self):
        super(PatchNet,self).__init__()
        self.encoder = resnet18()
        self.encoder.fc = nn.Sequential()
        self.fc = nn.Linear(512,9, bias=False)
    def forward(self,x):
        with torch.no_grad():
            x = self.encoder(x)
            self.fc.weight.data = F.normalize(self.fc.weight.data, p=2, dim=1) 

            x = F.normalize(x, p=2, dim=1)

            wf = self.fc(x)
            x = F.softmax(30 * wf)
        return x
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.RandomRotation(180),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomResizedCrop(160),
    transforms.ToTensor(),
])

model = PatchNet()
model.load_state_dict(torch.load('D:\\university\\GP\\eKYC deploy\\utils\\patchnet.pt',map_location=device))

def antispoof(img, p=9):
    output = torch.tensor([])
    for _ in range(p):
        patch = transform(img)
        out = model(patch.unsqueeze(0))
        output = torch.cat((output,out),dim=0)
    average_prob = torch.mean(output,dim=0)
    liveProb = average_prob[0]+average_prob[1]+average_prob[6]
    return liveProb
    

