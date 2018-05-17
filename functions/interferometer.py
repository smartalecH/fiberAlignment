import numpy as np
import nidaqmx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai1")

fig1 = plt.figure()
#fig2 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)
#ax2 = fig2.add_subplot(1,1,1)

rate = 1000
samples = 100

def getData():
    task.timing.cfg_samp_clk_timing(rate, samps_per_chan = samples)
    data = np.array(task.read(number_of_samples_per_channel = samples))
    return data

def plot_modes(i):
    data = getData()
    x = np.array(np.linspace(1,samples,samples))
    y1 = np.array(data[0])
    y2 = np.array(data[1])

    ax1.cla()
    plt.axis([1,samples,0,3])
    ax1.plot(x,y1,'-r',x,y2,'-b')

def live_plot():
    ani = animation.FuncAnimation(fig1, plot_modes)
    plt.show()

if __name__ == "__main__":
    live_plot()
