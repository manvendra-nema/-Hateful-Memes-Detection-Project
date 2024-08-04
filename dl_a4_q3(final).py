# -*- coding: utf-8 -*-
"""DL_A4_Q3(final).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tFy_MUud0KpP9xu4unOpuOtuMq_FHgxu
"""

!pip install transformers

# import libraries
import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
from torchvision.transforms import transforms
import torchvision
import numpy as np
import json
from torch.utils.data import Dataset
import cv2
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn import preprocessing
from tqdm.notebook import tqdm
import warnings
warnings.filterwarnings('ignore')

# import libraries
import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
from torchvision.transforms import transforms
import torchvision
import numpy as np
import json
from torch.utils.data import Dataset
import cv2
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn import preprocessing
from tqdm.notebook import tqdm
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import torch
import torch.optim as optim
# import wandb
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel
from torch.nn.utils.rnn import pad_sequence
import os

from google.colab import drive
drive.mount('/content/drive')

train_text = pd.read_json("/content/drive/MyDrive/A4/hateful_memes/train.jsonl",lines=True)
test_text = pd.read_json("/content/drive/MyDrive/A4/hateful_memes/dev_seen.jsonl",lines=True)
val_text = pd.read_json("/content/drive/MyDrive/A4/hateful_memes/test_seen.jsonl",lines=True)

train_text

val_text

test_text

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# function to return text tokens
def preprocess_text(text):
    tokens = tokenizer.tokenize(text) # Tokenize the text
    token_ids = tokenizer.convert_tokens_to_ids(tokens) # Convert tokens to IDs
    return token_ids

train_text['text'].apply(preprocess_text)[0]

train_text['text_tokens'] = train_text['text'].apply(preprocess_text)
val_text['text_tokens'] = val_text['text'].apply(preprocess_text)
test_text['text_tokens'] = test_text['text'].apply(preprocess_text)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_tokens_text = [torch.tensor(token) for token in train_text['text_tokens']]
train_tokens_text = pad_sequence(train_tokens_text, batch_first=True, padding_value=0)

val_tokens_text = [torch.tensor(token) for token in val_text['text_tokens']]
val_tokens_text = pad_sequence(val_tokens_text, batch_first=True, padding_value=0)

test_tokens_text = [torch.tensor(token) for token in test_text['text_tokens']]
test_tokens_text = pad_sequence(test_tokens_text, batch_first=True, padding_value=0)

train_labels_text = torch.tensor([i for i in train_text['label']])
val_labels_text = torch.tensor([i for i in val_text['label']])
test_labels_text = torch.tensor([i for i in test_text['label']])

