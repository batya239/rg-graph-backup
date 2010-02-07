#!/usr/bin/python
# -*- coding:utf8
import sys
from sympy import *
import rggraph_static as rggrf
import pydot

print dir(rggrf)
print dir(rggrf.Model)

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "moment"

var('p tau p1 K')

phi3=rggrf.Model("phi3")
phi3.AddLineType(1, propagator = 1/(p*p+tau), directed = 0)

phi3.AddNodeType(0, Lines = [],Factor = 1,Graphviz = "color=\"red\"")  #External Node
phi3.AddNodeType(1, Lines = [1, 1, 1], Factor = 1)
phi3.AddNodeType(2, Lines = [1, 1], Factor = p1 * p1) # nodes from Sigma subgraphs
phi3.AddNodeType(3, Lines = [1, 1 , 1], Factor = K )
phi3.AddNodeType(4, Lines = [1, 1], Factor = K )


phi3.AddSubGraphType(1, Lines = [1, 1, 1], dim = 0, K_nodetypeR1 = 3)
phi3.AddSubGraphType(2, Lines = [1, 1], dim = 2, K_nodetypeR1 = 4)

print phi3

G = rggrf.Graph(phi3)
G.LoadLinesFromFile(filename)
G.DefineNodes({})

for idxN in G.Nodes:
    print "idxN=",idxN, "type=", G.Nodes[idxN].Type, "Lines=",G.Nodes[idxN].Lines
for idxL in G.Lines:
    print "idxL=",idxL, "type=", G.Lines[idxL].Type, "In=",G.Lines[idxL].In, "Out=",G.Lines[idxL].Out , "Moment=",G.Lines[idxL].Momenta
    
G.SaveAsPNG("graph.png") 
print G.ExternalLines
print G.InternalLines
print

print G
print "subgraphs"
G.FindSubgraphs()
for i in range(len(G.subgraphs)):
    print "sub %s" %i
    print G.subgraphs[i]
#    print rggrf.visualization.Graph2dot(i)
    G.subgraphs[i].SaveAsPNG("sub%s.png" %i)
    
r1=rggrf.roperation.R1(G)
print "R1(G)"
for i in range(len(r1.terms)):
    print "term %s:"  %i
    print r1.terms[i].CTGraph
    print "\t term subgraphs:"
    for j in r1.terms[i].subgraphs:
        print "\t %s" %j
        
G.GenerateNikel()
    
    