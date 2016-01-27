import math
import sys
from planes_geometry import planes_geom as planes
import numpy as np
import matplotlib.pyplot as plt
import itertools

c = 3.e-2 #3e8 / 1e10

class retina :

    def __init__(self, nplanes, pl_dist, npoints = 50, time = False, fast = True) :
        
        self.grid = {}
        self.npts = npoints
        self.fast_retina = fast
        self.usetime = time
        self.timesigma = 4. * 30.
        self.rin = 1.
        self.rout = 30.
        self.zmin = 0.
        self.zmax = (nplanes-1) * pl_dist
        self.step_r = 2*self.rout / self.npts
        self.step_phi = 2*math.pi / self.npts
        
        self.ranges = {
                "r1" : [ self.step_r*(x+0.5) for x in range(0,self.npts)],
                "phi1" : [ self.step_r*(x+0.5) for x in range(0,self.npts)],
                "r2" : [ self.step_phi*(x+0.5) for x in range(0,self.npts)],
                "phi2" : [ self.step_phi*(x+0.5) for x in range(0,self.npts)],
                "x1" : [ self.step_r*(x+0.5) - self.rout for x in range(0,self.npts)],
                "x2" : [ self.step_r*(x+0.5) - self.rout for x in range(0,self.npts)],
                "y1" : [ self.step_r*(x+0.5) - self.rout for x in range(0,self.npts)],
                "y2" : [ self.step_r*(x+0.5) - self.rout for x in range(0,self.npts)]
        }
        
    def get_intersect(self,line,z) :
        
        if ( abs(line[1] - line[0]) < 1.e-6 ) : return None
        if ( abs(line[3] - line[2]) < 1.e-6 ) : return None

        zx0 = -line[0] * ( self.zmax - self.zmin ) / (line[1] - line[0]) + self.zmin
        yx0 = line[2] + ( zx0 - self.zmin) * (line[3] - line[2])
        #if abs(yx0) > 1 :  return None

        factor = ( z - self.zmin) / ( self.zmax - self.zmin )
        x = line[0] + factor * (line[1] - line[0])
        y = line[2] + factor * (line[3] - line[2])
        return [ x, y, math.sqrt( (zx0 - z)**2 + y**2 + x**2) / c ]

	def get_closest_pt(self,p0,p1) :
		
		nstepx0 = round( p0[0] / self.step_r )
		nstepy0 = round( p0[1] / self.step_r )
		nstepx1 = round( p1[0] / self.step_r )
		nstepy1 = round( p1[1] / self.step_r )
		return [nstepx0*self.step_r,nstepx1*self.step_r,nstepy0*self.step_r,nstepy1*self.step_r]

    def analyse_event(self, tracks, noise) :

        all_pts = noise
        for tr in tracks :
            for pl,hit in enumerate(tr["hits"]) :
                if(len(hit)>1) : all_pts[pl].append(hit)

        sigma = 2*self.step_r
        twosigma = 2 * sigma
        twosigmasq = 2 * sigma * sigma
		
		grid = []
		if( self.fast_retina ) :
			for p0 in range(all_pts[5]) :
				for p1 in range(all_pts[-1]) :
					grid.append(self.get_closest_pt(p0,p1))			
		else :
			grid = itertools.product(self.ranges["x1"],self.ranges["x2"],self.ranges["y1"],self.ranges["y2"])
		
        for pt in grid :
            for pl in range(len(all_pts)) :
                for p in all_pts[pl] :
                    
                    intersect = self.get_intersect(pt,p[2])
                    if intersect is None : continue
                    dist = abs(p[0] - intersect[0]) + abs(p[1] - intersect[1]) 
                    if(twosigma > dist) :
                        if pt not in self.grid : self.grid[pt] = 0
                        self.grid[pt] += math.exp(-(dist*dist)/twosigmasq)
                        if self.usetime :
                            self.grid[pt] += math.exp(-((p[3] - intersect[2])**2)/self.timesigma)


    def plot_grid(self,xv,yv) :
        
        fig = plt.gcf()
        x = []
        y = []
        w = []
        for coord,val in self.grid.iteritems() :    
            x.append( coord[2] )
            y.append( coord[3] )
            w.append( val )

        maxgrid = max(self.grid.iterkeys(), key=lambda k: self.grid[k])
        xA,yA,zA = maxgrid[0], maxgrid[2], self.zmin
        xB,yB,zB = maxgrid[1], maxgrid[3], self.zmax
        dx = (xB - xA)
        dy = (yB - yA)
        dz = (zB - zA)
        if(dx == 0) : phi = math.pi / 2.
        else : phi = math.atan ( dy / dx )
        if( phi == 0 ) : alpha = math.atan ( dy / dz / math.sin( phi ) )
        else : alpha = math.atan ( dx / dz / math.cos( phi ) )
        z0 = zA - xA * dz / dx
        print "(x1,x2,y1,y2) = ", maxgrid
        print "z0 = ", z0, " phi = ", phi, " alpha = ", alpha
        
        fig.gca().hist2d(x,y,weights=w,bins=[self.ranges["x1"],self.ranges["x2"]])
        plt.show()
        fig.savefig('retina.png')




