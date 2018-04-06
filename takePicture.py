#!/usr/bin/python

# -*- coding: utf 8 -*-

"""
*************************************************************************
* Created for: Gilroy Lab @ UW-Madison
* Created by: Alex Bilgri on Dec 3rd, 2015
* Modified by: Kyle Schneider on Jan 23rd, 2016
* _______________________
*
* This program is free software: you can redistribute it and/or modify it.
* This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY!
*************************************************************************
"""

import sys
import os
import datetime
from subprocess import call
from PIL import Image
import picamera
from time import sleep
import time

GenColor = True
GenGrey = True
#The number of false colors must be equal to (N*4)+1
#for instance, (2*4)+1 = 9
# or (64*4)+1 = 257
numFalseColors = 1025

def NDVI(photName, directory):
   """Generates greyscale and false color image as needed"""
   
   
   if GenGrey == True:
       
       print "Opening photo for greyscale generation..."
       #print directory + "/regPic/" + photName + ".jpg"
       startGS = time.clock()
       img = Image.open(directory + "/regPic/" + photName + ".jpg")
       width, height = img.size
       pixels = img.load()
       
       for x in range(0,width):
           #print x
           for y in range(0,height):
               #Store each pixel in a variable
               onePixel = pixels[x,y]

               if ((onePixel[0] and onePixel[2]) == 0):
                   newPixel = 0
               else:
                   #Perform the NDVI transform if red and blue are non-zero
                   ###for blue filter
                   newPixel = ((float(onePixel[0])-float(onePixel[2]))/(float(onePixel[0])+float(onePixel[2])))
                   ###testing for red filter
                   #newPixel = ((float(onePixel[2])-float(onePixel[0]))/(float(onePixel[2])+float(onePixel[0])))
                   #NDVI creates a number between -1 and 1               
                   #Normalized to 0-255
                   newPixel += 1                
                   newPixel *= 127.5

               #The next step only takes integers, round               
               newPixel = int(round(newPixel))
               #print newPixel
               #write each pixel with NDVI
               pixels[x,y] = (newPixel, newPixel, newPixel) #order is (Red, Green, Blue) Derp
       
       #save greyscale
       endGS = time.clock()
       print "Saving photo..."
       print endGS - startGS
       img.save(directory + "/greyScale/" + photName + "greyScale.jpg")
   
   
   if GenColor == True:
       
       #Open File
       print "opening photo for False-color generation..."
       startFC = time.clock()
       img = Image.open(directory + "/regPic/" + photName + ".jpg")
       #img = Image.open(directory + "/regPic/" + photName + ".jpg")
       width, height = img.size
       pixels = img.load()
       
       #generate a 256 color list (0,0,255) to (255,0,0) is blue to red
       colorList = genColorList(numFalseColors)
       for x in range(0,width):
           #print x
           for y in range(0,height):
               #Store each in a variable
               onePixel = pixels[x,y]
               if ((onePixel[0] and onePixel[2]) == 0):
                   newPixel = 0
                   #print "NANA"
               else:
                   #NDVI transform
                   newPixel = ((float(onePixel[0])-float(onePixel[2]))/(float(onePixel[0])+float(onePixel[2])))
                   #adjust -255 to 255
                   newPixel *= numFalseColors-1
                   #print newPixel
                   
               
	       #Round for next step
               newPixel = -int(round(newPixel))
               #Write pixel with the NDVI lookup in colorList
               pixels[x,y] = colorList[newPixel]
               
       #save image!
       endFC = time.clock()
       print "Saving photo..."
       print endFC - startFC
       img.save(directory + "/NDVI/" + photName + "NDVI.jpg")
       print "***********************************************"
  

def genColorList(n):
    """Generates n-long list of tuples that contain RGB values 
       between blue and red"""
       
    #number of transition steps between the below 4 functions
    q = (n-1)/4
    
    colorList = []
    
    #Blue to blue-green (0,0,255) -> (0,255,255)
    for i in range(0,q):
        j = int(255*i/q)
        colorList.append((0,j,255))
      
    #Blue-green to Green (0,255,255) -> (0,255,0)
    for i in range(0,q):
        j = 255-int(255*i/q)
        colorList.append((0,255,j))
        
    #Green to yellow (0,255,0) -> (255,255,0)
    for i in range(0,q):
        j = int(255*i/q)
        colorList.append((j,255,0))
        
    #Yellow to red (255,255,0) -> (255,0,0)
    for i in range(0,q+1):
        j = 255-int(255*i/q)
        colorList.append((255,j,0))
        
        
    return colorList

def genName():
    """account for any zeros in the date, like '06' instead 
    of '6' for 6AM"""
    
    UTC = datetime.datetime.utcnow()
    time = UTC - datetime.timedelta(hours = 6) #correct for CST

    if time.minute > 9:
	    minutes = str(time.minute)
    elif time.minute == 0:
	    minutes = '00'
    else:
	    minutes = '0' + str(time.minute)

    if time.hour > 9:
	    hours = str(time.hour)
    elif time.hour == 0:
	    hours = '00'
    else:
	    hours = '0' + str(time.hour)

    if time.day > 9:
	    days = str(time.day)
    else:
	    days = '0' + str(time.day)

    if time.month > 9:
	    months = str(time.month)
    else:
	    months = '0' + str(time.month)

    ##########needs to be revamped, naming convention is not very good...
    #photoname = "/home/pi/Desktop/" + testName + "/dish" + petriDishNum + "%s" % (time.year) + months + days + hours + minutes + ".jpg"
    photoname = "%s" % (time.year) + months + days + hours + minutes
    print photoname
    return photoname




def takePic(directory):
   photName = genName()
   print directory + "/regPic/" + photName + ".jpg"
   imageName = directory + "/regPic/" + photName + ".jpg"
   takePhotoCmd = "fswebcam --rotate 270 -r 1280x960 -S 30 " + imageName
   call([takePhotoCmd], shell = True)
   NDVI(photName, directory)


####OTHER WAYS FOR TAKING IMAGES WITH PI CAMERA

##takePhotoCmd = "fswebcam -r 1200x900 -S 30 " + photName
##print photName
##takePhotoCmd = photName
##call ([takePhotoCmd], shell = True)

##camera = picamera.PiCamera()
##camera.resolution = (1024, 768)
##camera.vflip = True
##camera.brightness = 50
##camera.capture(photName)


