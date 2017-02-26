from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time


camera = PiCamera()
PIR = 16
timmer_count = 3
photo_number = 1
video_number = 1
record_amount = 5
delay = 5
reset_time = record_amount

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)         
GPIO.setup(PIR, GPIO.IN)         #Read output from PIR motion sensor
          


# Main program:
if __name__ == '__main__':
        print "Starting up"
        camera.start_preview(alpha=250)
        while (timmer_count > 0):
               print (timmer_count)
               timmer_count -= 1
               time.sleep(1)


while True:
       camera.stop_preview()
       i=GPIO.input(PIR)                       #set PIR as input
       if i==0:                                #When output from motion sensor is LOW
             print "No intruders around"
             time.sleep(delay)
             
       elif i==1:                              #When output from motion sensor is HIGH
             print "Intruder detected"
             camera.start_recording('/home/pi/Documents/Raspberry_Projects/pics/vid_' + str(video_number) + '.h264')
             
             print "Recording in progress"
             print "Will record for %s seconds." %(record_amount)
             
             while (record_amount >=0):         #This will blink red to let you know it's
                    record_amount -= 1          #currently recording
                    time.sleep(1)
             
             camera.stop_recording()
             video_number += 1
             record_amount = reset_time        #reset the record time so it doesn't stay at
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
