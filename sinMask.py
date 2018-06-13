from functions import slmpy
import numpy as np
import time
from PIL import Image

def displayVal(seconds, frequency, X, Y):
    start = time.time()
    elapsed = 0
    x = np.empty([600L, 800L, 3L])
    while elapsed < seconds:
        elapsed = time.time() - start
        #testIMG = np.round((2**8-1)*(0.5+0.5*(-1)*np.sin(2*np.pi*X/50))*elapsed).astype('uint8')
        val = 127.5 * np.sin(2 * np.pi * frequency * elapsed) + 127.5
        x.fill(val)
        screen = np.array(x).astype('uint8')
        #slm.updateArray(testIMG)
        slm.updateArray(screen)


slm = slmpy.SLMdisplay(isImageLock = False)
slm = slmpy.SLMdisplay(monitor = 1)
resX, resY = slm.getSize()
X,Y = np.meshgrid(np.linspace(0,resX,resX),np.linspace(0,resY,resY))
#t = np.linspace(0,10,20000)
#t = 2 * np.pi * 20 * t
#display = np.sin(t)

displayVal(240, 8, X, Y)

#im = Image.open('Happy_face.jpg')
#testIMG = np.array(im).astype('uint8')
#print len(testIMG)
#print len(testIMG[0])
#print testIMG.shape
#print testIMG
#print "gotcha"
#slm.updateArray(testIMG)
#time.sleep(20)
slm.close()