# class to load image
class PNGDataset(Dataset):
    def __init__(self, root_dir, df,text ,transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.filenames = os.listdir(root_dir)
        self.df = df
        self.text = text

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        filename = self.filenames[idx]
        file_name = str(self.df['id'][idx])
        if len(file_name) == 4:
            file_name = '0'+file_name
        img_path = os.path.join(self.root_dir, file_name+'.png')
        #print(img_path)
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, self.text[idx], self.df['label'][idx]

# apply necessary transformations like resize and normalize
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((256,256)),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
# split into train, test and val set
train_dataset_img = PNGDataset('/content/drive/MyDrive/img', train_text,train_tokens_text)
val_dataset_img= PNGDataset('/content/drive/MyDrive/img', val_text,val_tokens_text)
test_dataset_img= PNGDataset('/content/drive/MyDrive/img', test_text,test_tokens_text)

train_dataset_img[22][1]

plt.imshow(train_dataset_img[8495][0])

# class that applies transformations to images
class ImageDataset(Dataset):
    def __init__(self, data,transform=None, target_transform=None):
        self.data=data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        
        image = self.data[idx][0]
        text = self.data[idx][1]
        
        # attention = self.data[idx][2]
        
        label = self.data[idx][2]
        if self.transform is not None:
            image = self.transform(image)
        return image,text ,label

ImageDataset(train_dataset_img,transform=transform)[0][1]

batch_size = 128
# defining data loaders
train_loader_img = torch.utils.data.DataLoader(ImageDataset(train_dataset_img,transform=transform), batch_size, shuffle=True)
val_loader_img = torch.utils.data.DataLoader(ImageDataset(val_dataset_img,transform=transform), batch_size)
test_loader_img = torch.utils.data.DataLoader(ImageDataset(test_dataset_img,transform=transform), batch_size*2)

def get_default_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

# data loader class
class DeviceDataLoader():
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        return len(self.dl)

import torch.nn as nn
from torchvision.models.resnet import resnet50
import json
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from sklearn.metrics import accuracy_score, classification_report
from transformers import AutoModel, AutoTokenizer, get_scheduler
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
from torch.optim import AdamW
from tqdm.notebook import tqdm, trange
from time import perf_counter
from PIL import Image
import pandas as pd
device = 'cuda'

class BertClassificationModel(torch.nn.Module):
    def __init__(self):
        super(BertClassificationModel, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = torch.nn.Dropout(0.5)
        self.linear = torch.nn.Linear(768, 2)
        
    # define forward method
    def forward(self, input_ids):
        output = self.bert(input_ids=input_ids)
        pooled_output = output.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.linear(pooled_output)
        return pooled_output
resnet18 = torchvision.models.resnet18(pretrained=True)
resnet18.fc = nn.Linear(in_features=512, out_features=2)
state_dict = torch.load("/content/drive/MyDrive/A4/Q1/model.pth",map_location=torch.device('cpu'))
resnet18.load_state_dict(state_dict)
for param in resnet18.parameters():
      param.requires_grad = False
resnet18.fc = nn.Linear(in_features=512, out_features=128)
bertModel = BertClassificationModel()
bertModel.load_state_dict(torch.load('/content/drive/MyDrive/A4/Q2/text_classifier.pt',map_location=torch.device('cpu')))
for param in bertModel.parameters():
        param.requires_grad = False
bertModel.linear =  torch.nn.Linear(768, 128)
class Merge(nn.Module):
  def __init__(self,text_model,img_model):
    super().__init__()
    self.text_model = text_model
    self.img_model = img_model
    self.linear1 = torch.nn.Linear(896, 64)
    self.linear2 = torch.nn.Linear(64, 2)
  
  def forward(self,text, img):
    a = self.text_model(text)
    b = self.img_model(img)
    c = torch.hstack((a,b))
    # print(c.shape)
    c = self.linear1(c)
    c = self.linear2(c)
    return c
    
merge_model = Merge(bertModel,resnet18)

criterion = nn.CrossEntropyLoss()

learning_rate = 5.0e-5
warmup_steps =200
t_total = len(train_loader_img) * 10
optimizer = torch.optim.Adam(merge_model.parameters(), lr=learning_rate, )
scheduler = get_scheduler(name="cosine", optimizer=optimizer, num_warmup_steps=warmup_steps, num_training_steps=t_total)

tloss=[]
vloss=[]
taccuracy=[]
vaccuracy=[]
prev_acc = 0
from tqdm.autonotebook import tqdm
criterion = nn.CrossEntropyLoss()
# define train loop
merge_model=merge_model.to('cuda')
for epoch in range(10):
    merge_model.train()
    train_loss,train_accuracy = 0,0
    for batch in tqdm(train_loader_img):
        b_imgs,b_inputs, b_labels  = batch    
        
        #inputs,text,attention, labels = batch
        # b_inputs = bert_tokenizer(
        #     list(b_text), truncation=True, max_length=32,
        #     return_tensors="pt", padding=True
        # )
        
        b_labels = b_labels.to(device)
        b_imgs = b_imgs.to(device)
        b_inputs = b_inputs.to(device)

        merge_model.zero_grad()        
        b_logits = merge_model(b_inputs, b_imgs)
        loss = criterion(b_logits, b_labels)
        loss.backward()
        optimizer.step()
        scheduler.step()
        pred_t = np.argmax(b_logits.detach().cpu().numpy(), axis=1)
        train_accuracy += accuracy_score(b_labels.detach().cpu().numpy(), pred_t)
        train_loss += loss.item()
      
        
        
        
    #scheduler.step()
    train_loss = train_loss / len(train_loader_img)
    train_accuracy = train_accuracy / len(train_loader_img)
    merge_model.eval()
    val_loss, val_accuracy = 0, 0
    with torch.no_grad():
        for batch in val_loader_img:
            b_imgs,b_inputs, b_labels  = batch   

            # b_inputs = bert_tokenizer(
            # list(b_text), truncation=True, max_length=32,
            # return_tensors="pt", padding=True)
        
            b_labels = b_labels.to(device)
            b_imgs = b_imgs.to(device)
            b_inputs = b_inputs.to(device)
            

            b_logits = merge_model(b_inputs,b_imgs)
            
            #loss_func = torch.nn.CrossEntropyLoss()
            loss = criterion(b_logits, b_labels)
            val_loss += loss.item()
            preds = np.argmax(b_logits.detach().cpu().numpy(), axis=1)
            val_accuracy += accuracy_score(b_labels.detach().cpu().numpy(), preds)
         
    
    val_loss = val_loss / len(val_loader_img)
    val_accuracy = val_accuracy / len(val_loader_img)
    if val_accuracy > prev_acc:
      prev_acc =val_accuracy
      torch.save(merge_model.state_dict(), '/content/drive/MyDrive/Colab Notebooks/data/model5555.pth')
    train_accuracy=train_accuracy*100
    val_accuracy=val_accuracy*100
    taccuracy.append(train_accuracy)
    vaccuracy.append(val_accuracy)
    tloss.append(train_loss)
    vloss.append(val_loss)
    print(f"Epoch {epoch+1}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}")

# model.load_state_dict(torch.load("/content/model1.pth"))
# model.eval()

# Plot the training and validation loss
plt.plot(tloss, label='Training Loss')
plt.plot(vloss, label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

# Plot the training and validation loss
plt.plot(taccuracy, label='Training Accuracy')
plt.plot(vaccuracy, label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.show()

merge_model.load_state_dict(torch.load("/content/drive/MyDrive/Colab Notebooks/data/model5555.pth"))
merge_model.eval()

# measure test accurancy
correct = 0
total = 0
with torch.no_grad():
    for batch in test_loader_img:
        
        b_imgs,b_inputs, b_labels  = batch    
        
        
        b_labels = b_labels.to(device)
        b_imgs = b_imgs.to(device)
        b_inputs = b_inputs.to(device)

        outputs = merge_model(b_inputs, b_imgs)
        _, predicted = torch.max(outputs.data, 1)
        total += b_labels.size(0)
        correct += (predicted == b_labels).sum().item()

print(f'Test Accuracy :- {100 * correct / total} %')

# Initialize lists to store labels and predictions
targets = []
predictions = []

# Iterate over test set and make predictions
with torch.no_grad():
    for batch in test_loader_img:
        b_imgs,b_inputs, b_labels  = batch    
        
        
        b_labels = b_labels.to(device)
        b_imgs = b_imgs.to(device)
        b_inputs = b_inputs.to(device)

        outputs = merge_model(b_inputs, b_imgs)
        
        _, preds = torch.max(outputs, 1)
        targets += b_labels.tolist()
        predictions += preds.tolist()

# Calculate overall precision, recall, and F1 score
precision, recall, f1_score, _ = precision_recall_fscore_support(targets, predictions, average='macro')

print(f'Overall Precision: {precision:.4f}')
print(f'Overall Recall: {recall:.4f}')
print(f'Overall F1 Score: {f1_score:.4f}')

# Calculate class-wise precision, recall, and F1 score
precision, recall, f1_score, support = precision_recall_fscore_support(targets, predictions)

for i in range(2):
    print(f'Class {i} - Precision: {precision[i]:.4f}, Recall: {recall[i]:.4f}, F1 Score: {f1_score[i]:.4f}')

merge_model=merge_model.to('cpu')

import pickle
with open('parrot.pkl', 'rb') as f:
  compare_labels = pickle.load(f)
compare_labels['text_tokens'] = compare_labels['text'].apply(preprocess_text)
compare_labels_tokens = [torch.tensor(token) for token in compare_labels['text_tokens']]
compare_labels_tokens = pad_sequence(compare_labels_tokens, batch_first=True, padding_value=0)
compare_labels_labels = torch.tensor([i for i in compare_labels['label']])
compare_labels_dataset_img= PNGDataset('/content/drive/MyDrive/img', compare_labels,compare_labels_tokens)
compare_labels_loader_img = torch.utils.data.DataLoader(ImageDataset(compare_labels_dataset_img,transform=transform), 100)
import seaborn as sns
from matplotlib.colors import ListedColormap
from sklearn.manifold import TSNE

def vector(img,text,model):
  l1  = model.text_model(text)  
  l2  = model.img_model(img)
  c = torch.hstack((l1,l2))
    # print(c.shape)
  c = model.linear1(c)
  return c

for batch in compare_labels_loader_img:
  b_imgs,b_inputs, b_labels  = batch
  t = vector(b_imgs,b_inputs,merge_model)
  print (t.shape)
  X_embedded = TSNE(n_components=2, learning_rate='auto',init='pca', perplexity=3).fit_transform(t.detach().numpy())
  x1= []
  y1 = []
  for i in X_embedded:
    x1.append(i[0])
    y1.append(i[1])
  print(b_labels[0])
  print(len(b_labels),len(x1),len(y1))
  sns.scatterplot(x=x1,y=y1,hue=b_labels,palette="deep")     
  cmap = ListedColormap(sns.color_palette("deep", 256).as_hex())

  break