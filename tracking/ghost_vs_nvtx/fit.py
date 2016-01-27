import numpy as np
import pylab as plt
import scipy.optimize as op

def func(fx,a,t):
    return a*np.exp(t*fx)

x = []
y = []
lines = open("xyscan.txt")
for l in lines :
	nums = l.split()
	x.append(float(nums[0]))
	y.append(float(nums[1]))
	
fx=np.array(x)
fy=np.array(y)
fxext = np.array(range(30))
#print fx, fy

# norm_x=fx.min()
# norm_y=fy.max()
# fx2=fx-norm_x+1
# fy2=fy/norm_y

popt,pcov=op.curve_fit(func,fx,fy,p0=(1,1),maxfev=6000)

plt.plot(fx,fy,'o')

gp8 = float(func(8, *popt))
for x,y in zip(fxext,func(fxext, *popt)) :
	print "N vtx = {} ==> Ghost prob = {:.3f}, Gp(Nvtx) /Gp(8) = {:.3f} ".format(x,y,y/gp8)

plt.plot(fxext,func(fxext, *popt))
plt.show()