import math
import sys
from planes_geometry import planes_geom as planes
import numpy as np
import matplotlib.pyplot as plt
import itertools

class retina :

    def __init__(self, dimensions, distance) :
        
        self.grid = {}
        self.dims = dimensions
        self.distance = distance

        self.ranges = []
        for k,dim in dimensions.iteritems() :

            npts = 100
            if( 'npoints' in dim ) :
                npts = dim["npoints"]
            self.dims[k]["npoints"] = npts
            if( npts <= 1 ) :
                self.dims[k]["step"] = 0
                self.dims[k]["range"] = [dim["max"] - dim["min"]]
                self.ranges.append(self.dims[k]["range"])
                continue
            
            self.dims[k]["step"] = float(dim["max"] - dim["min"]) / (npts - 1)
            self.ranges.append([x * self.dims[k]["step"] + dim["min"] for x in range(0,npts)])
            self.dims[k]["range"] = self.ranges[-1]
            
    def analyse_event(self, tracks, noise) :

        all_pts = noise
        for tr in tracks :
            for pl,hit in enumerate(tr["hits"]) :
                all_pts[pl] = []
                if(len(hit)>1) :
                    all_pts[pl].append(hit)

        sigma = math.sqrt(3.)
        #for d in self.dims :
        #    print self.dims[d]["step"]
        #    sigma += self.dims[d]["step"]
        twosigma = 2 * sigma
        twosigmasq = 2 * sigma * sigma

        for p0 in all_pts[0] :
            for p1 in all_pts[-1] :
                params = self.distance(p0,p1)
                for pt in itertools.product(*self.ranges) :
                    dist = abs(pt[2] - params[2]) / self.dims["z0"]["step"] 
                         + abs(pt[3] - params[1]) / self.dims["alpha"]["step"] 
                         + abs(pt[4] - params[0]) / self.dims["phi"]["step"] 
                    if(twosigma > dist) :
                        if pt not in self.grid : self.grid[pt] = 0
                        self.grid[pt] += math.exp(-(dist*dist)/twosigmasq)

            

        #for pl0 in range(len(all_pts)-1) :
        #    for p0 in  all_pts[pl0] :
        #        for p1 in  all_pts[pl0+1] :
        #            params = self.distance(p0,p1)
        #            print params
        #            for pt in itertools.product(*self.ranges) :
        #                dist = abs(pt[2] - params[2]) / self.dims["z0"]["step"] 
        #                + abs(pt[3] - params[1]) / self.dims["alpha"]["step"] 
        #                + abs(pt[4] - params[0]) / self.dims["phi"]["step"] 
        #                if(twosigma > dist) :
        #                    if pt not in self.grid : self.grid[pt] = 0
        #                    self.grid[pt] += math.exp(-(dist*dist)/twosigmasq)

    def plot_grid(self,xv,yv) :
        
        fig = plt.gcf()
        #print xv,yv,self.dims[xv]["step"], self.dims[yv]["step"]        
        binsx = np.arange(self.dims[xv]["min"]-self.dims[xv]["step"]/2.,
                self.dims[xv]["max"]+self.dims[xv]["step"]/2.,self.dims[xv]["step"])
        binsy = np.arange(self.dims[yv]["min"]-self.dims[yv]["step"]/2.,
                self.dims[yv]["max"]+self.dims[yv]["step"]/2.,self.dims[yv]["step"])
        
        x = []
        y = []
        w = []
        for coord,val in self.grid.iteritems() :    
            x.append( coord[2] )
            y.append( coord[3] )
            w.append( val )

        print max(self.grid.iterkeys(), key=lambda k: self.grid[k])
        
        fig.gca().hist2d(x,y,weights=w,bins=[binsx,binsy])
        #fig.gca().hist(x,weights=w,bins=binsx)
        plt.show()
        fig.savefig('retina.png')




