
from functions import daq
from functions import GuiFunctions as gf
import numpy
from scipy.optimize import minimize
from time import sleep
# Imports for plotting path
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#def sphere(x):
#    print x[0]
#    print x[1]
#    print x[2]
#    print ""
#    return sum((x[0:])**2.0)
#def rosen(x):
#    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
#bnds = ((2,5),(-2,0))
x0 = numpy.array([10,10])
gf.connect()
sleep(3) # Gives piezo enough time to initialize
res = minimize(daq.J, x0, method='nelder-mead', options={'xatol': 0.2, 'fatol': 10, 'disp': True})
print(res.x)
course = daq.getPath()

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

"""print(res.keys())
res = minimize(rosen, x0, method='CG', options={'gtol': 1e-8, 'disp': True})
print(res.x)

res = minimize(sphere, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print(res.x)

res = minimize(sphere, x0, method='CG', options={'gtol': 1e-8, 'disp': True})
print(res.x)"""
