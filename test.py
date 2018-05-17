from functions import slmpy
import numpy as np
import time
from PIL import Image
slm = slmpy.SLMdisplay(isImageLock = False)
slm = slmpy.SLMdisplay(monitor = 1)
resX, resY = slm.getSize()
X,Y = np.meshgrid(np.linspace(0,resX,resX),np.linspace(0,resY,resY))
#testIMG = np.round((2**8-1)*(0.5+0.5*(-1)*np.sin(2*np.pi*X/50))).astype('uint8')
im = Image.open('Happy_face.jpg')
testIMG = np.array(im).astype('uint8')
#print len(testIMG)
#print len(testIMG[0])
print testIMG.shape
print testIMG
slm.updateArray(testIMG)
time.sleep(20)
slm.close()
