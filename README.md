# NDVI-imaging
For raspberry pi to power Led light strip, usb camera and stepper motor.
DISCLAMER: this was my first python project so please have mercy on me!

Hardware: 
  - Raspberry pi 2 B
  - RasPiRobot v3 board for controlling the stepper motor
  - I beleive we used a Nema 23 stepper motor

*runImaging.py*  
  This controls the lights, stepper motor, and sets up all directories to hold the image files. 
  -> This makes a call to "takePicture.py"
 
 *takePicture*  
   Takes picture and does all NDVI computations saving a greyScale and the falseColor to the directory sent into the takePic method.
   Current problem: the naming convention when saving images might not be optimal, not intuitive to tell when the image was taken by 
        looking at image name.
   
*generateTimeLapse*  
  Creates a time lapse image of all the images in a folder. Creates a cool video to show the growth or deterioration of a plant!
