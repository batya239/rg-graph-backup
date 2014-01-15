#!/bin/bash

PWD1=`pwd`
echo $PWD1
for i in `ls -d GraphState Graphine RgGraphUtil RgGraphEnv Polynomial Reduction Phi4`; do
   cd $PWD1
   cd $i
   echo install $i
   A=`python setup.py install --user`
   echo $A
   echo
done;
