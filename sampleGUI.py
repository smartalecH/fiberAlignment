# File: sampleGUI.py
# Authors: Sequoia Ploeg, Robert
# Last modified: 2/20/2018
# Purpose: Provide an graphical interface with the BPC303 Piezo device.

import Tkinter
from functions import GuiFunctions as gf
from time import sleep
from functions import daq
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# The GUI class
class simpleGUI_tk(Tkinter.Tk):

    def __init__(self, parent):
        gf.connect()
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        #self.running = True

    def initialize(self):
        self.grid()
    # CHANNEL LABELS
        # Channel 1 label
        self.lblCh1 = Tkinter.Label(self, text="Ch 1:")
        self.lblCh1.grid(column=0, row=0, rowspan=2, sticky='EW')
        # Channel 2 Label
        self.lblCh2 = Tkinter.Label(self, text="Ch 2:")
        self.lblCh2.grid(column=0, row=2, rowspan=2, sticky='EW')
        # Channel 3 Label
        self.lblCh3 = Tkinter.Label(self, text="Ch 3:")
        self.lblCh3.grid(column=0, row=4, rowspan=2, sticky='EW')
    # IDENT BUTTONS
        # Chanel 1 IDENT
        self.btnId1 = Tkinter.Button(self, text="IDENT", bg="#f4a641", command=lambda: gf.identify(1))
        self.btnId1.grid(column=1, row=0, rowspan=2, sticky='EW')
        # Chanel 2 IDENT
        self.btnId2 = Tkinter.Button(self, text="IDENT", bg="#f4a641", command=lambda: gf.identify(2))
        self.btnId2.grid(column=1, row=2, rowspan=2, sticky='EW')
        # Chanel 3 IDENT
        self.btnId3 = Tkinter.Button(self, text="IDENT", bg="#f4a641", command=lambda: gf.identify(3))
        self.btnId3.grid(column=1, row=4, rowspan=2, sticky='EW')
    # POSITION DISPLAY
        # Chanel 1 Position
        self.frmPos1 = Tkinter.Frame(self)
        self.frmPos1.grid(column=2, row=0, rowspan=2, sticky='EW')
        self.grpPos1 = Tkinter.LabelFrame(self.frmPos1, text="Position (um)", padx=5, pady=5)
        self.grpPos1.grid(column=0, row=0, sticky='EW')
        self.txtPos1 = Tkinter.Entry(self.grpPos1, text="this")
        self.txtPos1.grid(column=0, row=0, sticky='EW')
        # Chanel 2 Position
        self.frmPos2 = Tkinter.Frame(self)
        self.frmPos2.grid(column=2, row=2, rowspan=2, sticky='EW')
        self.grpPos2 = Tkinter.LabelFrame(self.frmPos2, text="Position (um)", padx=5, pady=5)
        self.grpPos2.grid(column=0, row=0, sticky='EW')
        self.txtPos2 = Tkinter.Entry(self.grpPos2)
        self.txtPos2.grid(column=0, row=0, sticky='EW')
        # Chanel 3 Position
        self.frmPos3 = Tkinter.Frame(self)
        self.frmPos3.grid(column=2, row=4, rowspan=2, sticky='EW')
        self.grpPos3 = Tkinter.LabelFrame(self.frmPos3, text="Position (um)", padx=5, pady=5)
        self.grpPos3.grid(column=0, row=0, sticky='EW')
        self.txtPos3 = Tkinter.Entry(self.grpPos3)
        self.txtPos3.grid(column=0, row=0, sticky='EW')
    # LOOP MODE BUTTONS
        # Chanel 1 Mode
        self.btnOLoop1 = Tkinter.Button(self, text="Open Loop", bg="gray", command=lambda: openMode(1)) #gf.openLoop1)
        self.btnOLoop1.grid(column=3, row=0, sticky='SEW')
        self.btnCLoop1 = Tkinter.Button(self, text="Closed Loop", bg="#1cb251", command=lambda: closeMode(1))  #gf.closeLoop1)
        self.btnCLoop1.grid(column=3, row=1, sticky='NEW')
        # Chanel 2 Mode
        self.btnOLoop2 = Tkinter.Button(self, text="Open Loop", bg="gray", command=lambda: openMode(2))
        self.btnOLoop2.grid(column=3, row=2, sticky='SEW')
        self.btnCLoop2 = Tkinter.Button(self, text="Closed Loop", bg="#1cb251", command=lambda: closeMode(2))
        self.btnCLoop2.grid(column=3, row=3, sticky='NEW')
        # Chanel 3 Mode
        self.btnOLoop3 = Tkinter.Button(self, text="Open Loop", bg="gray", command=lambda: openMode(3))
        self.btnOLoop3.grid(column=3, row=4, sticky='SEW')
        self.btnCLoop3 = Tkinter.Button(self, text="Closed Loop", bg="#1cb251", command=lambda: closeMode(3))
        self.btnCLoop3.grid(column=3, row=5, sticky='NEW')
    # TARGET VALUE TEXT BOX
        # Chanel 1 Target
        self.lblInfo1 = Tkinter.Label(self, text="Range 0.0 to 20 um")
        self.lblInfo1.grid(column=4, row=0, sticky='SEW')
        self.txtTarget1 = Tkinter.Entry(self)
        self.txtTarget1.bind("<Return>", setTargetEvent1)
        self.txtTarget1.grid(column=4, row=1, sticky='NEW')
        # Chanel 2 Target
        self.lblInfo2 = Tkinter.Label(self, text="Range 0.0 to 20 um")
        self.lblInfo2.grid(column=4, row=2, sticky='SEW')
        self.txtTarget2 = Tkinter.Entry(self)
        self.txtTarget2.bind("<Return>", setTargetEvent2)
        self.txtTarget2.grid(column=4, row=3, sticky='NEW')
        # Chanel 3 Target
        self.lblInfo3 = Tkinter.Label(self, text="Range 0.0 to 20 um")
        self.lblInfo3.grid(column=4, row=4, sticky='SEW')
        self.txtTarget3 = Tkinter.Entry(self)
        self.txtTarget3.bind("<Return>", setTargetEvent3)
        self.txtTarget3.grid(column=4, row=5, sticky='NEW')
    # SET TARGET BUTTON
        # Chanel 1 Set Button
        self.btnSetTarget1 = Tkinter.Button(self, text="SET TARGET", bg="#4286f4", command=setTarget1)
        self.btnSetTarget1.grid(column=5, row=0, rowspan=2, sticky='EW')
        # Chanel 2 Set Button
        self.btnSetTarget2 = Tkinter.Button(self, text="SET TARGET", bg="#4286f4", command=setTarget2)
        self.btnSetTarget2.grid(column=5, row=2, rowspan=2, sticky='EW')
        # Chanel 3 Set Button
        self.btnSetTarget3 = Tkinter.Button(self, text="SET TARGET", bg="#4286f4", command=setTarget3)
        self.btnSetTarget3.grid(column=5, row=4, rowspan=2, sticky='EW')
    # STEP SIZE LABEL
        # Chanel 1 Label
        self.lblStepSize1 = Tkinter.Label(self, text="STEP\nSIZE")
        self.lblStepSize1.grid(column=6, row=0, rowspan=2, sticky='EW')
        # Chanel 2 Label
        self.lblStepSize2 = Tkinter.Label(self, text="STEP\nSIZE")
        self.lblStepSize2.grid(column=6, row=2, rowspan=2, sticky='EW')
        # Chanel 3 Label
        self.lblStepSize3 = Tkinter.Label(self, text="STEP\nSIZE")
        self.lblStepSize3.grid(column=6, row=4, rowspan=2, sticky='EW')
    # STEP VALUE TEXT BOX
        # Chanel 1 Step
        self.lblStepInfo1 = Tkinter.Label(self, text="Range 0.005 to 20 um")
        self.lblStepInfo1.grid(column=7, row=0, sticky='SEW')
        self.txtStepVal1 = Tkinter.Spinbox(self, from_=.005, to=7.5, increment=.005)
        self.txtStepVal1.grid(column=7, row=1, sticky='NEW')
        # Chanel 2 Step
        self.lblStepInfo2 = Tkinter.Label(self, text="Range 0.005 to 20 um")
        self.lblStepInfo2.grid(column=7, row=2, sticky='SEW')
        self.txtStepVal2 = Tkinter.Spinbox(self, from_=.005, to=7.5, increment=.005)
        self.txtStepVal2.grid(column=7, row=3, sticky='NEW')
        # Chanel 3 Step
        self.lblStepInfo3 = Tkinter.Label(self, text="Range 0.005 to 20 um")
        self.lblStepInfo3.grid(column=7, row=4, sticky='SEW')
        self.txtStepVal3 = Tkinter.Spinbox(self, from_=.005, to=7.5, increment=.005)
        self.txtStepVal3.grid(column=7, row=5, sticky='NEW')
    # STEP BUTTONS
        # Chanel 1 Mode
        self.btnStepUp1 = Tkinter.Button(self, text="UP", bg="#1cb251", command = lambda: up(self.txtStepVal1.get(), 1))
        self.btnStepUp1.grid(column=8, row=0, sticky='SEW')
        self.btnStepDown1 = Tkinter.Button(self, text="DOWN", bg="#d83e3e", command = lambda: down(self.txtStepVal1.get(), 1))
        self.btnStepDown1.grid(column=8, row=1, sticky='NEW')
        # Chanel 2 Mode
        self.btnStepUp2 = Tkinter.Button(self, text="UP", bg="#1cb251", command = lambda: up(self.txtStepVal2.get(), 2))
        self.btnStepUp2.grid(column=8, row=2, sticky='SEW')
        self.btnStepDown2 = Tkinter.Button(self, text="DOWN", bg="#d83e3e", command = lambda: down(self.txtStepVal2.get(), 2))
        self.btnStepDown2.grid(column=8, row=3, sticky='NEW')
        # Chanel 3 Mode
        self.btnStepUp3 = Tkinter.Button(self, text="UP", bg="#1cb251", command = lambda: up(self.txtStepVal3.get(), 3))
        self.btnStepUp3.grid(column=8, row=4, sticky='SEW')
        self.btnStepDown3 = Tkinter.Button(self, text="DOWN", bg="#d83e3e", command = lambda: down(self.txtStepVal3.get(), 3))
        self.btnStepDown3.grid(column=8, row=5, sticky='NEW')
    # ZERO BUTTONS
        # Chanel 1 Zeroes
        self.btnZero1 = Tkinter.Button(self, text="Zero", command= lambda: zero(1))
        self.btnZero1.grid(column=9, row=0, sticky='SEW')
        self.btnZeroed1 = Tkinter.Button(self, text="Zeroed", bg="#1cb251", state="disabled") #bg="gray"
        self.btnZeroed1.grid(column=9, row=1, sticky='NEW')
        # Chanel 2 Zeroes
        self.btnZero2 = Tkinter.Button(self, text="Zero", command= lambda: zero(2))
        self.btnZero2.grid(column=9, row=2, sticky='SEW')
        self.btnZeroed2 = Tkinter.Button(self, text="Zeroed", bg="#1cb251", state="disabled") #bg="gray"
        self.btnZeroed2.grid(column=9, row=3, sticky='NEW')
        # Chanel 3 Zeroes
        self.btnZero3 = Tkinter.Button(self, text="Zero", command= lambda: zero(3))
        self.btnZero3.grid(column=9, row=4, sticky='SEW')
        self.btnZeroed3 = Tkinter.Button(self, text="Zeroed", bg="#1cb251", state="disabled") #bg="gray"
        self.btnZeroed3.grid(column=9, row=5, sticky='NEW')
    # STATUS BAR
        self.statusLbl = Tkinter.Label(self, text="STATUS:")
        self.statusLbl.grid(column=1, row=6, sticky='W')
        self.status = Tkinter.Label(self, text="READY")
        self.status.grid(column=2, row=6, sticky='EW')
    # GRAPH
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        #self.ani = animation.FuncAnimation(self.fig, animate, interval=20)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(column=10, row=0, rowspan=7, sticky='EW')
# Function: on_closing
# Purpose: This is invoked when the window is closed to end the connection with the controller
# Parameters: None
# Returns: None
# Notes: This function is working properly.
def on_closing():
    gf.disconnect()
    app.destroy()
    print "NOTE: \nUntil a bug fix is found, please use the key combination \"Ctrl + C\" to terminate the program.\n"

