#!/bin/bash
#SBATCH -D /home/venezian/MCProd/FilteredBu2KpipiGamma_12103240
#SBATCH -o /home/venezian/MCProd/FilteredBu2KpipiGamma_12103240/logs/FilteredBu2KpipiGamma.%j.out
#SBATCH -J FilteredBu2KpipiGamma
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH -A batch
#SBATCH -p batch
#SBATCH -t 16:00:00
#SBATCH --mem-per-cpu=2400


echo "-----START JOB at `date`-----"

set -e

# Setup work directory
myID=$SLURM_JOB_ID 
workdir=/scratch/$USER/$myID
mkdir -p $workdir
echo "Workdir "$workdir

function finish { 
  echo "Cleaning up"
  rm -rf "$workdir"
}
trap finish EXIT SIGTERM SIGXCPU SIGINT SIGKILL

# Where do I put the output?
mkdir -p $HOME/MCProd/FilteredBu2KpipiGamma_12103240

# Setup everything
#cp $myhome/MC/DecFiles/* $workdir/

cd $workdir

# Prepare conditions
echo "from Configurables import LHCbApp" >> Conditions.py
echo 'LHCbApp().DDDBtag   = "dddb-20130929-1"' >> Conditions.py
echo 'LHCbApp().CondDBtag = "sim-20130522-1-vc-mu100"' >> Conditions.py

#------------# 
#   MOORE    #
#------------#
(
cd $workdir
export CMTCONFIG=x86_64-slc5-gcc46-opt
source LbLogin.sh -c x86_64-slc5-gcc46-opt
source SetupProject.sh Moore v14r8p1 --use "AppConfig v3r164"
# Prepare special conditions
echo "from Gaudi.Configuration import *" > MooreConfiguration.py
echo "from Configurables import LHCbApp, Moore" >> MooreConfiguration.py
echo 'LHCbApp().DDDBtag   = "dddb-20130929-1"' >> MooreConfiguration.py
echo 'LHCbApp().CondDBtag = "sim-20130522-1-vc-mu100"' >> MooreConfiguration.py
echo 'Moore().DDDBtag   = "dddb-20130929-1"' >> MooreConfiguration.py
echo 'Moore().CondDBtag = "sim-20130522-1-vc-mu100"' >> MooreConfiguration.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Boole.digi' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> MooreConfiguration.py
echo "Moore().outputFile = 'Moore.dst'" >> MooreConfiguration.py
# Run
gaudirun.py $APPCONFIGOPTS/Moore/MooreSimProductionWithL0Emulation.py $APPCONFIGOPTS/Conditions/TCK-0x40990042.py $APPCONFIGOPTS/Moore/DataType-2012.py $APPCONFIGOPTS/L0/L0TCK-0x0045.py MooreConfiguration.py
)

#-------------# 
#   BRUNEL    #
#-------------#
(
cd $workdir
export CMTCONFIG=x86_64-slc5-gcc46-opt
source LbLogin.sh -c x86_64-slc5-gcc46-opt
source SetupProject.sh Brunel v43r2p7 --use "AppConfig v3r164"
# Prepare files
echo "from Gaudi.Configuration import *" >> Brunel-Files.py
echo "EventSelector().Input = [\"DATAFILE='PFN:./Moore.dst' TYP='POOL_ROOTTREE' OPT='READ'\"]" >> Brunel-Files.py
# Run
gaudirun.py $APPCONFIGOPTS/Brunel/DataType-2012.py $APPCONFIGOPTS/Brunel/MC-WithTruth.py $APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py Conditions.py Brunel-Files.py
)

echo "-----END JOB at `date`-----"

# EOF
