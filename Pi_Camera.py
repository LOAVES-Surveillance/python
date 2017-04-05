from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Camera configuration:
camera = PiCamera()
camera.resolution = (512, 384)
camera.framerate = 32
record_amount = 10
delay = 5


#Other Variables:
PIR = 16
timmer_count = 10
photo_number = 1
reset_time = record_amount
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)                             #Use the regular pin identifiers. 
GPIO.setup(PIR, GPIO.IN)                                  #Read output from PIR motion sensor
date_string = time.strftime('%m_%d_%Y')           #Date for time stamp
hour_string = time.strftime("%H:%M:%S")           #Time used for file naming
standard_hour_string = time.strftime("%r")          #Time used for video time stamp overlay
mypath = '/home/pi/LOAVES/pics/' + date_string + '/'

if not os.path.isdir(mypath):
        os.makedirs(mypath)

print "Starting up"               
while (timmer_count > 0):                        # Delay that gives the pi sufficient 
        print (timmer_count)                     # time to boot up before trying to 
        time.sleep(1)                          # connect to the network
        timmer_count -= 1

gauth = GoogleAuth()                             # Google drive API

gauth.LoadCredentialsFile("mycreds.txt")         # Try to load saved client credentials
if gauth.credentials is None:                    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
    
elif gauth.access_token_expired:                 # Refresh them if expired
    gauth.Refresh()
    
else:                                            # Initialize the saved creds
    gauth.Authorize()
    
gauth.SaveCredentialsFile("mycreds.txt")         # Save the current credentials to a file
drive = GoogleDrive(gauth)                       # Set drive location using .json file




# Main program:
try:
	if __name__ == '__main__':
		
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
					record_amount -= 1                  			#currently recording
					time.sleep(1)
					standard_hour_string = time.strftime("%r")
					camera.annotate_text = standard_hour_string
					
				camera.stop_recording()
				time.sleep(.5)
			 
				print "Pushing saved video to Google Drive"        
				file2.SetContentFile(my_file)             #Set the recorded file to be uploaded   
				file2.Upload()                            #upload file to google drive
					 
				hour_string = time.strftime("%H:%M:%S")   #reset time so we don't overwrite exisiting files
				standard_hour_string = time.strftime("%r")
			 
				record_amount = reset_time                #reset the record time so it doesn't stay at
				time.sleep(.5)                            #0 seconds and keep looping 1 sec videos
				print "Done!\n\n"
				 
except KeyboardInterrupt:
        print "Program Terminated \n"

except:
	print "Other Error Occurred"
        
finally:
        GPIO.cleanup()
