#!/bin/bash
echo "-----START JOB at `date`-----"

#set -e

# Setup work directory
workdir=test
mkdir -p $workdir
echo "Workdir "$workdir
cp *.py $workdir

# Where do I put the output?
#mkdir -p {outputdir}

cd $workdir
dddb='dddb-20150702'
conddb='sim-20150716-vc-mu100'
lblogin='x86_64-slc6-gcc48-opt'
appconfig='v3r231'

# Prepare conditions
echo "from Configurables import LHCbApp" >> Conditions.py
echo 'LHCbApp().DDDBtag   = "'${dddb}'"' >> Conditions.py
echo 'LHCbApp().CondDBtag = "'${conddb}'"' >> Conditions.py

#-------------# 
#   GAUSS     #
#-------------#
export CMTCONFIG=${lblogin}
source LbLogin.sh -c ${lblogin}
source SetupProject.sh Gauss v48r3 --use "AppConfig '${appconfig}'"
evtid="10000000"
rm *.sim *.digi *.dst

#cp $GAUSSOPTS/Gauss-Job.py Gauss-Job.py
#echo "GaussGen.RunNumber      = "$myID";" >> Gauss-Job.py
#echo "LHCbApp().EvtMax = {events_per_job};"   >> Gauss-Job.py

# Check the opts file
optsfile=$DECFILESROOT/options/${evtid}.py
if [ ! -e $optsfile ]; then
  echo "Error, OPTSFILE not found $optsfile"
  exit 1
fi
# Run
gaudirun.py $optsfile Conditions.py Gauss-Job.py Beam-Conditions.py $APPCONFIGOPTS/Gauss/EnableSpillover-25ns.py \
    $APPCONFIGOPTS/Conditions/IgnoreCaliboffDB_LHCBv38r7.py $LBPYTHIA8ROOT/options/Pythia8.py \
    $APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py \
    $APPCONFIGOPTS/Gauss/Gauss-Upgrade-Baseline-20150522.py $APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py
# Prepare output
mv `ls *.sim` Gauss.sim


#-------------# 
#   BOOLE     #
#-------------#
cd $workdir
export CMTCONFIG=${lblogin}
source LbLogin.sh -c ${lblogin}
source SetupProject.sh Boole v29r8 --use "AppConfig v3r232"
# Prepare files
echo "from Gaudi.Configuration import *" >> Boole-Files.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Gauss.sim' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Boole-Files.py
# Run
gaudirun.py Conditions.py Boole-Files.py $APPCONFIGOPTS/Boole/Default.py $APPCONFIGOPTS/Boole/Boole-Upgrade-Baseline-20150522.py $APPCONFIGOPTS/Boole/EnableSpillover.py $APPCONFIGOPTS/Boole/Upgrade-RichMaPMT-NoSpilloverDigi.py $APPCONFIGOPTS/Boole/xdigi.py $APPCONFIGOPTS/Boole/Boole-Upgrade-NoNoise.py $APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py

#------------# 
#   MOORE    #
#------------#

#cd $workdir
#export CMTCONFIG={moore_lblogin}
#source LbLogin.sh -c {moore_lblogin}
#source SetupProject.sh Moore {moore_version} --use "AppConfig {moore_appconfig}"
# Prepare special conditions
#echo "from Gaudi.Configuration import *" > MooreConfiguration.py
#echo "from Configurables import LHCbApp, Moore" >> MooreConfiguration.py
#echo 'LHCbApp().DDDBtag   = "'${dddb}'"' >> MooreConfiguration.py
#echo 'LHCbApp().CondDBtag = "'${conddb}'"' >> MooreConfiguration.py
#echo 'Moore().DDDBtag   = "'${dddb}'"' >> MooreConfiguration.py
#echo 'Moore().CondDBtag = "'${conddb}'"' >> MooreConfiguration.py
#echo "EventSelector().Input = [\"DATAFILE='PFN:./Boole.digi' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> MooreConfiguration.py
#echo "Moore().outputFile = 'Moore.dst'" >> MooreConfiguration.py
# Run
#gaudirun.py  MooreConfiguration.py


#-------------# 
#   BRUNEL    #
#-------------#

cd $workdir
export CMTCONFIG=${lblogin}
source LbLogin.sh -c ${lblogin}
source SetupProject.sh Brunel v48r0 --use "AppConfig '${appconfig}'"
# Prepare files
echo "from Gaudi.Configuration import *" >> Brunel-Files.py
#Uncomment if you include Moore
#echo "EventSelector().Input = [\"DATAFILE='PFN:./Moore.dst' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Brunel-Files.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Boole.digi' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Brunel-Files.py
# Run
gaudirun.py Conditions.py Brunel-Files.py $APPCONFIGOPTS/Brunel/MC-WithTruth.py $APPCONFIGOPTS/Brunel/Brunel-Upgrade-Baseline-20150522.py $APPCONFIGOPTS/Brunel/Upgrade-RichPmt.py $APPCONFIGOPTS/Brunel/patchUpgrade1.py $APPCONFIGOPTS/Brunel/ldst.py $APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py


#------------------------# 
#   DAVINCI/STRIPPING    #
#------------------------#
#if false ; then
#    (
#    cd $workdir
#    export CMTCONFIG={lblogin}
#    source LbLogin.sh -c {lblogin}
#    # And setup
#    source SetupProject.sh DaVinci {davinci_version} --use "AppConfig {davinci_appconfig}"
#    # Prepare files
#    echo "from Gaudi.Configuration import *" >> DaVinci-Files.py
#    echo "EventSelector().Input = [\"DATAFILE='PFN:./Brunel.dst' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> DaVinci-Files.py
#    # Run
#    gaudirun.py {stripping_options} Conditions.py DaVinci-Files.py
#    )
#fi

# Finish
ls -l $workdir
# cp -f `ls $workdir/*AllStreams.dst` {outputdir}/StrippedMC.{event_type}.${{myID}}.dst
#cp -f Brunel.dst {outputdir}/StrippedMC.{event_type}.${{myID}}.dst
#cp -f GeneratorLog.xml {logdir}/{name}.${{myID}}.GeneratorLog.xml
# cp -r  $workdir  {outputdir}/${{myID}}

echo "-----END JOB at `date`-----"

# EOF
