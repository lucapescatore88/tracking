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
#echo "from Configurables import LHCbApp" >> Conditions.py
#echo 'LHCbApp().DDDBtag   = "{dddb}"' >> Conditions.py
#echo 'LHCbApp().CondDBtag = "{conddb}"' >> Conditions.py


#-------------# 
#   BOOLE     #
#-------------#
#(
#cd $workdir
#export CMTCONFIG={lblogin}
#source LbLogin.sh -c {lblogin}
#source SetupProject.sh Boole {boole_version} --use "AppConfig {boole_appconfig}"
# Prepare files
#echo "from Gaudi.Configuration import *" >> Boole-Files.py
#echo "EventSelector().Input = [\"DATAFILE='PFN:./Gauss.sim' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Boole-Files.py
# Run
#gaudirun.py {boole_options} Conditions.py Boole-Files.py
#)

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

 "-----END JOB at `date`-----"

# EOF
