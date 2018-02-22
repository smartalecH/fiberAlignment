import ctypes as ct
import numpy
import time


piezoDll = ct.CDLL("Thorlabs.MotionControl.Benchtop.Piezo.dll")
deviceManagerDll = ct.CDLL("Thorlabs.MotionControl.DeviceManager.dll")
serialNumber = ct.c_char_p('71874833')
channel1 = ct.c_short(1)
channel2 = ct.c_short(2)
channel3 = ct.c_short(3)
typeId = 71
piezoDll.TLI_BuildDeviceList()
deviceListSize = piezoDll.TLI_GetDeviceListSize()
print deviceListSize
if deviceListSize == 0: quit

# Models the TLI_DeviceInfo Struct, see Thorlabs.MotionControl.C_API
class TLI_DeviceInfo(ct.Structure):
    _fields_ = [
        ("id", ct.c_uint32),
        ("description", ct.c_char * 65),
        ("serialNo", ct.c_char * 9),
        ("PID", ct.c_uint32),
        ("isKnownType", ct.c_bool),
        ("motorType", ct.c_uint64),
        ("isPiezoDevice", ct.c_bool),
        ("isLaser", ct.c_bool),
        ("isCustomType", ct.c_bool),
        ("isRack", ct.c_bool),
        ("maxChannels", ct.c_short)
        ]

test = TLI_DeviceInfo()
print test.description
print serialNumber.value

# Test to see if we can communicate with the BPC303 device. Function returns
# 1 if successful, 0 if not. Gets device info by serial number.
error  = -1
error = piezoDll.TLI_GetDeviceInfo(serialNumber, ct.byref(test))

# Print out everything now stored in the TLI_DeviceInfo class
print test
print "error: " + str(error) + " (1 = successful, 0 = failed)"
print "id: " + str(test.id)
print "description: " + str(test.description)
print "serialNumber: " + str(test.serialNo)
print "PID: " + str(hex(test.PID))
print "isKnownType: " + str(test.isKnownType)
print "MotorType: " + str(hex(test.motorType))
print "isPiezoDevice: " + str(test.isPiezoDevice)
print "isLaser: " + str(test.isLaser)
print "isCustomType: " + str(test.isCustomType)
print "isRack: " + str(test.isRack)
print "maxChannels: " + str(test.maxChannels)

#open connection to the controler 0 == success
isOpened = piezoDll.PBC_Open(serialNumber)
print "connection opened: " + str(isOpened)
piezoDll.PBC_CheckConnection.restype = ct.c_bool
isConnected = piezoDll.PBC_CheckConnection(serialNumber)
print "is device connected? " + str(isConnected)
ch1ControlMode = piezoDll.PBC_GetPositionControlMode(serialNumber, channel1)
print "ch1ControlMode: " + str(ch1ControlMode) + " (1 = open loop; 2 = Closed loop)"
piezoDll.PBC_SetPositionControlMode(serialNumber, channel1, 1)
ch1ControlMode = piezoDll.PBC_GetPositionControlMode(serialNumber, ct.)
piezoDll.PBC_SetOutputVoltage(serialNumber, channel1, ct.c_short(0))
piezoDll.PBC_Disconnect(serialNumber)
piezoDll.PBC_Close(serialNumber)

def changeLoop(channel, newPosition):
    serialNumber = ct.c_char_p('71874833')
    piezoDll = ct.CDLL("Thorlabs.MotionControl.Benchtop.Piezo.dll")
    piezoDll.PBC_SetPositionControlMode(serialNumber, ct.c_short(channel), ct.c_short(newPosition))

def calculateDistanceShort(position_um, channel):
    piezoDll = ct.CDLL("Thorlabs.MotionControl.Benchtop.Piezo.dll")
    serialNumber = ct.c_char_p('71874833')
    input100Percent = 32767
    #set channel to channel currently in use
    channel = ct.c_short(channel)
    #gets the max distance of the actuator in 100nm
    maxTravel = piezoDll.PBC_GetMaxTravel(serialNumber, channel)
    #convert position from um to 100nm
    position_100nm = 10 * position_um
    pecentageOfMax = position_100nm / maxTravel
    inputShort = pecentageOfMax * input100Percent
    return inputShort

def calculatePosition_um(channel):
    piezoDll = ct.CDLL("Thorlabs.MotionControl.Benchtop.Piezo.dll")
    serialNumber = ct.c_char_p('71874833')
    input100Percent = 32767
    channel = ct.c_short(channel)
    positionShort = piezoDll.PBC_GetPosition(serialNumber, channel)
    maxTravel = piezoDll.PBC_GetMaxTravel(serialNumber, channel)
    percentOfMax = positionShort / input100Percent
    position_100nm = maxTravel * percentOfMax
    position_um = position_100nm / 10
    return position_um