# Function: openMode
# Purpose: Change the control mode of a given channel to Open Loop
# Parameters: channel (int) from 1 to 3; representing channels one through three.
# Returns: None
# Notes: This function has been tested and is working properly.
def openMode(channel):
    gf.openLoop(channel)
    # Change calling button's color to show what mode the piezo controller is in.
    # #1cb251 is a darkish green
    if channel == 1:
        app.btnOLoop1.config(bg="#1cb251")
        app.btnCLoop1.config(bg="gray")
    elif channel == 2:
        app.btnOLoop2.config(bg="#1cb251")
        app.btnCLoop2.config(bg="gray")
    elif channel == 3:
        app.btnOLoop3.config(bg="#1cb251")
        app.btnCLoop3.config(bg="gray")

# Function: closeMode
# Purpose: Change the control mode of a given channel to Open Loop
# Parameters: channel (int) from 1 to 3; representing channels one through three.
# Returns: None
# Notes: This function has been tested and is working properly.
def closeMode(channel):
    gf.closeLoop(channel)
    # Change calling button's color to show what mode the piezo controller is in.
    # #1cb251 is a darkish green
    if channel == 1:
        app.btnOLoop1.config(bg="gray")
        app.btnCLoop1.config(bg="#1cb251")
    elif channel == 2:
        app.btnOLoop2.config(bg="gray")
        app.btnCLoop2.config(bg="#1cb251")
    elif channel == 3:
        app.btnOLoop3.config(bg="gray")
        app.btnCLoop3.config(bg="#1cb251")

