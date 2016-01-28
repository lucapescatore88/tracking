# File for setting hypotetical Beam conditions
# They are suitable for upgrade studies:
#   Beam 7 TeV, beta* = 3m , emittance(normalized) ~ 2 micron
#   No spill-over
# 
#
# Requires Gauss v45r1 or higher.
#
# Syntax is: 
#  gaudirun.py $APPCONFIGOPTS/Gauss/Beam7000GeV-md100-nu6.8-v45r1.py
#              $DECFILESROOT/options/30000000.opts (i.e. event type)
#              $LBGENROOT/options/GEN.py (i.e. production engine)
#              Sim08-2011-Tags.py (i.e. database tags to be used)
#              gaudi_extra_options_NN_II.py (ie. job specific: random seed,
#                               output file names, see Gauss-Job.py as example)
#
from Configurables import Gauss
from GaudiKernel import SystemOfUnits

#--Set the L/nbb, total cross section and revolution frequency and configure
#  the pileup tool, a CrossingRate of 11.245 kilohertz is used internally
#  This is the L per bunch, corresponding to
#                           L = 2 x 10^33 cm-2 s-1 with 2400 colliding bunches
#  It correspond to nu(total) = 7.6 and we assume mu(visible)=0.699*nu
Gauss().Luminosity        = 0.8338*(10**30)/(SystemOfUnits.cm2*SystemOfUnits.s)
Gauss().TotalCrossSection = 102.5*SystemOfUnits.millibarn

#--Set the average position of the IP: assume a perfectly centered beam in LHCb
Gauss().InteractionPosition = [ 0.0, 0.0, 0.0 ]

#--Set the bunch RMS, this will be used for calculating the sigmaZ of the
#  Interaction Region. SigmaX and SigmaY are calculated from the beta* and
#  emittance
Gauss().BunchRMS = 90.0*SystemOfUnits.mm

#--Set the energy of the beam,
Gauss().BeamMomentum      = 7.0*SystemOfUnits.TeV

#--the half effective crossing angle (in LHCb coordinate system), horizontal
#  and vertical. The horizontal one is given by the LHCb magnet and corrector
#  so its sign depend on the polarity (negative angle for magnet down)
Gauss().BeamHCrossingAngle = -0.115*SystemOfUnits.mrad
Gauss().BeamVCrossingAngle = 0.000*SystemOfUnits.mrad
Gauss().BeamLineAngles     = [ 0.0, 0.0 ]

#--beta* and emittance (beta* is nomimally 3m and e_norm 2.5um,
#                       adjusted to match sigmaX and sigmaY)
Gauss().BeamEmittance     = 0.0038*SystemOfUnits.mm
# Gives \sigma_{x,y} = 0.037697  ~= 0.0377
Gauss().BeamBetaStar      = 2.79*SystemOfUnits.m
