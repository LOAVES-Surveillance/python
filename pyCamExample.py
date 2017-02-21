from picamera import PiCamera, Color
from time import sleep
import datetime
import time

camera = PiCamera()

camera.rotation = 180

#camera.resolution = (2592, 1944) #these 2 lines change resolution up from default resolution of pi's monitor res
#camera.framerate = 15

camera.start_preview(alpha=250) #alpha is transparency between 0-255
camera.start_recording('/home/pi/Desktop/video.h264')
#sleep(5)

##for effect in camera.IMAGE_EFFECTS:
##    camera.image_effect = effect
##    camera.annotate_text = "Effect: %s" %effect
##    sleep(3)

for i in range(10):
        aText = 'Timestamp: {:%m/%d/%Y %H:%M:%S}'.format(datetime.datetime.now())
        ##    camera.annotate_background = Color('blue')
        ##    camera.annotate_foreground = Color('green')
            camera.annotate_text_size = 50
                camera.annotate_text = aText
                    sleep(1)
                        
                        #camera.capture('/home/pi/Desktop/image.jpg') #takes picture
                        camera.stop_recording()
                        camera.stop_preview()
