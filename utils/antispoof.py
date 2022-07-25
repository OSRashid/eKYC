import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.resnet import resnet18
from torchvision import transforms
import torch
from PIL import Image

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

class NewPad(object):
    def __init__(self):
        pass
        
    def __call__(self, img, x_size=180, y_size=180):
        width, height = img.size
        pad_width = max(x_size,width)
        pad_height = max(y_size, height)
        left = (pad_width - width)//2
        top = (pad_height - height)//2
        new_img = Image.new(img.mode,(pad_width,pad_height),(0,0,0))
        new_img.paste(img,(left,top))
        return new_img

transform = transforms.Compose([
    NewPad(),
    transforms.RandomRotation(180),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomCrop(160),
    transforms.ToTensor(),
])

model = PatchNet()
model.load_state_dict(torch.load('D:\\university\\GP\\eKYC deploy\\utils\\patchnet.pt',map_location=device))

def antispoof(img, p=9):
    output = torch.tensor([])
    for _ in range(p):
        patch = transform(img)
        with torch.no_grad():
            out = model(patch.unsqueeze(0))
        output = torch.cat((output,out),dim=0)
    average_prob = torch.mean(output,dim=0)
    liveProb = average_prob[0]+average_prob[1]+average_prob[6]
    return liveProb.item()
