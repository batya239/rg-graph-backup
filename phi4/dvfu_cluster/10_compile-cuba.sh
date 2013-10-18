#!/bin/bash
NUM_THREADS=2
CUR_DIR=`pwd`
WORKDIR=$HOME'/work/rg-graph/phi_4_d2_s2/feynmanSDdotSF_mpi/'
#if !`ls $WORKDIR | grep SConstruct`
    cp $CUR_DIR/SConstruct.pvegas $WORKDIR
#if !`ls $WORKDIR | grep cubaCodeTemplate.py`
    cp $CUR_DIR/cubaCodeTemplate.py $WORKDIR
METHOD='cuhre'
cd $WORKDIR
for d in `ls -d */`
    do
        cd $d
        scons -j $NUM_THREADS -f ../SConstruct.pvegas
        cd ..
    done
cd $CUR_DIR
