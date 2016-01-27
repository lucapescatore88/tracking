import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


class planes_geom :
	
	def __init__(self, nplanes, pl_dist, planes_inner_radius, planes_outer_radius) :
		
		self.nplanes = nplanes
		self.pl_dist = pl_dist
		self.planes_inner_radius = planes_inner_radius
		self.planes_outer_radius = planes_outer_radius
		
		self.positions = [ (0.,0.,pl * self.pl_dist) for pl in range(self.nplanes) ]
	
	def draw_event(self, tracks, noise, planes = [0]) :

		for pl in planes :
			
			print "Drawing plane", pl
			hits_x = []
			hits_y = []
			for trk in tracks :
				hit = trk["hits"][pl]
				if( len(hit) < 3) : continue
				hits_x.append( hit[0] )
				hits_y.append( hit[1] )
			
			noise_hits_x = [ p[0] for p in noise[pl] ]
			noise_hits_y = [ p[1] for p in noise[pl] ]
		
			circle=plt.Circle((0,0),self.planes_outer_radius, fill='grey', edgecolor='black')
			circle_in=plt.Circle((0,0),self.planes_inner_radius, color='w')
		
			fig = plt.gcf()
			lim = self.planes_outer_radius*1.1
			fig.gca().axis([-lim,lim,-lim,lim])
			fig.gca().add_artist(circle)
			fig.gca().add_artist(circle_in)
			fig.gca().plot(hits_x,hits_y,'o',color='red')
			fig.gca().plot(noise_hits_x,noise_hits_y,'o',color='black')
			fig.savefig('plane'+str(pl)+'.png')
		
			#plt.show()
		 
		fig.gca().cla()
		fig.gca().axis([-self.pl_dist,(self.nplanes+1)*self.pl_dist,-lim,lim])

		hits_y = []
		hits_z = []
		for t,trk in enumerate(tracks) :
			for p in trk["hits"] :
				if len(p) > 1 :
					hits_y.append(p[0])
					hits_z.append(p[2])
		
		for pl in range(self.nplanes) :
			fig.gca().plot( 
				[pl*self.pl_dist,pl*self.pl_dist],
				[-self.planes_outer_radius,-self.planes_inner_radius],
				'r')
			fig.gca().plot( 
				[pl*self.pl_dist,pl*self.pl_dist],
				[self.planes_inner_radius,self.planes_outer_radius],
				'r')
		fig.gca().plot(hits_z,hits_y,'o',color='red')
		fig.savefig('event.png')
		
		plt.show()
			
