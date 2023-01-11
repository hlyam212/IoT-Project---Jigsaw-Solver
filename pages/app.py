from flask import Flask, render_template,request
from PIL import Image,ImageChops
import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math 
from werkzeug import secure_filename

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

INT_ANG=[40, 80, 80, 150, 0, 0]#Init
PIC_ANG=[[1,5,1],[40,180, 80]]#[40, 40, 80, 150, 0, 180, 80]#Pickup[0,1,2,3,4,5,1]
MT1_ANG=[[0,3,1,5,1],[168,135,50,0,80]]#Move To 0
MT2_ANG=[[0,3,1,5,1],[145,135,50,0,80]]#Move To 1
MT3_ANG=[[0,3,1,5,1],[168,160,50,0,80]]#Move To 2
MT4_ANG=[[0,3,1,5,1],[145,160,50,0,80]]#Move To 3

ORDERLIST=range(nbPCAServo)

pca=ServoKit(channels=16)

UPLOAD_FOLDER = './static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/PS01ModelSelect')
def staticPage():
    return render_template('PS01ModelSelect.html')

@app.route('/PS02Upload')
def upload_file():
    path=request.full_path
    picFileName=path.split('=')[1]
    print("PS02Upload.html : {}".format(picFileName))
    return render_template('PS02Upload.html',modalNum=picFileName)

@app.route('/runExit')
def runExit():
   return exit()
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_back():
   if request.method == 'POST':
        print("uploader START")
        f = request.files['file11']
        filePath=os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))
        f.save(filePath)
        print("uploader Saved Pic :{}".format(filePath))
        
        picFileName=request.form['modalNum']
        
        img1 = Image.open(filePath)
        img2 = Image.open('../img/{0}.png'.format(picFileName))
        print("uploader Opened Pic :")
        result=DetectMain(img1,img2)
        return render_template('PS02Upload.html', resultMSG=result,modalNum=picFileName)

def DetectMain(img1,img2):
    print("uploader DetectMain START")
    inputPic= np.asarray(img1)      
    fullPic = np.asarray(img2)          # queryImage

    area,areaCode,crop_img=DetectPosition(inputPic,fullPic)

    rotatAngle=DetectRotationAngle(inputPic,crop_img)

    result='Match point sum:{0}; Prediect Area:{1}; Rotat Angle:{2}'.format(area,areaCode,rotatAngle)
    print(result)
    
    init()
    if(areaCode==0):
        ArmMove(PIC_ANG[1],PIC_ANG[0])
        ArmMove(MT1_ANG[1],MT1_ANG[0])
        ArmMove(INT_ANG,ORDERLIST)
    elif(areaCode==1):
        ArmMove(PIC_ANG[1],PIC_ANG[0])
        ArmMove(MT2_ANG[1],MT2_ANG[0])
        ArmMove(INT_ANG,ORDERLIST)
    elif(areaCode==2):
        ArmMove(PIC_ANG[1],PIC_ANG[0])
        ArmMove(MT3_ANG[1],MT3_ANG[0])
        ArmMove(INT_ANG,ORDERLIST)
    else:
        ArmMove(PIC_ANG[1],PIC_ANG[0])
        ArmMove(MT4_ANG[1],MT4_ANG[0])
        ArmMove(INT_ANG,ORDERLIST)

    print("uploader DetectMain END")
    return result

def DetectPosition(inputPic,fullPic):
    print("uploader DetectPosition START")

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

    print("uploader DetectPosition END")
    return area,areaCode,crop_img

def DetectRotationAngle(inputPic,correctPiece):
    print("uploader DetectRotationAngle START")

    im1 = Image.fromarray(inputPic)
    im2 = Image.fromarray(correctPiece)

    mse = []
    for i in range(360):
        im2_rot = im2.rotate(i)
        mse.append(rmsdiff(im1,im2_rot))

    result=mse.index(min(mse)) # outputs 90 degrees

    print("uploader DetectRotationAngle END")
    return result

def rmsdiff(x, y):
  """Calculates the root mean square error (RSME) between two images"""
  errors = np.asarray(ImageChops.difference(x, y)) / 255
  return math.sqrt(np.mean(np.square(errors)))

def init():
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i],MAX_IMP[i])
        pca.servo[i].angle=INT_ANG[i]
        j=INT_ANG[i]
        print("Send angle {} to Servo {}".format(j,i))
        time.sleep(0.5)
    time.sleep(1)
    print('init DONE.')

def ArmMove(angles,orderBy):
    acending=1
    
    for a in range(len(orderBy)):
        startAng=(int)(pca.servo[orderBy[a]].angle)
        endAng=(int)(angles[a])
        
        if startAng>endAng:
            acending=-1
        else:
            acending=1
        print("Ang : {}-{};{}".format(startAng,endAng,acending))
        
        for j in range(startAng,endAng,acending):
            pca.servo[orderBy[a]].angle=j
            time.sleep(0.015)
        
        print("Send angle {} to Servo {}".format((int)(pca.servo[orderBy[a]].angle),orderBy[a]))
        time.sleep(0.5)
    time.sleep(1)
    print('ArmMove DONE.')

def exit():
    for i in range(nbPCAServo):
        pca.servo[i].angle=None
    time.sleep(0.5)
    sys.exit()

if __name__ == '__main__':
    app.debug = True
    app.trace = True
    app.run('0.0.0.0',debug=True)