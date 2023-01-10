from flask import Flask, render_template,request
from PIL import Image,ImageChops
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math 

def DetectMain(inputPic,fullPicPath):
    fullPic = cv.imread(fullPicPath)          # queryImage

    area,areaCode,crop_img=DetectPosition(inputPic,fullPic)
    rotatAngle=DetectRotationAngle(inputPic,crop_img)
    result='Match point sum:{0}; Prediect Area:{1}; Rotat Angle:{2}'.format(area,areaCode,rotatAngle)
    print(result)

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
    inputPic=Image.fromarray(inputPic)
    correctPiece=Image.fromarray(correctPiece)
    
    mse = []
    for i in range(360):
        im2_rot = correctPiece.rotate(i)
        mse.append(rmsdiff(inputPic,im2_rot))
    result=mse.index(min(mse))

    print(mse.index(min(mse))) # outputs 90 degrees

    '''
    if 0<=result<=90:
        result=90
    elif 91<=result<=180:
        result=180
    '''
    


    return result

def rmsdiff(x, y):
  """Calculates the root mean square error (RSME) between two images"""
  errors = np.asarray(ImageChops.difference(x, y)) / 255
  return math.sqrt(np.mean(np.square(errors)))


if __name__ == '__main__':
    img = cv.imread('img/BAK/IMG_5629.png')
    result=DetectMain(img,'img/ans.png')
    print(result)