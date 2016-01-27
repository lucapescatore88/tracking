import math
import numpy as np
import matplotlib.pyplot as plt
import random
from planes_geometry import planes_geom as planes


class event_generator :
	
	def __init__(self, geometry, hit_eff, lumi_sigma, sigma, twoD = False) :
		
		self.geom = geometry
		self.hit_eff = hit_eff
		self.lumi_sigma = lumi_sigma
		self.sigma = sigma
		self.twoD = twoD

		self.tracks = []
	
	
	def generate_event(self, ntracks = 1, nnoise = 20) :
		
		for tr in range(ntracks) :
			self.tracks.append( self.generate_track() )
		
		self.generate_noise(nnoise)
			
	def generate_track(self) :
	
		trk = {}
	
		max_alpha = math.asin( self.geom.planes_outer_radius / (self.geom.nplanes * self.geom.pl_dist) )
		min_alpha = math.asin( self.geom.planes_inner_radius / self.geom.pl_dist )
	
		# Get random track parameters
	
		trk["x0"]	= 0. #random.gauss(0,self.lumi_sigma[0])
		trk["y0"]	= 0. #random.gauss(0,self.lumi_sigma[1])
		trk["z0"]	= random.gauss(0,self.lumi_sigma[2])
	
		trk["phi"]  = 0.
		if not self.twoD :
			trk["phi"]   = random.uniform(0,2*math.pi)
		trk["alpha"] = random.uniform(min_alpha,max_alpha)
	
		trk["xc"]	= math.tan(trk["alpha"]) * math.cos(trk["phi"])
		trk["yc"]	= math.tan(trk["alpha"]) * math.sin(trk["phi"])
	
		# Now find the crossing points with the planes (true coordinates)
	
		trk["true_hits"] = []
		c = 3.e-2 # 3e8 / 1e10 # speed of light in m/s
	
		for pl in self.geom.positions :
				
			curz = pl[2]
			if(trk["z0"] > curz) : 
				trk["true_hits"].append('X')
				continue
			
			curx = trk["x0"] + trk["xc"] * (curz - trk["z0"])
			cury = trk["y0"] + trk["yc"] * (curz - trk["z0"])
			trk["true_hits"].append(
				[
					curx, cury, curz,
					math.sqrt(  ( 1. + trk["xc"]**2 + trk["yc"]**2 ) * (curz - trk["z0"] )**2 ) / c
				]
			)

		# now define the measurements. In this case just gaussian smeared
		
		trk["hits"] = []
 
		for pl in trk["true_hits"] :
			if len(pl) > 1 :
				y = 0.
				if not self.twoD : y = random.gauss(pl[1], self.sigma[1])
				trk["hits"].append( [				# Smear true hit by resolution
					random.gauss(pl[0], self.sigma[0]),
					y, pl[2],
					random.gauss(pl[3], self.sigma[3])
				] )
			else :
				trk["hits"].append( ['X'] )
	
		return trk
	
	
	
	def generate_noise(self, nnoise) :
	
		# add noise
		
		self.noise = {}
		
		for p,pl in enumerate(self.geom.positions) :
		
			self.noise[p] = []
		
			for pn in range(0,nnoise) :
				r = random.uniform(self.geom.planes_inner_radius, self.geom.planes_outer_radius)
				phi = random.uniform(0, 2*math.pi)
				self.noise[p].append(
				 [				
					r*math.cos(phi),
					r*math.sin(phi),
					pl[2],
					random.uniform(0, 1000)
					]
				)

	def print_track(self,trk,opt="") :
		
		print "Track true parameters"
		print "(x0,y0,z0) = ({:.3},{:.3},{:.3})".format( trk["x0"], trk["y0"], trk["z0"] )
		print "alpha, phi = {:.3} {:.3}".format( trk["alpha"], trk["phi"] )
		
		if(opt!="nohits") :
			print "True hits \t\t\t\t Smeared hits"
			for t,s in zip(trk["true_hits"],trk["hits"]) :
				if len(t) > 1 :
					print "(x,y,z,t) = ({0:.2f},{1:.2f},{2:.2f},{3:.2f})".format(*t),
					print "\t(x,y,z,t) = ({0:.2f},{1:.2f},{2:.2f},{3:.2f})".format(*s)
				else :
					print 'X' 

	def draw_plane(self, trks, noise, planes = [0], opt = "") :

		for pl in planes :
			
			noise_hits_x = [ p[0] for p in noise[pl] ]
			noise_hits_y = [ p[1] for p in noise[pl] ]
			hits_x = []
			hits_y = []
			for tr in trks :
				if( len(tr["hits"][pl]) < 2 ) : continue
				hits_x.append( tr["hits"][pl][0] )
				hits_y.append( tr["hits"][pl][1] )
			
			circle=plt.Circle((0,0),self.geom.planes_outer_radius, fill='grey', edgecolor='black')
			circle_in=plt.Circle((0,0),self.geom.planes_inner_radius, color='w')
		
			fig = plt.gcf()
			lim = self.geom.planes_outer_radius*1.1
			fig.gca().axis([-lim,lim,-lim,lim])
			fig.gca().add_artist(circle)
			fig.gca().add_artist(circle_in)
			fig.gca().plot(hits_x,hits_y,'o',color='red')
			fig.gca().plot(noise_hits_x,noise_hits_y,'o',color='black')
			fig.savefig('plane'+str(pl)+'.png')
		
			#plt.show()
		 
		fig.gca().cla()
		fig.gca().axis([-self.geom.pl_dist,(self.geom.nplanes+1)*self.geom.pl_dist,-lim,lim])
		
		hits_x = []
		hits_z = []
		for trk in trks :
			for p in trk["hits"] :
				if len(p) > 1 :
					hits_x.append(p[0])
					hits_z.append(p[2])
		
		for pl in range(self.geom.nplanes) :
		   fig.gca().plot( 
		   		[pl*self.geom.pl_dist,pl*self.geom.pl_dist],
				[-self.geom.planes_outer_radius,-self.geom.planes_inner_radius],'r')
		   fig.gca().plot( 
		   		[pl*self.geom.pl_dist,pl*self.geom.pl_dist],
				[self.geom.planes_inner_radius,self.geom.planes_outer_radius],'r') 

		fig.gca().plot(hits_z,hits_x,'o',color='red')
		fig.savefig("event.png")	
		plt.show()
			
			
		

if __name__ == "__main__":

	geom = planes(
			nplanes = 20,	# Number of planes
			pl_dist = 3., # Plane to plane distance
			planes_inner_radius = 1, # cm
			planes_outer_radius = 30, # cm
			)
			
	evt_gen = event_generator(
			geometry = geom,
			hit_eff = 1.,	# Hit efficiency. 1 for simplicity
			lumi_sigma = [0.1,0.1,5.], # Luminosity region gaussian with sigma = 5 cm around 0
			sigma = [0.1,0.1,0.,30.]
		)
	
	evt_gen.generate_event(ntracks = 2, nnoise = 20)
	#evt_gen.print_track(evt_gen.tracks[0])
	#geom.draw_event(evt_gen.tracks,evt_gen.noise)
		


