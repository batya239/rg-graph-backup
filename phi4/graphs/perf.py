#!/usr/bin/python
# -*- coding: utf8
import sys

from dummy_model import _phi3,_phi4
from graphs import Graph
import sympy
import conserv
import comb
import methods.feynman_tools

#from sympy.printing.ccode2 import ccode2


phi4=_phi4('dummy')

if len(sys.argv)==3:
    exec('from %s import save, compile, execute'%sys.argv[2])
else:
    exec('from feynman import save,compile, execute')

g1=Graph(sys.argv[1])
name=str(g1.GenerateNickel())
print name
g1.FindSubgraphs(phi4)

int_edges=g1._internal_edges_dict()
cons = conserv.Conservations(int_edges)
qi, qi2l = qi_lambda(cons, eqs)

det=methods.feynman_tools.det_as_lst(cons)

res=0

for term in det:
    sterm=1
    for term2 in term:
       ui=sympy.var('u_%s'%term2)
       sterm=sterm*ui
    res+=sterm
print res

#save(name,g1,phi4)

#compile(name,phi4)

#(res,err) = execute(name, phi4, neps=0)
#for i in range(len(res)):
#    print i, (res[i],err[i])

