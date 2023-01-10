from PIL import Image, ImageChops
import numpy as np
import cv2 as cv
import math 
import matplotlib.pyplot as plt

def rmsdiff(x, y):
  """Calculates the root mean square error (RSME) between two images"""
  errors = np.asarray(ImageChops.difference(x, y)) / 255
  return math.sqrt(np.mean(np.square(errors)))
'''
inputPic = cv.imread('img/BAK/IMG_5629.png')
fullPic = cv.imread('img/ans.png')
rectXY=(0,0)
fullPic = fullPic[rectXY[1]:100+rectXY[1], rectXY[0]:100+rectXY[0]]

im11=Image.fromarray(inputPic,'RGBA')
im21=Image.fromarray(fullPic,'RGBA')
'''
im1 = Image.open("img/BAK/IMG_5629.png")
im2 = Image.open("img/BAK/Rotat2.png")


mse = []
for i in range(360):
  im2_rot = im2.rotate(i)
  mse.append(rmsdiff(im1,im2_rot))

print(mse.index(min(mse))) # outputs 90 degrees
plt.plot(mse)
plt.show()