# Function: up
# Purpose: Increment the position of a given channel by a certain step amount,
# given in micrometers (um).
# Parameters: step (float) in micrometers, channel (int) from 1 to n.
# Returns: None
# Notes: This function has been tested and properly calls gf.stepUp
def up(step, channel):
    step = float(step)
    gf.stepUp(step, channel)

# Function: down
# Purpose: Decrement the position of a given channel by a certain step amount,
# given in micrometers (um).
# Parameters: step (float) in micrometers, channel (int) from 1 to n.
# Returns: None
# Notes: This function has been tested and properly calls gf.stepDown
def down(step, channel):
    step = float(step)
    gf.stepDown(step, channel)

# Function: zero
# Purpose: Sets the voltage output of a specified channel to zero and defines
# the ensuing actuator position as zero. Also changes the color of the 'Zeroed'
# indicator.
# Parameters: The channel (int) from 1 to n.
# Returns: None
# Notes: This function has been tested and works properly.
def zero(channel):
    gf.zero(channel)
    # Change 'Zeroed' indicator color
    if channel == 1:
        app.btnZeroed1.config(bg="#1cb251")
    elif (channel == 2):
        app.btnZeroed2.config(bg="#1cb251")
    elif (channel == 3):
        app.btnZeroed3.config(bg="#1cb251")

