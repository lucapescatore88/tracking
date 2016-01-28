#!/bin/bash
#SBATCH -D {workdir}
#SBATCH -o {logdir}/{name}.%j.out
#SBATCH -J {name}
#SBATCH -N {num_nodes}
#SBATCH -n 1
#SBATCH -c {cpus_per_task}
#SBATCH -A {queue}
#SBATCH -p {queue}
#SBATCH -t {time}
#SBATCH --mem-per-cpu={mem_per_cpu}
{sbatch_directives}

echo "-----START JOB at `date`-----"

set -e

# Setup work directory
myID=$SLURM_JOB_ID 
workdir=$WORK/test
mkdir -p $workdir
echo "Workdir "$workdir

function finish {{ 
  echo "Cleaning up"
  rm -rf "$workdir"
}}
trap finish EXIT SIGTERM SIGXCPU SIGINT SIGKILL

# Where do I put the output?
mkdir -p {outputdir}

# Setup everything
#cp $myhome/MC/DecFiles/* $workdir/

cd $workdir

# Prepare conditions
echo "from Configurables import LHCbApp" >> Conditions.py
echo 'LHCbApp().DDDBtag   = "{dddb}"' >> Conditions.py
echo 'LHCbApp().CondDBtag = "{conddb}"' >> Conditions.py

#-------------# 
#   GAUSS     #
#-------------#
(
cd $workdir
export CMTCONFIG={lblogin}
source LbLogin.sh -c {lblogin}
source SetupProject.sh Gauss {gauss_version} --use "AppConfig {gauss_appconfig}"
# Prepare gauss
cp $GAUSSOPTS/Gauss-Job.py Gauss-Job.py
echo "GaussGen.RunNumber      = "$myID";" >> Gauss-Job.py
echo "LHCbApp().EvtMax = {events_per_job};"   >> Gauss-Job.py

# Check the opts file
optsfile=$DECFILESROOT/options/{event_type}.py
if [ ! -e $optsfile ]; then
  echo "Error, OPTSFILE not found $optsfile"
  exit 1
fi
# Run
gaudirun.py {gauss_options} $optsfile Conditions.py Gauss-Job.py
# Prepare output
mv `ls *.sim` Gauss.sim
)

#-------------# 
#   BOOLE     #
#-------------#
(
cd $workdir
export CMTCONFIG={lblogin}
source LbLogin.sh -c {lblogin}
source SetupProject.sh Boole {boole_version} --use "AppConfig {boole_appconfig}"
# Prepare files
echo "from Gaudi.Configuration import *" >> Boole-Files.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Gauss.sim' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Boole-Files.py
# Run
gaudirun.py {boole_options} Conditions.py Boole-Files.py
)

#------------# 
#   MOORE    #
#------------#
(
cd $workdir
export CMTCONFIG={moore_lblogin}
source LbLogin.sh -c {moore_lblogin}
source SetupProject.sh Moore {moore_version} --use "AppConfig {moore_appconfig}"
# Prepare special conditions
echo "from Gaudi.Configuration import *" > MooreConfiguration.py
echo "from Configurables import LHCbApp, Moore" >> MooreConfiguration.py
echo 'LHCbApp().DDDBtag   = "{dddb}"' >> MooreConfiguration.py
echo 'LHCbApp().CondDBtag = "{conddb}"' >> MooreConfiguration.py
echo 'Moore().DDDBtag   = "{dddb}"' >> MooreConfiguration.py
echo 'Moore().CondDBtag = "{conddb}"' >> MooreConfiguration.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Boole.digi' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> MooreConfiguration.py
echo "Moore().outputFile = 'Moore.dst'" >> MooreConfiguration.py
# Run
gaudirun.py {moore_options} MooreConfiguration.py
)

#-------------# 
#   BRUNEL    #
#-------------#
(
cd $workdir
export CMTCONFIG={lblogin}
source LbLogin.sh -c {lblogin}
source SetupProject.sh Brunel {brunel_version} --use "AppConfig {brunel_appconfig}"
# Prepare files
echo "from Gaudi.Configuration import *" >> Brunel-Files.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Moore.dst' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Brunel-Files.py
# Run
gaudirun.py {brunel_options} Conditions.py Brunel-Files.py
)

#------------------------# 
#   DAVINCI/STRIPPING    #
#------------------------#
if false ; then
    (
    cd $workdir
    export CMTCONFIG={lblogin}
    source LbLogin.sh -c {lblogin}
    # And setup
    source SetupProject.sh DaVinci {davinci_version} --use "AppConfig {davinci_appconfig}"
    # Prepare files
    echo "from Gaudi.Configuration import *" >> DaVinci-Files.py
    echo "EventSelector().Input = [\"DATAFILE='PFN:./Brunel.dst' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> DaVinci-Files.py
    # Run
    gaudirun.py {stripping_options} Conditions.py DaVinci-Files.py
    )
fi

# Finish
ls -l $workdir
# cp -f `ls $workdir/*AllStreams.dst` {outputdir}/StrippedMC.{event_type}.${{myID}}.dst
cp -f Brunel.dst {outputdir}/StrippedMC.{event_type}.${{myID}}.dst
cp -f GeneratorLog.xml {logdir}/{name}.${{myID}}.GeneratorLog.xml
# cp -r  $workdir  {outputdir}/${{myID}}

echo "-----END JOB at `date`-----"

# EOF
