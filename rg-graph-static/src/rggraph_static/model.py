#!/usr/bin/python
# -*- coding:utf8

#import sympy

class Model:
    """ Class represents necessary information about model
        LineTypes - dict of line types (for now - 1 record)
        NodeTypes - dict of vertex types
        subgraphs - list of lists of LineTypes?
    """
    def __init__(self, name_):
        self.name = name_
        self.line_types = dict()
        self.node_types = dict()
        self.subgraph_types = dict()
        self.k_nodetype_r1 = dict()
        self.dot_types = dict()
        
    def AddLineType(self, line_idx, **kwargs):
        """ propagator,directed,Graphviz
            propagator="1/(p*p+tau)", directed=0 (simple massive line)
            only for static!!! для динамики нужно оперировать полями
            Graphviz - additional options for vizualization, Ex. color="red"
        """
        if line_idx not in self.line_types:
            self.line_types[line_idx] = kwargs
        else:
            raise Exception, "LineType %s allready defined" %line_idx
        
    def AddNodeType(self, node_idx, **kwargs):
        """ Lines(types),Factor, graphviz
            Lines=[1,1,1], Factor=1 (simple phi3 vertex)
            Lines=[1,1], Factor=p1*p1 ( phi2 vertex with p^2 in it )
            Lines=[], Factor=1 (External node?)
            Graphviz - additional options for vizualization, Ex. color="red"

        """
        if node_idx not in self.node_types:
            self.node_types[node_idx] = kwargs
        else:
            raise Exception, "NodeType %s allready defined" %node_idx
    
    def AddSubGraphType(self, subgraph_idx, **kwargs):
        """ Lines(types), dim?? 
            K_nodetypeR1 - Maps  subgraph types to node types 
        """
        if subgraph_idx not in self.subgraph_types:
            self.subgraph_types[subgraph_idx] = kwargs
            if "K_nodetypeR1" in kwargs :
                self.k_nodetype_r1[subgraph_idx] = kwargs["K_nodetypeR1"]
        else:
            raise Exception, "SubGraphType %s allready defined" %subgraph_idx  

    def AddDotType(self, dot_idx, **kwargs):
        """ dim  
        """
        if dot_idx not in self.dot_types:
            self.dot_types[dot_idx] = kwargs
        else:
            raise Exception, "DotType %s allready defined,%s" %(dot_idx,self.dot_types)  

                
    def __str__(self):
        res = "Model Name = %s\n\nLine types:\n" %self.name
        for idxL in self.line_types:
            res = res + "\ttype %s : %s\n" %(idxL, self.line_types[idxL])
        res = res + " \nNode types:\n"
        for idxN in self.node_types:
            res = res + "\ttype %s : %s\n" %(idxN, self.node_types[idxN])
        res = res + " \nSubGraph types:\n"
        for idxS in self.subgraph_types:
            res = res + "\ttype %s : %s\n" %(idxS, self.subgraph_types[idxS])
        res = res + " \nDot types:\n"
        for idxD in self.dot_types:
            res = res + "\ttype %s : %s\n" %(idxD, self.dot_types[idxD])
        return res
        