# Function: updatePosition
# Purpose: Get the position from the piezo controller and update the 'position'
# fields for each channel on the GUI.
# Parameters: None
# Returns: None
# Notes: This function has been tested and is working properly.
def updatePosition():
    position_um = gf.getPosition()
    # The round function is rounding to the nearest thousandth.
    app.txtPos1.delete(0,Tkinter.END)
    app.txtPos1.insert(0,str(round(position_um[0],3)))
    app.txtPos2.delete(0,Tkinter.END)
    app.txtPos2.insert(0,str(round(position_um[1],3)))
    app.txtPos3.delete(0,Tkinter.END)
    app.txtPos3.insert(0,str(round(position_um[2],3)))
    #print position_um[0]
    app.after(200, updatePosition)

# Function: animate
# Purpose: Update the voltage plot on the right side of the GUI.
# Parameters: an automatic i (do not pass animate any parameters!)
# Returns: None
def animate(i):
    # Get x and y data.
    x = np.array(np.linspace(0,100,100))
    y = np.array(daq.get100data()) * 1000
    # Get the average value
    avg = np.mean(y) / 43
    z = np.full((100,1), avg)
    # Clear the figure, and plot the new data
    app.ax1.cla()
    # The plot:
    lim = 100 #avg * 1.5
    app.ax1.axis([0,100,0,lim])
    app.ax1.plot(x,y,'r-',x,z,'b-')
    app.ax1.set_ylabel('Voltage (mv)')
    app.ax1.set_xlabel('Measurement #')
    app.ax1.set_title("DAQ Real-Time Measurements")
    app.ax1.legend(['Measured voltage','Average = ' + str('{:.2f}'.format(avg)) + ' %'], loc='upper left', bbox_to_anchor=(0.5,1))

# Function: setTarget1/2/3
# Purpose: gets the position inputted into the "target" text box and sets the motor's position.
# Parameters: None
# Returns: None
def setTarget1():
    position = float(app.txtTarget1.get())
    gf.setPosition(position, 1)
    app.txtTarget1.delete(0,Tkinter.END)
    app.txtTarget1.insert(0,"")
def setTarget2():
    position = float(app.txtTarget2.get())
    gf.setPosition(position, 2)
    app.txtTarget2.delete(0,Tkinter.END)
    app.txtTarget2.insert(0,"")
def setTarget3():
    position = float(app.txtTarget3.get())
    gf.setPosition(position, 3)
    app.txtTarget3.delete(0,Tkinter.END)
    app.txtTarget3.insert(0,"")

# Function: setTargetEvent1/2/3
# Purpose: Allows buttons and entry boxes to be bound to a key command. In this case,
# when the enter key is pressed while one of the setTarget text boxes is active,
# it will call the setTarget functions. This way you can type a value and press
# enter rather than having to click the "Set Position" button.
# Parameters: An event argument, generated by the .bind function.
# Returns: None
def setTargetEvent1(event):
    setTarget1()
def setTargetEvent2(event):
    setTarget2()
def setTargetEvent3(event):
    setTarget3()

def setStatus(code):
    if code == 0:
        app.status.config(text="READY ")
    if code == 1:
        app.status.config(text="WAIT")

# -----------------MAIN---------------------
if __name__ == "__main__":
    app = simpleGUI_tk(None)
    app.title('THORLABS BPC 303 Piezo Controller')
    # This calls on_closing when the window is closed
    app.protocol("WM_DELETE_WINDOW", on_closing)
    # Update the position text boxes
    updatePosition()
    ani = animation.FuncAnimation(app.fig, animate, interval=100)
    app.mainloop()
