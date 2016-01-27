from random import *
from math import *
import numpy as np

nevts = 1000000

msigma = sqrt(2*0.9*0.9)

gmean = 0
gsigma = 5.2

xmean = xsigma = 0
xes = []

dmean = dminmean = dsigma = dminsigma = 0
ds = []
dmins = []

mag1s = mag2s = mag_min1s = mag_min2s = 0

mu = 2
i = 0


def gen_vertices(nvtx,mean,sigma) :

    out = {}
    out["vtxs"] = []
    for n in range(0,nvtx) :
        out["vtxs"].append(gauss(mean,sigma))
    
    out["dists"] = []
    out["min_dist"] = -1
    out["max_dist"] = -1
    if nvtx > 1 :
        v_ord = sorted(out["vtxs"])
        out["dists"] = [ abs(v_ord[i] - v_ord[i+1]) for i in range(0,len(v_ord) - 1)]
        out["max_dist"] = max(out["dists"])
        out["min_dist"] = min(out["dists"])

    return out




while i < nevts :

    nvtx = np.random.poisson(mu)
    if(nvtx <=1) : continue

    i += 1
    print "\r %.2f %% done ..." % (float(i)/nevts*100.),

    vtxs = gen_vertices(nvtx,gmean,gsigma)
    
#    print len(vtxs["vtxs"])

    xes.append(vtxs["vtxs"][0])
    xmean += xes[-1]

    ds.append(vtxs["max_dist"])
    dmean += ds[-1]

    dmins.append(vtxs["min_dist"])
    dminmean += dmins[-1]

    if(ds[-1] > msigma) :
        mag1s += 1 
    if(ds[-1] > 2 * msigma) :
        mag2s += 1

    if(dmins[-1] > msigma) :
        mag_min1s += 1 
    if(dmins[-1] > 2 * msigma) :
        mag_min2s += 1



xmean /= len(xes)
dmean /= len(ds)
dminmean /= len(dmins)

for k in range(0,len(ds)) :

    dsigma += (ds[k] - dmean)*(ds[k] - dmean)
    dminsigma += (dmins[k] - dminmean)*(dmins[k] - dminmean)
    xsigma += (xes[k] - xmean)*(xes[k] - xmean)

dsigma /= len(ds)
dsigma = sqrt(dsigma) 
dminsigma /= len(dmins)
dminsigma = sqrt(dminsigma) 
xsigma /= len(xes)
xsigma = sqrt(xsigma)


print "X -> mean: %.3f sigma: %.3f" % (xmean, xsigma)
print "Max |X-Y| -> mean: %.3f sigma: %.3f" % (dmean, dsigma)
print "Min |X-Y| -> mean: %.3f sigma: %.3f" % (dminmean, dminsigma)
print "Sigma measurement = %.3f" % msigma
print "Max distance above 1 sigma = %.1f %%" % (float(mag1s) / len(xes)*100)
print "Max distance above 2 sigma = %.1f %%" % (float(mag2s) / len(xes)*100)
print "Min distance above 1 sigma = %.1f %%" % (float(mag_min1s) / len(xes)*100)
print "Min distance above 2 sigma = %.1f %%" % (float(mag_min2s) / len(xes)*100)




