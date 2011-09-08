from lines import Line
from nodes import Node
import moments

class _generic_model: 
    def __init__( self, name):
        self.name=name
        """ add model specific definitons here        
        """
    def Dim( self, obj ):
        """ using generic _Dim function
        """
        return _Dim(self,obj)

    def SetTypes(self, graph):
        """ using generic _setType
        """
        _SetTypes(graph)
    
    def GenerateMoment(self,graph):
        """ at present time GenerateMoment uses moments.Generic function
        """
        return moments.Generic(self,graph)

    def dTau(self, graph):
        """ applies \partial_{m^2}  on graph (m^2\equiv\tau). 
            returns list of graphs with modifiers
        """
        if 'tau' not in self.modifiers_dim:
            raise ValueError, "there is no tau modifier in model"
        else:
            return _dTau(graph)

    def propagator(line):
        return 1/(line.momenta.Squared()+1)

    def vertex(node):
        return sympy.Number(1)


class _phi3(_generic_model):
    def __init__( self , name):
        self.name=name
        self.space_dim=6
        self.lines_dim={1:-2}
        self.modifiers_dim={'tau':-2,'p':-1}
        self.nodes_dim={1:0}
        self.checktadpoles=False
        
    
class _phi4(_generic_model):
    def __init__( self , name):
        self.name=name
        self.space_dim=4
        self.lines_dim={1:-2}
        self.modifiers_dim={'tau':-2,'p':-1}
        self.nodes_dim={1:0}
        self.checktadpoles=True


def _SetTypes(graph):
    """ set types for graph nodes and lines ( this implementation may be used only for models with 1 type of lines and 1 type of nodes)
    """
    for line in graph.xInternalLines():
        line.type=1
    for node in graph.xInternalNodes():
        node.type=1

def _Dim(model,obj):
    """ dimension calculation for graph  (nodes, lines and its modifiers)
    """
    if obj.type==None:
        raise ValueError , "cant determine Dim: type is None"
    if isinstance( obj, Line ):
        dim=model.lines_dim[obj.type]
    elif isinstance( obj, Node):
        dim=model.nodes_dim[obj.type]
    else:
        raise ValueError, 'unknown object'
    if obj.modifiers<>None:
        for mod in obj.modifiers:
            dim+=model.modifiers_dim[mod]
    return dim

def _dTau(graph):
    """ places tau modifier on each  graph line sequentlially
    """
    res=list()
    for line in graph.xInternalLines():
        idx=graph.Lines().index(line)
        g=graph.Clone()
        newline=g._Line(idx)
        newline.AddModifier("tau")
        res.append(g)
    return res

