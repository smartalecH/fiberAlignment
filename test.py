
import ctypes
mydll = ctypes.CDLL("C:\\Program Files (x86)\Thorlabs\Kinesis\Thorlabs.MotionControl.Benchtop.Piezo.dll")
mydll.TLI_BuildDeviceList()
result = mydll.TLI_GetDeviceListSize()
print result
