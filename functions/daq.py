#import ctypes as ct
import numpy as np
import nidaqmx
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import GuiFunctions as gf
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import sys

#maximize imports
from scipy.optimize import minimize
# Imports for plotting path
#import matplotlib as mpl
#3.2mw/1.42v
#2.2535 mw/v

# A list for storing lists of our optimization path and values.
path = []
# uncomment the two below lines if you want to use the runChart function

# Function: surface_plot
# Purpose: Given a matrix, convert it into a form that matplotlib knows how
# to plot in 3d space as a surface.
# Parameters: the matrix to be plotted (formatted as an x by z matrix, whose
# values are the values of the surface at that point).
# Returns: a tuple containing the figure, axis, and surface.
# Surface plot code courtesy of CMCDragonkai, see
# https://gist.github.com/CMCDragonkai/dd420c0800cba33142505eff5a7d2589
def surface_plot (matrix, **kwargs):
    # acquire the cartesian coordinate matrices from the matrix
    # x is cols, y is rows
    (x, y) = np.meshgrid(np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (fig, ax, surf)

# Function: animate
# Purpose: Produce a plot that has the same function as an oscilloscope screen.
# Parameters: Auto handled by the matplotlib FuncAnimation function.
# Returns: None
def animate(i):
    # Get x and y data.
    x = np.array(np.linspace(0,100,100))
    y = np.array(get100data()) * 1000
    # Get the average value
    avg = np.mean(y)
    z = np.full((100,1), avg)
    # Clear the figure, and plot the new data
    ax1.cla()
    # The plot:
    lim = avg * 1.5
    plt.axis([0,100,0,lim])
    ax1.plot(x,y,'r-',x,z,'b-')
    plt.ylabel('Voltage (mv)')
    plt.xlabel('Measurement #')
    plt.title("DAQ Real-Time Measurements")
    plt.legend(['Measured voltage','Average = ' + str('{:.2f}'.format(avg)) + ' mV'], loc='upper left', bbox_to_anchor=(0.6,1))

# Function: get100data
# Purpose: Reads 100 samples from cDAQ1Mod1/ai0 at 10kHz sample rate. Stores
# the results in an array.
# Parameters: None
# Returns: The array of 100 sample values.
def get100data():
    with nidaqmx.Task() as task:
        # Configure task
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        task.timing.cfg_samp_clk_timing(10000, samps_per_chan = 100)
        # Read the data
        data = task.read(number_of_samples_per_channel=100)
        return data

# Function: getAverage
# Purpose: Return the average value of 100 samples read from the DAQ. Automatically
# calls get100data().
# Parameters: None
# Returns: A value, the average of 100 samples.
def getAverage():
    a = np.array(get100data())
    avg = np.mean(a) * 1000
    return avg

# THIS FUNCTION IS NOT YET COMPLETE
# Function: calcPercent
# Purpose:
# Parameters:
# Returns:
def calcPercent():
    avg = getAverage()
    percent = 2.2535*avg/3.2
    return percent

# Function: runChart
# Purpose: Run the o-scope chart directly from the daq script; no need to
# open sampleGUI.
# Parameters: None
# Returns: None; opens a new window displaying a real-time updating chart.
def runChart():
    ani = animation.FuncAnimation(fig, animate, interval=20)
    plt.show()

# Function: xzIntensity
# Purpose: Creates a surface plot of voltage intensity as the fibers'
# position varies over the xz plane.
# Parameters: None
# Returns: None. Automatically opens a new window with the plot.
def xzIntensity():
    gf.connect()
    square = 20 + 1
    xlist = np.linspace(0,20,square)
    zlist = np.linspace(0,20,square)
    ylist = np.zeros((square,square))
    sleep(2)
    for x in range (len(xlist)):
        gf.setPosition(xlist[x],1)
        for z in range (len(zlist)):
            gf.setPosition(zlist[z],3)
            sleep(.1)
            ylist[x,z] = getAverage()

    (fig, ax, surf) = surface_plot(ylist, cmap=cm.coolwarm)
    fig.colorbar(surf)
    ax.set_xlabel('Z (um)')
    ax.set_ylabel('X (um)')
    ax.set_zlabel('magnitude (mV)')
    plt.show()
    fig.canvas.manager.window.activateWindow()
    fig.canvas.manager.window.raise_()

# Function: probability3d
# Purpose: I've given up on this function.
# Parameters:
# Returns:
# This function is a work in progress.
def probability3d():
    gf.connect()
    cube = 5 + 1
    xlist = np.linspace(0,20,cube)
    ylist = np.linspace(0,20,cube)
    zlist = np.linspace(0,20,cube)
    values = np.zeros((cube,cube,cube))
    sleep(5)
    for x in range(len(xlist)):
        gf.setPosition(xlist[x],1)
        for y in range (len(ylist)):
            gf.setPosition(ylist[y],2)
            for z in range(len(zlist)):
                gf.setPosition(zlist[z],3)
                values[x,y,z] = getAverage()

    fig = plt.figure()
    ax = Axes3D(fig)
    # Trying to plot a 3d scalar field
    for x in range(len(xlist)):
        for y in range (len(ylist)):
            for z in range(len(zlist)):
                intensity = int(values[x,y,z] / 50)
                ax.scatter3D(xlist[x], ylist[y], zlist[z], marker="o", c='r')#, markersize=intensity)

    plt.show()

# Function: getPath
# Purpose: return the array stored within daq that is called "path". It is an
# array of arrays; each entry represents another n-dimension reading
# (currently x,y,voltage).
# Parameters: None
# Returns: An array of arrays containing, sequentially, the path taken during
# the optimzation process.
def getPath():
    return path

# Function: J
# Purpose: Objective function for minimization
# Parameters: An array of positions in n dimensions. Currently supports setting
# the piezo controller's x and z dimensions only.
# Returns: The negated average voltage of 100 samples, reading from the DAQ.
def J(x):
	# Channel 1 = x, Channel 2 = y, Channel 3 = z
    gf.setPosition(x[0],1)
    gf.setPosition(x[1],3)
    # Wait for transients to disappear
    sleep(0.1)
    # Add this point to the path
    path.append([x[0], x[1], getAverage()])
    # Negate the result, since we have a minimizing algorithm
    print getAverage()
    return (-1) * getAverage()

# Function: get100data
# Purpose: Reads 100 samples from cDAQ1Mod1/ai0 at 10kHz sample rate. Stores
# the results in an array.
# Parameters: None
# Returns: The array of 100 sample values.
def getTimedData(samplerate, sampletime):
    with nidaqmx.Task() as task:
        # Configure task
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        task.timing.cfg_samp_clk_timing(samplerate, samps_per_chan = samplerate * sampletime)
        # Read the data
        data = task.read(number_of_samples_per_channel=samplerate * sampletime)
        mean = np.mean(data)
        return mean

def maximize():
    x0 = np.array([10,10])
    gf.connect()
    sleep(3) # Gives piezo enough time to initialize
    res = minimize(J, x0, method='nelder-mead', options={'xatol': 0.2, 'fatol': 10, 'disp': True})
    print(res.x)
    course = getPath()

    # Plot the course
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = []
    y = []
    z = []
    for i in range (len(course)):
        x.append(course[i][0])
        y.append(course[i][1])
        z.append(course[i][2])
    ax.plot(x, y, z, label='Voltage along path')
    ax.legend()
    ax.set_xlabel('X (um)')
    ax.set_ylabel('Z (um)')
    ax.set_zlabel('Magnitude (mV)')

    plt.show()

if __name__ == "__main__":
    if sys.argv[1] == "intensity":
        xzIntensity()
    elif sys.argv[1] == "voltage":
        print (getTimedData(8000, 1))
    elif sys.argv[1] == "maximize":
        maximize()
    elif sys.argv[1] == "scope":
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        ani = animation.FuncAnimation(fig, animate, interval=20)
        plt.show()
        runChart()
    else:
        xzIntensity()
    #values = np.zeros((2000,2000))
    #print values
