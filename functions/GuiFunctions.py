import ctypes as ct
import numpy
from time import sleep
import os
serialNumber = ct.c_char_p('71874833')
serialNumberA = ct.c_char_p('71874833')
serialNumberB = ct.c_char_p('71854093')
#adds location of the dlls to the system path so that this program can run on any machine
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_location = dir_path + "\\dll"
os.environ['PATH'] = dll_location + os.pathsep + os.environ['PATH']
#import piezo controller dll
piezoDll = ct.CDLL("Thorlabs.MotionControl.Benchtop.Piezo.dll")
hundredPercent = 32767
channel1 = ct.c_short(1)
channel2 = ct.c_short(2)
channel3 = ct.c_short(3)

# Function: connect
# Purpose: initializes the connection to the Piezo controller puts all channels into closed loop control mode
# Parameters: None
# Returns: None, but prints either "successfully connected" or "error connecting: "
# with an error code to the console.
def connect(which="primary", centralize="all"):
    global serialNumber
    if which == "primary":
        serialNumber = serialNumberA
    elif which == "secondary":
        serialNumber = serialNumberB
    result = piezoDll.PBC_Open(serialNumber)
    if result != 0: print "error connecting: " + str(result)
    else: print "Successfully Connected"
    closeLoop(1)
    closeLoop(2)
    closeLoop(3)
    #zero(1)
    #zero(2)
    #zero(3)
    #print "Initializing, zeroing, and setting to mid position:"
    #for x in range (0,25):
        #wait = 24 - x
        #print "Time remaining: " + (str(wait)) + " seconds",
        #print "\r",
        #sleep(1)
    #print "\nComplete"
    sleep(1)
    if centralize == "xz":
        setPosition(10, 1)
        setPosition(10, 3)
    elif centralize == "all":
        center()

# Function: disconnect
# Purpose: disconnects the control from the computer so it no longer takes commands
# Parameters: None
# Returns: None, but prints "disconnect" to the console.
def disconnect():
    piezoDll.PBC_Disconnect(serialNumber)
    piezoDll.PBC_Close(serialNumber)
    #print "disconnect"

# Function: center
# Purpose: center all channels to mid range
# Parameteres: None
# Returns: None
def center():
    setPosition(10, 1)
    setPosition(10, 2)
    setPosition(10, 3)

# Function: stepUp
# Purpose: increase the position of one channel by a specified step distance
# Parameters: step: a float representing the distance in um to increase the position by
#           channel: number 1-n representing the channel to change
# Returns: None
def stepUp(step, channel):
    if step <.005: step = .005
    positionb = getPosition()[channel - 1]
    position = getPosition()[channel - 1] + step
    setPosition(position, channel)

# Function: stepDown
# Purpose: decrease the position of one channel by a specified step distance
# Parameters: step: a float representing the distance in um to decrease the position by
#           channel: number 1-n representing the channel to change
# Returns: None
def stepDown(step, channel):
    if step <.005: step = .005
    position = getPosition()[channel - 1] - step
    setPosition(position, channel)

# Function: openLoop
# Purpose: Set a specified channel to "Open Loop" mode.
# Parameters: The channel (int) from 1 to n.
# Returns: None
def openLoop(channel):
    #(serialno, channel, control mode 1==open, 2==closed)
    channelNum = ct.c_short(channel)
    piezoDll.PBC_SetPositionControlMode(serialNumber, channelNum, ct.c_short(1))

# Function: closedLoop
# Purpose: Set a specified channel to "Closed Loop" mode.
# Parameters: The channel (int) from 1 to n.
# Returns: None
def closeLoop(channel):
    #(serialno, channel, control mode 1==open, 2==closed)
    channelNum = ct.c_short(channel)
    piezoDll.PBC_SetPositionControlMode(serialNumber, channelNum, ct.c_short(2))

# Function: identify
# Purpose: Sends a command to the device/channel to make it identify itself (in
# the case of our piezo, flash the screen of the requested channel).
# Parameters: An integer representing the channel (1 to n).
# Returns: None
# Notes: This function has been tested and is working properly.
def identify(channel):
    #(serialno, channel)
    piezoDll.PBC_Identify(serialNumber, ct.c_short(channel))

# Function: setZero
# Purpose: Sets the voltage output of a specified channel to zero and defines
# the ensuing actuator position as zero.
# Parameters: The channel (int) from 1 to n.
# Returns: None.
# Notes: This function has been tested and is working properly.
def zero(channel):
    piezoDll.PBC_SetZero(serialNumber, ct.c_short(channel))

# Function: getPosition
# Purpose: Gets the position from the piezo controller when in closed loop mode.
# The result is undefined if not in closed loop mode.
# Parameters: None
# Returns: A vector of floats of positions - from 0 to 2, corresponding to
# channels 1 to 3.
def getPosition():
    positions = [0,0,0]
    positions[0] = calculatePosition_um(1)
    positions[1] = calculatePosition_um(2)
    positions[2] = calculatePosition_um(3)
    return positions

# Function: setPosition
# Purpose: sets the position of the specified channel to the specified position in micrometers
# Parameters: position_um (float, position in micrometers), channel (int, 1 to n).
# Returns: None
def setPosition(position_um, channel):
    if position_um < 0:
        position_um = 0
        print "error: position < 0"
    elif position_um > 20:
        print "Out of bounds error: position > 20"
    inputShort = calculateDistanceShort(position_um, channel)
    if inputShort > hundredPercent: inputShort = hundredPercent
    inputShort = ct.c_short(inputShort)
    piezoDll.PBC_SetPosition (serialNumber, ct.c_short(channel), inputShort)

# Function: calculateDistanceShort
# Purpose: calculates the needed input as a percentage of max travel as a short from 0 to 32767
# Parameters: position_um (float, position in micrometers), channel (int, 1 to n).
# Returns: An integer between 0 to 32767, representing the percentage of
# max travel (corresponds to 0% to 100%, respectively).
def calculateDistanceShort(position_um, channel):
    #set channel to channel currently in use
    channel = ct.c_short(channel)
    #gets the max distance of the actuator in 100nm
    maxTravel = ct.c_short(piezoDll.PBC_GetMaximumTravel(serialNumber, channel)).value
    #print maxTravel
    #convert position from um to 100nm
    position_100nm = 10 * position_um
    pecentageOfMax = position_100nm / float(maxTravel)
    inputShort = pecentageOfMax * hundredPercent
    return int(inputShort)

# Function: calculatePosition_um
# Purpose: Convert the value returned from the channel (which is a percentage)
# into its equivalent physical distance in micrometers (um).
# Parameters: An integer representing the channel (1 to n).
# Returns: A float, the value of the channel's current position in micrometers.
# Notes: This function has been tested and is working properly.
def calculatePosition_um(channel):
    channel = ct.c_short(channel)
    error = piezoDll.PBC_RequestActualPosition(serialNumber, channel)
    positionShort = piezoDll.PBC_GetPosition(serialNumber, channel)
    pyPosition = (ct.c_short(positionShort).value)
    maxTravel = ct.c_short(piezoDll.PBC_GetMaximumTravel(serialNumber, channel)).value/10
    percentOfMax = float(pyPosition) / float(hundredPercent)
    return percentOfMax * maxTravel
