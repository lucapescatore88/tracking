import math
import retina
from event_generator import event_generator as gen
from planes_geometry import planes_geom as planes

dimensions = {
    'x0' :    { 'min' : 0, 'max' : 0, 'npoints' : 1},
    'y0' :    { 'min' : 0, 'max' : 0, 'npoints' : 1},
    'z0' :    { 'min' : -15, 'max' : 15, 'npoints' : 50},
    'alpha' : { 'min' : 0., 'max' : 5., 'npoints' : 50},
    'phi' :   { 'min' : 0., 'max' : 2*math.pi, 'npoints' : 50}
    }

myretina = retina.retina(npoints = 50, nplanes = 20, pl_dist = 3.)#, time=True)

geom = planes(
			nplanes = 20,	# Number of planes
			pl_dist = 3., # Plane to plane distance
			planes_inner_radius = 1, # cm
			planes_outer_radius = 30, # cm
			)
			
evt_gen = gen(
			geometry = geom,
			hit_eff = 1.,	# Hit efficiency. 1 for simplicity
			lumi_sigma = [0.1,0.1,5.], # Luminosity region gaussian with sigma = 5 cm around 0
			sigma = [0.1,0.1,0.,30.]
		)
	
evt_gen.generate_event(ntracks = 1, nnoise = 20)
evt_gen.print_track(evt_gen.tracks[0])
evt_gen.draw_plane(evt_gen.tracks,evt_gen.noise)
#evt_gen.print_track(evt_gen.tracks[1],opt="nohits")

myretina.analyse_event(tracks=evt_gen.tracks,noise=evt_gen.noise)
myretina.plot_grid("z0","alpha")




