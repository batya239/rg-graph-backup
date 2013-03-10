#!/usr/bin/python
# -*- coding: utf8


import sys
import re

import graph_state
import polynomial.sd_lib as sd_lib
import polynomial

import subgraphs
from dummy_model import _phi3_dyn, _phi4_dyn

import dynamics


def splitUA(varSet):
    u = list()
    a = list()
    for var in varSet:
        if isinstance(var, str) and re.match('^a.*', var):
            a.append(var)
        else:
            u.append(var)
    return set(u), set(a)


def deltaArg(varSet):
    return polynomial.poly(map(lambda x: (1, [x]), varSet))


model = _phi4_dyn("phi4_dyn_test")

filename = sys.argv[1]

exec ('import %s as data' % filename[:-3])

print data.graphName

gs = graph_state.GraphState.fromStr(data.graphName)
tVersion = data.tVersion

dG = dynamics.DynGraph(gs)
dG.FindSubgraphs(model)
subgraphs.RemoveTadpoles(dG)
Components = dynamics.generateCDET(dG, tVersion, model=model)
print str(gs)
print tVersion
#print "C = %s\nD = %s\nE = %s\nT = %s\n" % tuple(Components)
C, D, E, T = Components
#d=4-2*e


expr = C * D * E * T
print "C = %s\nD = %s\nE = %s\nT = %s\n" % (C, D, E, T)
#print expr

variables = expr.getVarsIndexes()
print "variables: ", variables
uVars, aVars = splitUA(variables)
delta_arg = deltaArg(uVars)

neps = model.target - dG.NLoops()

dynamics.save(model, expr, data.sectors, filename[:-3], neps)
dynamics.compileCode(model, filename[:-3], options=["-lm", "-lpthread", "-lpvegas", "-O2"])


# print
# print "-------------------"
# for sector, aOps in data.sectors:
#
#     sectorExpr = [sd_lib.sectorDiagram(expr, sector, delta_arg=delta_arg)]
#
#     for aOp in aOps:
#         sectorExpr = aOp(sectorExpr)
#     sectorExpr = map(lambda x: x.simplify(), sectorExpr)
#     check = dynamics.checkDecomposition(sectorExpr)
#     print sector, check
#     if "bad" in check:
#         print
#         print polynomial.formatter.format(sectorExpr, polynomial.formatter.CPP)
#         print
#
# #    sectorVariables = set(polynomial.formatter.formatVarIndexes(sectorExpr, polynomial.formatter.CPP))
# #    print sectorVariables
#
#
# #



