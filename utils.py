# -*- coding: utf-8 -*-
"""utils

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1850-k5tzux1O1NuPgBE30xiKnao0zRQQ
"""

import torch
import torchvision
# from dataset import Dataset
from torch.utils.data import DataLoader

def save_checkpoint(state, filename='my_checkpoint.pth.tar'):
  #모델 체크포인트를 저장할 때 일반적으로 사용되는 파일 확장자
  # 가중치(weight), 최적화 상태(optimizer state), 에폭(epoch) 등을 포함하는 모델 체크포인트를 저장하는 데 사용
  print('=>  체크포인트 저장중')
  torch.save(state,filename) #현 state를 filename에 저장

def load_checkpoint(checkpoint,model):
  print('=> 체크포인트 로딩중')
  model.load_state_dict(checkpoint['state_dict'])

def get_loaders(
      train_imgdir,
      train_maskdir,
      val_imgdir,
      val_maskdir,
      batchsize,
      train_transform,
      val_transform,
      num_workers=4,
      pin_memory=True,
  ):
  train_ds = Dataset(image_dir=train_imgdir, #dataset.py 에정의한 클래스
                     mask_dir=train_maskdir,
                     transform =train_transform)
  train_loader = DataLoader(train_ds,   #import한 module
                            batch_size =batchsize,
                            num_workers=num_workers,
                            pin_memory =pin_memory,
                            shuffle=True)
  val_ds = Dataset(image_dir=val_imgdir,
                    mask_dir=val_maskdir,
                     transform =val_transform)
  val_loader = DataLoader(val_ds,
                          batch_size =batchsize,
                          num_workers=num_workers,
                          pin_memory =pin_memory,
                          shuffle=False)
def check_accuracy(loader,model,device='cuda'):
  num_correct = 0 #바르게 예측된 픽셀수
  num_pixels = 0
  model.eval()

  with torch.no_grad(): #parameter업뎃 없음
    for x,y in loader:
      x =x.to(device)
      y = y.to(device).unsqueeze(1) #grayscale임으로 channel이 없ㄴ는 상태
      preds = torch.sigmoid(model(x))
      preds = (preds > 0.5).float() #이진분류에서 처리가능한 형태 float으로
      num_correct += (preds==y).sum()
      num_pixels += torch.numel(preds) #number of element
  print(
      f'맞춘픽셀 개수{num_correct}, 전체 픽셀수 {num_pixels}, 정확도는 {num_correct/num_pixels*100:.2f}'
  )
  model.train()

def save_predictions_as_imgs(loader,model,folder='saved_images/',device='cuda'):
  model.eval()
  for idx, (x,y) in enumerate(loader):
    x = x.to(device=device)
    with torch.no_grad():
      preds = torch.sigmoid(model(x))
      preds = (preds > 0.5).float()
    torchvision.utils.save_image(
        preds, f'{folder}/pred_{idx}.png'
    )
    torchvision.utils.save_image(y.unsqueeze(1),f'{folder}')
  model.train()

