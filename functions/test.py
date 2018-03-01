
import ctypes as ct
import numpy
from time import sleep
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_location = dir_path + "\\dll"
os.environ['PATH'] = dll_location + os.pathsep + os.environ['PATH']
#import piezo controller dll
uc480dotnet = ct.CDLL("uc480.dll")
a = uc480dotnet.Camera.Init()
