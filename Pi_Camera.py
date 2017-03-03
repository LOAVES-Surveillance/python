from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)


#Camera configuration:
camera = PiCamera()
camera.resolution = (512, 384)
camera.framerate = 32
record_amount = 10
delay = 5


#Other Variables:
PIR = 16
timmer_count = 3
photo_number = 1
reset_time = record_amount
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)         
GPIO.setup(PIR, GPIO.IN)                         #Read output from PIR motion sensor
date_string = time.strftime('%m_%d_%Y')          #Date for time stamp
hour_string = time.strftime("%H:%M:%S")          #Hour and minuets for time stamp
mypath = '/home/pi/Documents/Raspberry_Projects/pics/' + date_string + '/'

if not os.path.isdir(mypath):
        os.makedirs(mypath)

# Main program:
if __name__ == '__main__':
        print "Starting up"
        while (timmer_count > 0):
               print (timmer_count)
               timmer_count -= 1
               time.sleep(1)
               

while True:
       i=GPIO.input(PIR)                       #set PIR as input
       if i==0:                                #When output from motion sensor is LOW
             print "No intruders around"
             time.sleep(delay)
             
       elif i==1:                              #When output from motion sensor is HIGH
             print "Intruder detected"
             my_file = (mypath +  str(hour_string) + '.h264')
             
             camera.start_recording(my_file)
             file2 = drive.CreateFile()
             

             print "Recording in progress"
             print "Will record for %s seconds." %(record_amount)
             
             while (record_amount >= 0):                #This will blink red to let you know it's
                    record_amount -= 1                  #currently recording
                    time.sleep(1)
                    
             camera.stop_recording()
             time.sleep(1)
             
             file2.SetContentFile(my_file)             #Set the recorded file to be uploaded   
             file2.Upload()                            #upload file to google drive
                     
             hour_string = time.strftime("%H:%M:%S")   #reset time so we don't overwrite exisiting files
             record_amount = reset_time                #reset the record time so it doesn't stay at
                                                       #0 seconds and keep looping 1 sec videos


#used for taking pictures
'''
while True:
       i=GPIO.input(PIR)                  #set PIR as input
       if i==0:                           #When output from motion sensor is LOW
             print "No intruders around" 
             time.sleep(delay)
             
       elif i==1:                         #When output from motion sensor is HIGH
             print "Intruder detected" 
             camera.capture('/home/pi/Documents/Raspberry_Projects/pics/image_' + str(photo_number) + '.jpg')
             print "Caught you on candid camera!"
             time.sleep(delay)
             photo_number += 1 
'''
