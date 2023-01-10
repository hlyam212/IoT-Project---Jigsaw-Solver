from flask import Flask, render_template,request
from PIL import Image,ImageChops
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math 

import time
import sys
from adafruit_servokit import ServoKit
import tkinter as tk
from tkinter import ttk

nbPCAServo=6

MIN_IMP=[500,500,500,500,500,500]
MAX_IMP=[2500,2500,2500,2500,2500,2500]
MIN_ANG=[0,0,0,0,0,0]
MAX_ANG=[180,180,180,180,180,180]

INT_ANG=[160, 70, 50, 150, 0, 179]#Init
PIC_ANG=[160, 70, 50, 150, 0, 179]#Pickup
DRO_ANG=[160, 70, 50, 150, 0, 179]#Drop
MT1_ANG=[160, 70, 50, 150, 0, 179]#Move To 0
MT2_ANG=[160, 70, 50, 150, 0, 179]#Move To 1
MT3_ANG=[160, 70, 50, 150, 0, 179]#Move To 2
MT4_ANG=[160, 70, 50, 150, 0, 179]#Move To 3

pca=ServoKit(channels=16)

#from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/PS01ModelSelect')
def staticPage():
    return render_template('PS01ModelSelect.html')

@app.route('/PS02Upload')
def upload_file():
   return render_template('PS02Upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_back():
   if request.method == 'POST':
        
        #read image file string data
        filestr = request.files['file'].read()
        #convert string data to numpy array
        print(filestr)
        file_bytes = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        img1 = Image.frombytes('RGB', (500,500), file_bytes, 'raw')
        img2 = Image.open('../img/{0}.png'.format(request.form['modalNum']))

        plt.imshow(img1)
        plt.show()

        result=DetectMain(img1,img2)
        return result

def DetectMain(img1,img2):
    inputPic= np.asarray(img1)      
    fullPic = np.asarray(img2)          # queryImage

    area,areaCode,crop_img=DetectPosition(inputPic,fullPic)

    rotatAngle=DetectRotationAngle(inputPic,crop_img)

    result='Match point sum:{0}; Prediect Area:{1}; Rotat Angle:{2}'.format(area,areaCode,rotatAngle)
    print(result)

    if(areaCode==0):
        ArmMove(INT_ANG)
        ArmMove(PIC_ANG)
        ArmMove(MT1_ANG)
        ArmMove(DRO_ANG)
    elif(areaCode==1):
        ArmMove(INT_ANG)
        ArmMove(PIC_ANG)
        ArmMove(MT2_ANG)
        ArmMove(DRO_ANG)
    elif(areaCode==2):
        ArmMove(INT_ANG)
        ArmMove(PIC_ANG)
        ArmMove(MT3_ANG)
        ArmMove(DRO_ANG)
    else:
        ArmMove(INT_ANG)
        ArmMove(PIC_ANG)
        ArmMove(MT4_ANG)
        ArmMove(DRO_ANG)

    return result

def DetectPosition(inputPic,fullPic):
    # Initiate SIFT detector
    sift = cv.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(fullPic,None)
    kp2, des2 = sift.detectAndCompute(inputPic,None)
    # BFMatcher with default params
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    # Apply ratio test
    good = []
    area=[0,0,0,0,0]
    
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            point=kp1[m.queryIdx].pt
            if(point[0]<=100 and point[1]<=100):
                area[0]+=1
            elif(point[0]>100 and point[1]<=100):
                area[1]+=1
            elif(point[0]<=100 and point[1]>100):
                area[2]+=1
            elif(point[0]>100 and point[1]>100):
                area[3]+=1
            else:
                area[4]+=1
    # cv.drawMatchesKnn expects list of lists as matches.
    img3 = cv.drawMatchesKnn(fullPic,kp1,inputPic,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    areaCode=area.index(max(area))

    if(areaCode==0):
        rectXY=(0,0)
    elif(areaCode==1):
        rectXY=(100,0)
    elif(areaCode==2):
        rectXY=(0,100)
    else:
        rectXY=(100,100)
    # 裁切圖片
    crop_img = fullPic[rectXY[1]:100+rectXY[1], rectXY[0]:100+rectXY[0]]

    return area,areaCode,crop_img

def DetectRotationAngle(inputPic,correctPiece):
    im1 = Image.fromarray(inputPic)
    im2 = Image.fromarray(correctPiece)

    mse = []
    for i in range(360):
        im2_rot = im2.rotate(i)
        mse.append(rmsdiff(im1,im2_rot))

    result=mse.index(min(mse)) # outputs 90 degrees
    return result

def rmsdiff(x, y):
  """Calculates the root mean square error (RSME) between two images"""
  errors = np.asarray(ImageChops.difference(x, y)) / 255
  return math.sqrt(np.mean(np.square(errors)))

def ArmMove(angles):
    acending=1
    for a in range(nbPCAServo):
        b=(int)(angles[a])
        startAng=(int)(pca.servo[a].angle)
        endAng=b
        if pca.servo[a].angle>b:
            acending=-1

        for j in range(startAng,endAng,acending):
            pca.servo[a].angle=j
            time.sleep(0.015)

if __name__ == '__main__':
    app.debug = True
    app.trace = True
    app.run('0.0.0.0',debug=True)