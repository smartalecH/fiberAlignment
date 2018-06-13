from functions import slmpy
import numpy as np
import time
#from PIL import Image

<<<<<<< HEAD
def displayVal(seconds, frequency, X, Y):
=======
def displayVal(slm, seconds, frequency):
>>>>>>> 87ebb676e88bfbd6fde319501412ce7ca92ba147
    start = time.time()
    elapsed = 0
    x = np.empty([600, 800, 3])
    while elapsed < seconds:
        elapsed = time.time() - start
        #testIMG = np.round((2**8-1)*(0.5+0.5*(-1)*np.sin(2*np.pi*X/50))*elapsed).astype('uint8')
        val = 127.5 * np.sin(2 * np.pi * frequency * elapsed) + 127.5
        x.fill(val)
        screen = np.array(x).astype('uint8')
        #slm.updateArray(testIMG)
        slm.updateArray(screen)


<<<<<<< HEAD
slm = slmpy.SLMdisplay(isImageLock = False)
slm = slmpy.SLMdisplay(monitor = 1)
=======
slm = slmpy.SLMdisplay(monitor = 0)
#slm = slmpy.SLMdisplay(monitor = 0)
>>>>>>> 87ebb676e88bfbd6fde319501412ce7ca92ba147
resX, resY = slm.getSize()
X,Y = np.meshgrid(np.linspace(0,resX,resX),np.linspace(0,resY,resY))
#t = np.linspace(0,10,20000)
#t = 2 * np.pi * 20 * t
#display = np.sin(t)

<<<<<<< HEAD
displayVal(240, 8, X, Y)
=======
displayVal(slm, 5, 1)
>>>>>>> 87ebb676e88bfbd6fde319501412ce7ca92ba147

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
