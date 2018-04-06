"""
*************************************************************************
* Created for: Gilroy Lab @ UW-Madison
* Created by: Kyle Schneider on Jan 23rd, 2016
* _______________________
*
* This program is free software: you can redistribute it and/or modify it.
* This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY!
*************************************************************************

"""


import RPi.GPIO as GPIO
### for stepper motor board
from rrb3 import *
import time
import sys
### for LEDs
import pigpio
### for taking pictures
import subprocess
import os
import takePicture
#import testWebCam

GenColor = True
GenGrey = True

#The number of false colors must be equal to (N*4)+1
#for instance, (2*4)+1 = 9
# or (64*4)+1 = 257
numFalseColors = 1025
#setting up LEDs
pi = pigpio.pi()
# strip 1 of lights
RED_PIN1 = 17
GREEN_PIN1 = 22
BLUE_PIN1 = 24
# strip 2 of lights
RED_PIN2 = 25
GREEN_PIN2 = 13
BLUE_PIN2 = 18
# strip 3 of lights
RED_PIN3 = 27
GREEN_PIN3 = 04
BLUE_PIN3 = 20

#setting motor voltage and input voltage
rr = RRB3(12.0,12.0)

#initalize it to -1 so we know if anything is wrong
petriDishes = -1;

def setLights(pin, brightness):
    pi.set_PWM_dutycycle(pin, brightness)

#This gives the program information on how many directories to set up for images to store in
def askDishes():
    petriDishes = input("How many petri dishes did you put in? ")

    if petriDishes > 6:
        print "must be between 1-6"
        askDishes()

    if petriDishes < 1:
        print "must be between 1-6"
        askDishes()

    print petriDishes
    return petriDishes
    
#makes directories
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def find_dir():
    print ('finding dir')
    directory = os.getcwd()
    print directory

#makes a folder system for your new project inside of directory the program was called from
def settingUpFolders():
    global testName
    testName = raw_input("your test name(no spaces allowed)? ")
    mkdir_p(os.getcwd() + '/' + testName)
    print ('folder ' + testName + ' has been created')

    global petriDishes
    petriDishes = askDishes()

    for x in range(0,petriDishes):
        if x == 0:
            num = 'One'
        if x == 1:
            num = 'Two'
        if x == 2:
            num = 'Three'
        if x == 3:
            num = 'Four'
        if x == 4:
            num = 'Five'
        if x == 5:
            num = 'Six'
        mkdir_p(os.getcwd() + '/' + testName + '/dish' + num)
        mkdir_p(os.getcwd() + '/' + testName + '/dish' + num + '/regPic')
        mkdir_p(os.getcwd() + '/' + testName + '/dish' + num + '/greyScale')
        mkdir_p(os.getcwd() + '/' + testName + '/dish' + num + '/NDVI')


def main():
	print "Please enter petri dishes in order from 1-6,"
	print "also please make sure the camera is pointed at "
	print "petri dish one before starting."	

	settingUpFolders()
	timeInMin = input("How many minutes would you like inbetween each picture? ")

	try:
	    while True:
    	    delay = 10
    	    stepsFor = 8
        	stepsBack = 8 * (petriDishes-1)
        
        	# set 3 testing
        	setLights(RED_PIN3, 255)
        	setLights(BLUE_PIN3, 255)
        	setLights(GREEN_PIN3, 0)
        	    
        	for x in range(0,petriDishes-1):            
            	if x == 0:
                	dishNum = 'One'
            	if x == 1:
                	dishNum = 'Two'
            	if x == 2:
                	dishNum = 'Three'
            	if x == 3:
            	    dishNum = 'Four'
            	if x == 4:
            	    dishNum = 'Five'
            	if x == 5:
            	    dishNum = 'Six'
           
           		takePicture.takePic(os.getcwd() + "/" + testName + "/dish" + dishNum)
            	###other ways to take pictures...
            	#testWebCam.takePic(os.getcwd() + "/" + testName + "/dish" + dishNum) 
            	#subprocess.Popen([sys.executable, "takePicture.py", str(dishNum)])
            	###### end camera code #####
            	rr.step_forward(int(delay)/1000.0,int(stepsFor))
            	print 'start timing'
            	time.sleep(60*timeInMin)
            	print 'end timing'
        	#### camera code
        	if petriDishes == 1:
        	    dishNum = 'One'
        	if petriDishes == 2:
        	    dishNum = 'Two'
        	if petriDishes == 3:
        	    dishNum = 'Three'
        	if petriDishes == 4:
        	    dishNum = 'Four'
        	if petriDishes == 5:
        	    dishNum = 'Five'
        	if petriDishes == 6:
        	    dishNum = 'Six'
        	takePicture.takePic(os.getcwd() +"/" + testName + "/dish" + dishNum)
        	###other ways to take pictures...
        	#testWebCam.takePic(os.getcwd() + "/" + testName + "/dish" + dishNum) 
        	#subprocess.call([sys.executable, "takePicture.py", str(dishNum)])
        	rr.step_reverse(int(delay)/1000.0,int(stepsBack))
        	time.sleep(60*timeInMin)
        
	finally:
    	try:
    		setLights(RED_PIN3, 0)
    		setLights(BLUE_PIN3, 0)
    		setLights(GREEN_PIN3, 0)
    	GPIO.cleanup()
