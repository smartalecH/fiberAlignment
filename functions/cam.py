# File: cam.py
# Last modified: 3/7/2018

# Dependancies: Instrumental-lib by Mabuchi Lab
# Documentation located at http://instrumental-lib.readthedocs.io/en/stable/index.html
# Can be installed via pip or by cloning the github package, see the above site.

# import matplotlib to be able to display the captured image.
from instrumental import instrument
from matplotlib import pyplot
from instrumental.drivers.cameras import uc480

paramsets = uc480.list_instruments()
# Assuming only one camera device is connected, the camera we want to connect
# to will be the only one in the instrument list.
camera = instrument(paramsets[0])
a = camera.grab_image()
pyplot.imshow(a)
pyplot.show()
