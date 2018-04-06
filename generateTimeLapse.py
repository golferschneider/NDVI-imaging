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

import mencoder
import os
testName = raw_input("what test did you want to time lapse?" )
dishNum = raw_input("what dish did you want to timelapse? ")
user_fps = raw_input("how many pictures per second in timeLapse? ")

realDir = os.getcwd() + "/" + testName + "/" + dishNum

lsName = directory + ".txt"

call(["cd", "realDir"])
call(["ls","*.jpg",">","lsName")
call(["mencoder","-nosound","-ovc","lavc","-lavcopts","vcodec=mpeg4:aspect=16/9:vbitrate=8000000","-vf","scale=1920:1080","-o","timelapse.avi","-mf","type=jpeg:fps=user_fps","mf://@lsName"])

