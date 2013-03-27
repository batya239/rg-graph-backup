#!/bin/sh
#set -x

N=8
#NODES=32:ppn=1
NODES=8:ppn=1
#N=8
NITER=2
SCRIPTDIR=`pwd`
LIB=/home/mkompan/libs/pvegas
MODEL=`cat modelN.txt`
MODELNAME=`echo $MODEL|sed 's/_phi/phi_/'`
METHOD='feynmanSDdotS_mpi'
DIR="/home/mkompan/work/rg-graph/$MODELNAME/$METHOD/$1/"


cd $DIR

if [ "x$2" == "x" ]; then POINTS=100000; else POINTS=$2; fi
if [ "x$3" == "x" ]; then DELTA=0.; else DELTA=$3; fi

for i in `ls *.run`; do
#~/submit-tp-vm -v openmpi -q long -j $i -f "`pwd`/$i $2 $N $NITER" -n $N -e "LD_LIBRARY_PATH=$LIBRARY_PATH:$LIB/" --debug

#~/tmp/qsub-integral-tp.sh $i $2 $N $NITER
echo  $i $POINTS $N $NITER $DELTA $NODES
sh $SCRIPTDIR/qsub-integral-tp.sh $i $POINTS $N $NITER $DELTA $NODES $DIR
done





