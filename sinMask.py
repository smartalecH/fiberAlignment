from functions import slmpy
import numpy as np
import time
#from PIL import Image

def displayVal(slm, seconds, frequency):
    start = time.time()
    elapsed = 0
    x = np.empty([600, 800, 3])
    while elapsed < seconds:
        elapsed = time.time() - start
        val = 127.5 * np.sin(2 * np.pi * frequency * elapsed) + 127.5
        x.fill(val)
        screen = np.array(x).astype('uint8')
        slm.updateArray(screen)


slm = slmpy.SLMdisplay(monitor = 0)
#slm = slmpy.SLMdisplay(monitor = 0)
resX, resY = slm.getSize()
X,Y = np.meshgrid(np.linspace(0,resX,resX),np.linspace(0,resY,resY))
#testIMG = np.round((2**8-1)*(0.5+0.5*(-1)*np.sin(2*np.pi*X/50))).astype('uint8')
#t = np.linspace(0,10,20000)
#t = 2 * np.pi * 20 * t
#display = np.sin(t)

displayVal(slm, 5, 1)

#im = Image.open('Happy_face.jpg')
#testIMG = np.array(im).astype('uint8')
#print len(testIMG)
#print len(testIMG[0])
#print testIMG.shape
#print testIMG
#print "gotcha"
#slm.updateArray(testIMG)
time.sleep(2)
slm.close()
