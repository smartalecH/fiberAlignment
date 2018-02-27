import ctypes as ct
import numpy as np
import nidaqmx
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import GuiFunctions as gf
from mpl_toolkits.mplot3d import Axes3D
#3.2mw/1.42v
#2.2535 mw/v
#
# Surface plot code courtesy of CMCDragonkai, see
# https://gist.github.com/CMCDragonkai/dd420c0800cba33142505eff5a7d2589
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def surface_plot (matrix, **kwargs):
    # acquire the cartesian coordinate matrices from the matrix
    # x is cols, y is rows
    (x, y) = np.meshgrid(np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (fig, ax, surf)

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)

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
    #lim = avg * 1.5
    #plt.axis([0,1000,0,lim])
    ax1.plot(x,y,'r-',x,z,'b-')
    plt.ylabel('Voltage (mv)')
    plt.xlabel('Measurement #')
    plt.title("DAQ Real-Time Measurements")
    plt.legend(['Measured voltage','Average = ' + str('{:.2f}'.format(avg)) + ' mV'], loc='upper left', bbox_to_anchor=(0.6,1))

def get100data():
    with nidaqmx.Task() as task:
        # Configure task
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        task.timing.cfg_samp_clk_timing(10000, samps_per_chan = 100)
        # Read the data
        data = task.read(number_of_samples_per_channel=100)
        return data

def getAverage():
    a = np.array(get100data())
    avg = np.mean(a) * 1000
    return avg

def calcPercent():
    avg = getAverate()
    percent = 2.2535*avg/3.2
    return percent

def runChart():
    ani = animation.FuncAnimation(fig, animate, interval=20)
    plt.show()

def xzIntensity():
    gf.connect()
    square = 20 + 1
    xlist = np.linspace(0,20,square)
    ylist = np.linspace(0,20,square)
    zlist = np.zeros((square,square))
    sleep(2)
    for x in range (len(xlist)):
        gf.setPosition(xlist[x],1)
        for y in range (len(ylist)):
            gf.setPosition(ylist[y],3)
            zlist[x,y] = getAverage()

    (fig, ax, surf) = surface_plot(zlist, cmap=cm.coolwarm)
    fig.colorbar(surf)
    ax.set_xlabel('X (um)')
    ax.set_ylabel('Y (um)')
    ax.set_zlabel('Z (mV)')
    plt.show()

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
	
def J(x):
	# Channel 1 = x
	# Channel 2 = y
	# Channel 3 = z
	gf.setPosition(x[0],1)
	gf.setPosition(x[1],3)
	sleep(0.1)
	return getAverage()

if __name__ == "__main__":
    #ani = animation.FuncAnimation(fig, animate, interval=20)
    #plt.show()
    #values = np.zeros((2000,2000))
    #print values
    #xzIntensity()
    probability3d()
