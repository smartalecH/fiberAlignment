
from functions import daq
from functions import GuiFunctions as gf
import numpy
from scipy.optimize import minimize


def sphere(x):
    return sum((x[0:])**2.0)
def rosen(x):
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
x0 = numpy.array([1.7,1.5,.1])
res = minimize(rosen, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print(res.x)
print(res.keys())
res = minimize(rosen, x0, method='CG', options={'gtol': 1e-8, 'disp': True})
print(res.x)

res = minimize(sphere, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print(res.x)

res = minimize(sphere, x0, method='CG', options={'gtol': 1e-8, 'disp': True})
print(res.x)
