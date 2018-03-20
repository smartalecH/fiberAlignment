# File: cam.py
# Last modified: 3/7/2018

# Dependancies: Instrumental-lib by Mabuchi Lab
# Documentation located at http://instrumental-lib.readthedocs.io/en/stable/index.html
# Can be installed via pip or by cloning the github package, see the above site.

# import matplotlib to be able to display the captured image.
from instrumental import instrument
from matplotlib import pyplot
from instrumental.drivers.cameras import uc480
import cv2
import time
paramsets = uc480.list_instruments()
# Assuming only one camera device is connected, the camera we want to connect
# to will be the only one in the instrument list.

camera = instrument(paramsets[0])

#this loop is suposed to update the image live but
#right now it only updates when the image is closed needs fixed

camera.start_live_video()
while camera.wait_for_frame():
    frame = camera.latest_frame()
    cv2.imshow('frame',frame)

    cv2.waitKey(100)
    if cv2.getWindowProperty('frame',cv2.WND_PROP_VISIBLE) < 1: break
#I down loaded the source files for instrumental from git hum they are at C:\Users\ecestudent\Downloads\Instrumental-master
cv2.destroyAllWindows()
