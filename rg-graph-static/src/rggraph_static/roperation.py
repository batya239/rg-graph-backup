#!/usr/bin/python
# -*- coding: utf8

def ExtractSubgraphs( G, subgraph_list ):
    from graph import Graph, Line

    ctg_lines = set( G.lines.keys() )
    map_reduced_nodes = dict()
    node_types = G.GetNodesTypes()
    cur_node_idx=1000  # номер вершины на который будем заменять вершины текущего  подграфа.
    subgraph_map=dict()
    for idxS in subgraph_list:
        while ( cur_node_idx in node_types):
            cur_node_idx=cur_node_idx+1
#        print cur_node_idx, node_types, G.model.k_nodetype_r1, G.subgraphs[idxS].type
        node_types[ cur_node_idx ] = G.model.k_nodetype_r1[ G.subgraphs[idxS].type ]
        subgraph_map[cur_node_idx] = subgraph_list.index(idxS)

        # не факт что K_nodetype хорошее решение.
        
        ctg_lines = ctg_lines - G.subgraphs[idxS].internal_lines
        for idxN in G.subgraphs[idxS].internal_nodes:
            map_reduced_nodes[idxN] = cur_node_idx
        
    ct_graph=Graph(G.model)
    for idxL in ctg_lines:
        if G.lines[idxL].start in map_reduced_nodes:
            In = map_reduced_nodes[ G.lines[idxL].start ] 
        else:
            In = G.lines[idxL].start
        if G.lines[idxL].end in map_reduced_nodes:
            Out = map_reduced_nodes[ G.lines[idxL].end ]
        else:
            Out = G.lines[idxL].end
        ct_graph.AddLine( idxL, Line( G.lines[idxL].type, 
                                     In, Out, G.lines[idxL].momenta, 
                                     G.lines[idxL].dots ) )

# TODO: we must determine dims by power counting        
    ct_graph.DefineNodes(node_types, dim=G.dim )
    
# inherit subgraphs from original graph.
# order of subgraphs must be the same as in subgraph_list
    subgraphs=list()
    for idxS in subgraph_list:
        subgraphs.append(G.subgraphs[idxS])
        
    ct_graph.subgraphs = tuple(subgraphs)
    return (ct_graph , subgraph_map)    
        
    
    


class R1Term:
    """ CTGraph - counterterm graph (Graph class)
        SubgraphMap - Map Nodes of CTGraph with appropriate subgraph (dict) 
        subgraphs - tuple of subgraphs (each - Graph class)
    """
    def __init__( self, G, subgraph_list ):
        ( self.ct_graph, self.subgraph_map ) = ExtractSubgraphs( G, subgraph_list )
        self.subgraphs = tuple( [ G.subgraphs[idxS] for idxS in subgraph_list ] )
        
        t_lines = []
        for cur_graph in [self.ct_graph,]+ list(self.subgraphs):
            ext_moment_atoms = set([])
            for idxL in cur_graph.external_lines:
                ext_moment_atoms = (ext_moment_atoms | 
                                   set(cur_graph.lines[idxL].momenta.dict.keys()))
            for idxL in cur_graph.internal_lines:
                if len(set(cur_graph.lines[idxL].momenta.dict.keys()) &
                       ext_moment_atoms) == 0:
                    t_lines.append(idxL)
        self.unaffected_lines = tuple(t_lines)



class R1:
    def __init__( self, G ):

        def IsIntersect( G, subgraph_list ):
            res = False
            lineset=set([])
            int_sub_nodes=set([])
            for idx in subgraph_list:
#                print int_sub_nodes, idx, subgraph_list, G.subgraphs[idx].internal_nodes
                if len( int_sub_nodes & G.subgraphs[idx].internal_nodes ) == 0: # поиск общих вершин
                    int_sub_nodes = int_sub_nodes | G.subgraphs[idx].internal_nodes
                else:
                    return True

                if len( lineset & G.subgraphs[idx].internal_lines) == 0: # поиск общих линий
                    lineset = lineset | G.subgraphs[idx].internal_lines
                else:
                    return True
                                    
            return res

        def xuniqueCombinations( items, n):
            if n == 0: yield [ ]
            else:
                for i in xrange( len( items ) ):
                    for cc in xuniqueCombinations( items[ i+1 : ], n-1 ):
                        yield [ items[ i ] ] + cc            
        
        self.terms = [ ]
        self.terms.append( R1Term( G, [ ] ) )
        for idx in range(1, len( G.subgraphs ) + 1 ):
            
            for subgraph_list in xuniqueCombinations( range( len( G.subgraphs ) ), idx ):
                if not IsIntersect( G, subgraph_list ):
                    self.terms.append( R1Term( G, subgraph_list ) )
                    
        t_set = set(self.terms[0].unaffected_lines)
        for idxRT in self.terms[1:]:
            t_set = t_set &  set(idxRT.unaffected_lines)
        self.factorization = t_set
        
        for idxRT in self.terms:
            idxRT.factorization = t_set
            
                    
    def SaveAsPNG(self, filename):
        from visualization import R12dot
#        import pydot
        gdot=R12dot(self)
        gdot.write_png(filename,prog="dot")            


class Factorized:
    
    def __init__(self, factor_, other_):
        self.factor = factor_
        self.other = other_
        
    def __add__(self, other):
        from sympy import pretty_print
        if isinstance(other,Factorized):
            if self.factor/other.factor <> 1:
                pretty_print(self.factor)
                pretty_print(other.factor)
                raise ValueError, "can't add 2 factorized equations with different factor"
            else:
                return Factorized(self.factor, self.other + other.other)
        elif other == 0 :
            return Factorized(self.factor, self.other)
        else:
            pretty_print(self.factor)
            pretty_print(other.factor)
            raise ValueError , "can add Factorized instance only with Factorized or zero "
        
    def __radd__(self,other):
        if other == 0: 
            return Factorized(self.factor, self.other)
        else: 
            raise ValueError , "can radd Factorized instance only with Facorized or zero "
        
    def __sub__(self, other):
        if self.factor/other.factor <> 1:
            raise ValueError, "can't substract 2 factorized equations with different factor"
        else:
            return Factorized(self.factor, self.other - other.other)
    def __neg__(self):
        return Factorized(self.factor, -self.other)
    
    def __mul__(self, other):
        if isinstance(other,Factorized):
            return Factorized(self.factor*other.factor, self.other*other.other)

    def pprint(self):
        from sympy import pretty_print
        pretty_print(self.factor)
        pretty_print(self.other)


class Delta:
    pass