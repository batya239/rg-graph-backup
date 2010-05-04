#!/usr/bin/python
# -*- coding: utf8
'''
Created on Feb 17, 2010

@author: mkompan

definition of phi3 model in terms of rggraph_static
'''

import sympy
import os
import sys
import rggraph_static as rggrf
import copy
import re

#definitions of propagators, node factors, dot actions, and K operation 

def AddStrech(Obj,strech, atoms_str):
    if isinstance(Obj,(rggrf.Line,rggrf.Node)):
        if 'strechs' not in Obj.__dict__:
            Obj.strechs=dict()   
        if strech not in Obj.strechs: 
            Obj.strechs[strech]=atoms_str
        else:
            raise ValueError, "Strech variable %s allready present in object"%strech
    else:
        raise NotImplementedError, "Do not know how to strech object: %s"%type(Obj)    

def AddDiff(Obj,var):
    if isinstance(Obj,(rggrf.Line,rggrf.Node)):
        if 'diffs' not in Obj.__dict__:
            Obj.diffs=list()   
        Obj.diffs.append(var)
    else:
        raise NotImplementedError, "Do not know how to diff object: %s"%type(Obj) 

def propagator(Line):
    tau=sympy.var('tau')
    res = 1 / (Line.momenta.Squared() + tau)
    if 'strechs' in Line.__dict__:
        for strech in Line.strechs:
            res = rggrf.StrechAtoms(res, Line.strechs[strech], strech, ignore_present_strech = False)
    if 'diffs' in Line.__dict__:
        for diff in Line.diffs:
            res = res.diff(sympy.var(diff))
    for idxD in Line.dots:
        for idx in range(Line.dots[idxD]):
            res = Line.model.dot_types[idxD]["action"](propagator=res)
    return res

def IsDotted(Node):
    if "dots" in Node.__dict__:
        if len(Node.dots.keys())>1:
            raise NotImplementedError, "Invalid node dots : %s"%Node.dots
        elif len(Node.dots.keys())==1:
            if 1 not in Node.dots.keys():
                raise NotImplementedError, "Invalid node dots : %s"%Node.dots
            if Node.dots[1]==1:
                return True
            else:
                raise NotImplementedError, "Invalid node dots : %s"%Node.dots
        else:
            return False
    return False
    
def feynman4(Node):

    #print "f4:%s "%Node.type
    if Node.type == 4:
        sqmoment = Node.lines_dict.values()[0].momenta.Squared()
        parent_subgraph = Node.parent_subgraph
#        print Node.str_nickel
        if Node.str_nickel in model.feynman:
            if IsDotted(Node):
                exec(model.feynman[Node.str_nickel][1])
#                print res
            else:
                exec(model.feynman[Node.str_nickel][0])
#                print res
    elif Node.type == 3:
        if Node.str_nickel in model.feynman:
            node_intersect = (set(Node.lines_dict.values()[0].Nodes()) & set(Node.lines_dict.values()[1].Nodes()) &set(Node.lines_dict.values()[2].Nodes()) )
            if len(node_intersect)<>1:
                raise ValueError, "Cant determine Node idx: %s"%node_intersect
            else:
                node_idx = list(node_intersect)[0]
            if Node.lines_dict.values()[0].end == node_idx:
                k1 = Node.lines_dict.values()[0].momenta
            else:    
                k1 = - Node.lines_dict.values()[0].momenta
            if Node.lines_dict.values()[1].end == node_idx:
                k2 = Node.lines_dict.values()[1].momenta
            else:    
                k2 = - Node.lines_dict.values()[1].momenta
            if Node.lines_dict.values()[2].end == node_idx:
                k3 = Node.lines_dict.values()[2].momenta
            else:    
                k3 = - Node.lines_dict.values()[2].momenta
            if len(k1.dict)==0:
                k2=k1
            k2xk3=k2*k3
            k2sq = k2.Squared()
            k3sq = k3.Squared()

            parent_subgraph = Node.parent_subgraph
            if IsDotted(Node):
                exec(model.feynman[Node.str_nickel][1])
#                print res
            else:
                exec(model.feynman[Node.str_nickel][0])
#                print res

    else:
        raise ValueError, "Invalid node type: %s " %Node.type
    res = rggrf.roperation.Factorized(1, res)
    if 'strechs' in Node.__dict__:
        for strech in Node.strechs:
            res = rggrf.StrechAtoms(res, Node.strechs[strech], strech, ignore_present_strech = False)
    if 'diffs' in Node.__dict__:
        for diff in Node.diffs:
            res = rggrf.roperation.Factorized(1, (res.factor*res.other).diff(sympy.var(diff)))
    return res
    

def node_factor(Node):
    if Node.type == 0:
        res = rggrf.roperation.Factorized(1, 1) 
    elif Node.type == 1:
        res = rggrf.roperation.Factorized(1, 1)
    elif Node.type == 2:
        moment = Node.lines_dict.values()[0].momenta
        res = rggrf.roperation.Factorized(1, moment.Squared())

    else:
        raise ValueError, "Invalid node type: %s " %Node.type
    if 'strechs' in Node.__dict__:
        for strech in Node.strechs:
            res = rggrf.StrechAtoms(res, Node.strechs[strech], strech, ignore_present_strech = False)
    if 'diffs' in Node.__dict__:
        for diff in Node.diffs:
            res = rggrf.roperation.Factorized(1, (res.factor*res.other).diff(sympy.var(diff)))
    if 'dots' in Node.__dict__:
        for idxD in Node.dots:
            for idx in range(Node.dots[idxD]):
                res = rggrf.roperation.Factorized(1, Node.model.dot_types[idxD]["action"](propagator=res.factor*res.other))
    return res

def moment_serialize(Moment, preserve_sign=False):
    t_moment=Moment
    atoms = t_moment.dict.keys()
    atoms.sort()
    if len(atoms)>0:
        if not preserve_sign and Moment.dict[atoms[0]] <0:
            t_moment= -t_moment
            atoms = t_moment.dict.keys()
            atoms.sort()
    res = ""
    for atom in atoms:
        res = res + str((atom, t_moment.dict[atom]))
    return res

def strech_serialize(strechs):
    res = ""
    keys = strechs.keys()
    keys.sort()
    for key in keys:
        vars = strechs[key]
        vars.sort()
        res = res + str((key,vars))
    return res

def diff_serialize(diffs):
    
    import copy
    keys = copy.copy(diffs)
    keys.sort()
    return str(keys)

def dot_serialize(dots):
    res = ""
    for dot in dots:
        res = res + str(("dot%s"%dot, dots[dot]))
    return res

def line_serialize(Line, include_dots=True): 
    s_moment = "moment:(%s)"%moment_serialize(Line.momenta, preserve_sign=False)
    
    if "strechs" in Line.__dict__:
        s_strechs = "strechs:(%s)"%strech_serialize(Line.strechs)
    else:
        s_strechs = "strechs:()"
        
    if "diffs" in Line.__dict__:
        s_diffs = "diffs:(%s)"%diff_serialize(Line.diffs)
    else:
        s_diffs = "diffs:()"
    
    s_dots = "dots:(%s)"%dot_serialize(Line.dots)
    if include_dots:
        return "line%s(%s,%s,%s,%s)"%(Line.type,s_moment,s_strechs,s_diffs,s_dots)
    else:
        return "line%s(%s,%s,%s)"%(Line.type,s_moment,s_strechs,s_diffs)

def node_serialize(Node):
    if Node.type == 0:
        s_moment = "" 
    elif Node.type == 1:
        s_moment = ""
    elif Node.type == 2:
        s_moment = moment_serialize(Node.lines_dict.values()[0].momenta, preserve_sign=False)
    elif Node.type == 3:
        s_moment = [moment_serialize(Node.lines_dict.values()[0].momenta, preserve_sign=False),moment_serialize(Node.lines_dict.values()[0].momenta, preserve_sign=False),moment_serialize(Node.lines_dict.values()[0].momenta, preserve_sign=False)]
        s_moment.sort()
    elif Node.type == 4:
        s_moment = moment_serialize(Node.lines_dict.values()[0].momenta, preserve_sign=False)
    else:
        raise ValueError, "Invalid node type: %s " %Node.type
    if "strechs" in Node.__dict__:
        s_strechs = "strechs:(%s)"%strech_serialize(Node.strechs)
    else:
        s_strechs = "strechs:()"
        
    if "diffs" in Node.__dict__:
        s_diffs = "diffs:(%s)"%diff_serialize(Node.diffs)
    else:
        s_diffs = "diffs:()"
    
    if "dots" in Node.__dict__:
        s_dots = "dots:(%s)"%dot_serialize(Node.dots)
    else:
        s_dots = "dots:()"
    
    return "node%s(%s,%s,%s,%s)"%(Node.type,s_moment,s_strechs,s_diffs,s_dots)

def graph_serialize(G):
    s_graph_dict=dict()
    for idxL in G.internal_lines:
        s_line=line_serialize(G.lines[idxL])
        if s_line in s_graph_dict.keys():
            s_graph_dict[s_line] =  s_graph_dict[s_line] + 1
        else:
            s_graph_dict[s_line] = 1
            
    for idxN in G.internal_nodes:
        s_node=node_serialize(G.nodes[idxN])
        if s_node in s_graph_dict.keys():
            s_graph_dict[s_node] =  s_graph_dict[s_node] + 1
        else:
            s_graph_dict[s_node] = 1
    
    keys = s_graph_dict.keys()
    keys.sort()
    
    res= ""
    for key in keys:
        res = res + str ((key, s_graph_dict[key]))
    
    return res
        
def dot_action(**kwargs):
    tau = sympy.var('tau')
    propagator=kwargs["propagator"]
    return propagator.diff(tau)

def FindExtMomentAtoms(G):
    res=set(list())
    for ext_line in G.external_lines:
        res=res | set(G.lines[ext_line].momenta.dict.keys())
    return list(res)



def ExpandScalarProdsAndPrepareFactorized(factorized_expr,debug=False):
    return rggrf.roperation.Factorized(ExpandScalarProdsAndPrepare(factorized_expr.factor,debug), 
                      ExpandScalarProdsAndPrepare(factorized_expr.other,debug))

def ExpandScalarProdsAndPrepare(expr_,debug=False):
    if isinstance(expr_,rggrf.roperation.Factorized):
        rggrf.utils.print_debug( "WARNING!!! Factorizied object passed to ExpandScalarProdsAndPrepare",debug)
        expr = expr_.factor*expr_.other
    else:
        expr = expr_ 
    import re as regex
    try:
        atoms = expr.atoms()
    except:
        rggrf.utils.print_debug( "WARNING!!!! %s passed to ExpandScalarProdsAndPrepare" %type(expr),debug)
        return expr
    t_expr = ExpandScalarProds(expr,debug=False)
    
    #Prepare p=1, tau=1
    p=sympy.var('p')
    tau=sympy.var('tau')
    t_expr = t_expr.subs(p,1).subs(tau,1)
    return t_expr            

def ExpandScalarProds(expr_,debug=False):
    if isinstance(expr_,rggrf.roperation.Factorized):
        rggrf.utils.print_debug( "WARNING!!! Factorizied object passed to ExpandScalarProds",debug)
        expr = expr_.factor*expr_.other
    else:
        expr = expr_ 
    import re as regex
    try:
        atoms = expr.atoms()
    except:
        rggrf.utils.print_debug( "WARNING!!!! %s passed to ExpandScalarProds" %type(expr),debug)
        return expr
    t_expr = expr
    for atom in atoms:
        reg = regex.match("^(.+)x(.+)$",str(atom))
        if reg :
            atom1 = sympy.var(reg.groups()[0])
            atom2 = sympy.var(reg.groups()[1])
            t_expr = t_expr.subs(atom,atom*atom1*atom2)
    #Prepare p=1, tau=1
#    p=sympy.var('p')
#    tau=sympy.var('tau')
#    t_expr = t_expr.subs(p,1).subs(tau,1)
    return t_expr            


def FindLinesWithAtoms(G,atoms):
    lines_list=list()
    for idxL in G.internal_lines:
        if len(set(atoms) & set(G.lines[idxL].momenta.dict.keys()))>0:
            lines_list.append(idxL)
    return lines_list

def FindExtMomentPath(G,atoms):
    ext_moment_path=list()
    path_lines=FindLinesWithAtoms(G,atoms)
    for line in path_lines:
        ext_moment_path.append((line,"L"))
        for node in G.lines[line].Nodes():
            if G.nodes[node].type in [2,3,4] and (node,"N") not in ext_moment_path:
                ext_moment_path.append((node,"N"))
    return ext_moment_path

def compare_graphs(graph1,graph2):
    if len(graph1.internal_lines) < len(graph2.internal_lines):
        return 1
    elif len(graph1.internal_lines) == len(graph2.internal_lines):
        return 0
    else: 
        return -1

def subgraph_dim_with_diff(G,subgraph):
    dim = subgraph.dim
    for idxL in subgraph.internal_lines:
        if "diffs" in  G.lines[idxL].__dict__:
            dim = dim  - len(G.lines[idxL].diffs)
    for idxN in subgraph.internal_nodes:
        if "diffs" in  G.nodes[idxN].__dict__:
            dim = dim  - len(G.nodes[idxN].diffs)
    return dim

def checkdim_and_sort_subgraphs(G):
    res = list()
    for subgraph in G.subgraphs:
#        print "sub:%s,dim1:%s,dim2:%s\n"%(subgraph.internal_lines,subgraph.dim, subgraph_dim_with_diff(subgraph))
        
        dim = subgraph_dim_with_diff(G,subgraph)
        if dim >= 0:
            res.append(subgraph)
    res.sort(compare_graphs)
    return res
            
    


def K_nR1(G, N, Kres=dict(), debug=False):
    debug_level = 1
    ext_strech_var_str=None
#generate diffs for external moment, and appropriate strechs
    if N==0:
        diffs=[None,]
        extra_diff_multiplier = 1.
    elif N==2:
        extra_diff_multiplier = 0.5
        ext_moment_atoms_str = FindExtMomentAtoms(G)
        if len(ext_moment_atoms_str)==1:
            ext_strech_var_str = "%s_strech_var"%ext_moment_atoms_str[0]
            ext_moment_path = [(i[0],i[1],ext_strech_var_str) for i in FindExtMomentPath(G,ext_moment_atoms_str)]
            
            if debug and debug_level>0:
                print
                print ext_moment_path
                print
                
            for idx in ext_moment_path:
#                print idx,
                if idx[1]=="L":
                    obj = G.lines[idx[0]]
                elif idx[1]=="N":
                    obj = G.nodes[idx[0]]
                model.AddStrech(obj, ext_strech_var_str, ext_moment_atoms_str)
#                print obj.strechs
#                print
            diffs = [i for i in rggrf.utils.xSelections(ext_moment_path,N)]
                                    
        else:
            raise ValueError, "no or complex external momenta, atoms: %s"%ext_moment_atoms_str
    else:
        raise ValueError, " Unknown operation :  K%s"%N 
    G_list = list()
    for diff in diffs:
        cur_G=G.Clone()
        if diff == None:
            cur_G.extra_strech_multiplier=1.
            G_list.append(cur_G)
        else:
#            print
#            print diff
            for idx in diff:
                    if idx[1]=="L":
                        obj = cur_G.lines[idx[0]]
                    elif idx[1]=="N":
                        obj = cur_G.nodes[idx[0]]
                    model.AddDiff(obj, idx[2])
            cur_G.extra_strech_multiplier=1.
            cur_G.FindSubgraphs()
            #print diff,len(cur_G.subgraphs)
            G_list.append(cur_G)    

#generate diffs and strechs for subgraphs 

    
    stop = False
    new_G_list=G_list
    while (not stop):
        stop = True
        G_list=new_G_list
        new_G_list=list()
        for cur_G in G_list:
            if debug:
                print 
                print "serial:", graph_serialize(cur_G)                        
            cur_G.FindSubgraphs()   
#            print "   -----"     
#            for sub in cur_G.subgraphs:
#                print "      sub %s, dim1:%s, dim2:%s"%(sub.internal_lines, sub.dim, subgraph_dim_with_diff(cur_G, sub))
                
            subgraphs = checkdim_and_sort_subgraphs(cur_G)
            if debug:
                print 
                print "   number of subgraphs:%s" %len(subgraphs)
                for sub in subgraphs:
                    print "      sub %s, dim1:%s, dim2:%s"%(sub.internal_lines, sub.dim, subgraph_dim_with_diff(cur_G, sub))
                    
            if len(subgraphs)>0:
                stop = False
                subgraph = subgraphs[0] 
                sub_ext_atoms_str = FindExtMomentAtoms(subgraph)
                strech_var_str = "a"
                int_lines = list(subgraph.internal_lines)
                int_lines.sort()
                for idxL in int_lines:
                    strech_var_str = strech_var_str + "_%s"%idxL
                sub_ext_path = [(i[0],i[1],strech_var_str) for i in FindExtMomentPath(subgraph, sub_ext_atoms_str)]
                for idx in sub_ext_path:
                    if idx[1]=="L":
                        obj = cur_G.lines[idx[0]]
                    elif idx[1]=="N":
                        obj = cur_G.nodes[idx[0]]
                    model.AddStrech(obj, strech_var_str, sub_ext_atoms_str)
                degree = subgraph_dim_with_diff(G, subgraph) +1    
                if degree<=0:
                    raise ValueError, "irrelevant graph!!"
                sub_diffs = [i for i in rggrf.utils.xSelections(sub_ext_path,degree)]
                strech_var = sympy.var(strech_var_str)
                if degree>1: 
                    cur_G.extra_strech_multiplier = cur_G.extra_strech_multiplier * (1.-strech_var)**(degree-1.)/sympy.factorial(degree-1)
                for diff in sub_diffs:
                    new_G=cur_G.Clone()
                    if diff == None:
                        raise ValueError, "diff can't be None" 
                    else:
                        
                        for idx in diff:
                            if idx[1]=="L":
                                obj = new_G.lines[idx[0]]
                            elif idx[1]=="N":
                                obj = new_G.nodes[idx[0]]
                            model.AddDiff(obj, idx[2])
                        new_G_list.append(new_G)
            else:
                new_G_list.append(cur_G)                 
                

    res_dict=Kres    
    for cur_G in G_list: 
        s_graph=graph_serialize(cur_G)
        if debug: 
            print
            print s_graph
            print
        
        if s_graph in res_dict.keys():
            res_dict[s_graph] = (res_dict[s_graph][0], res_dict[s_graph][1] + 1)
        else:
            t_res = rggrf.roperation.Factorized(1,extra_diff_multiplier*cur_G.extra_strech_multiplier)
#            print t_res.other
            for idxL in cur_G.internal_lines:
                curline=cur_G.lines[idxL]
                prop = curline.Propagator()
                if debug and debug_level > 0:
                    print "Line %s: "%idxL
                    sympy.pretty_print(prop)
                    
                t_res.other = t_res.other * prop
            
            for idxN in cur_G.internal_nodes:
                curnode = cur_G.nodes[idxN]
                
                factor = curnode.Factor()
                
                if debug and debug_level > 0:
                    print "Node %s type %s: "%(idxN, cur_G.nodes[idxN].type)
                    sympy.pretty_print(factor.other*factor.factor)
                    
                t_res = t_res * factor
                
            if ext_strech_var_str <>None:
                strech_var = sympy.var(ext_strech_var_str)
                try:
                    atoms = t_res.factor.atoms()
                except:
                    pass
                else:
                    t_res.factor = t_res.factor.subs(strech_var,0)
                try:
                    atoms = t_res.other.atoms()
                except:
                    pass
                else:
                    t_res.other = t_res.other.subs(strech_var,0)
            
            if debug:
                sympy.pretty_print(t_res.factor*t_res.other)

            res_dict[s_graph]=(t_res, 1)
#    res=list()
#    for key in res_dict:
#        (t_res,t_cnt) = res_dict[key]
#        res.append(t_res*rggrf.roperation.Factorized(1,t_cnt))    
#    print
#    print len(res)
#    print

    if debug:
        print
        for key in res_dict:
            print "key:%s\n expr:%s\nfactor:%s\n\n"%(key,res_dict[key][0].factor*res_dict[key][0].other,res_dict[key][1])

    return res_dict
            
        
        
            
        
    
def L_dot(G, progress=None,debug=False):
    if progress <>  None:
        (progressbar,maxprogress) = progress
        step = float(maxprogress)/(len(G.internal_lines)+len(G.internal_nodes))
        cur_progress = progressbar.currval
    Kres=dict()
    for idxL in G.internal_lines:
        cur_G=G.Clone()
        cur_G.lines[idxL].dots[1] = 1
        #cur_G.DefineNodes(G.GetNodeTypes)
        cur_G.FindSubgraphs()
#        cur_r1.SaveAsPNG("test.png")
    
        if len(G.external_lines) == 2:
            Kres = K_nR1(cur_G, 2, Kres, debug)
        elif len(G.external_lines) == 3:
            Kres = K_nR1(cur_G, 0, Kres, debug)
        else:
            raise ValueError, "unknown graph type"
        progressbar.update(cur_progress+step)
        cur_progress = progressbar.currval
    
    #print "=========== NODES =============="
    
    for idxN in G.internal_nodes:
        if "dots" not in G.nodes[idxN].__dict__:
            G.nodes[idxN].dots=dict()
        if not G.nodes[idxN].type in [3,4]:
            progressbar.update(cur_progress+step)
            cur_progress = progressbar.currval
            continue
        cur_G=G.Clone()
        cur_G.nodes[idxN].dots[1] = 1
        cur_G.FindSubgraphs()
#        print "subgraphs:", cur_G.subgraphs
        if len(G.external_lines) == 2:
            Kres = K_nR1(cur_G, 2, Kres, debug)
        elif len(G.external_lines) == 3:
            Kres = K_nR1(cur_G, 0, Kres, debug)
        else:
            raise ValueError, "unknown graph type"
        progressbar.update(cur_progress+step)
        cur_progress = progressbar.currval
    
    res=list()
    for key in Kres.keys():
        (t_res,t_cnt) = Kres[key]
        res.append(t_res*rggrf.roperation.Factorized(1,t_cnt))        
    return res


def feynman_reduce(G):
    cur_G = G.Clone()
    nodetypes = cur_G.GetNodesTypes()
    nodes_to_remove=set()
    linesets_to_remove=list()
    for idxN in cur_G.internal_nodes:
        node = cur_G.nodes[idxN]
        if node.type == 2:
            if idxN in nodes_to_remove:
                continue
            else:
                t_lines_set = set(node.Lines())
                found = False
                for lineset in linesets_to_remove:
                    if len(t_lines_set & lineset) >0:
                        lineset = lineset or t_lines_set
                        found = True
                if not found:
                    linesets_to_remove.append(t_lines_set)
                nodes_to_remove = nodes_to_remove | set([idxN,])
                
#    print linesets_to_remove
    phi2_terms=list()
    for lineset in linesets_to_remove:
        nodes = list()
        for idxL in lineset:
            nodes = nodes + list(set(cur_G.lines[idxL].Nodes())-nodes_to_remove)
        if len(nodes)>2:
#            print nodes_to_remove
            raise ValueError, "found more then 2 nodes for one line! lineset: %s, nodes: %s"%(lineset,nodes)
        line = cur_G.lines[list(lineset)[0]]
        new_dots=dict()
        for idxL in list(lineset):
            if len(cur_G.lines[idxL].dots)<>0:
                for dot in cur_G.lines[idxL].dots:
                    if dot in new_dots:
                        new_dots[dot] = new_dots[dot] + cur_G.lines[idxL].dots[dot]
                    else:
                        new_dots[dot] =  cur_G.lines[idxL].dots[dot]
        for idxL in list(lineset)[1:]:
            del cur_G.lines[idxL]
        line.start = nodes[0]
        line.end = nodes[1]
        line.dots = new_dots
        phi2_terms.append((list(lineset)[0],len(lineset)-1))
    cur_G.DefineNodes(nodetypes)
#    cur_G.GenerateNickel()
    cur_G.phi2_terms = phi2_terms
    #print cur_G.nickel, phi2_terms
    return cur_G
    
def L_dot_feynman(F):
    def monom_coeff(F,monom, symbols):
        res = sympy.Number(1)
        eps = sympy.var('e')
        for idx in range(reduce(lambda x,y:x+y, monom)):
            res  = res * (idx+1 + F.n *eps/sympy.Number(2))
        for idx1 in range(len(monom)):
            for idx2 in range(monom[idx1]):
                res = res / (F.terms[F.reverse_u_map[symbols[idx1]]].lambd+idx2)
        return res
    
    def QForm(F_):
        u = dict()
        Q = 0
        cnt = 0
        for key in F_.terms:
            u[cnt] = sympy.var('u%s'%cnt)
            term = F_.terms[key]
#            Q = Q + u[idxT]*(term.line.momenta.Squared() + 1)
            Q = Q + u[cnt]/term.line.Propagator()
            cnt = cnt + 1     
        Q=ExpandScalarProds(Q).subs(sympy.var('tau'),1)
        
        #remove scalar prods q1xq2 pxq1 ...
        for atom in Q.atoms():
            if re.search('x',str(atom)):
                Q = Q.subs(atom,1)
        
        M=sympy.matrices.Matrix(F_.n,F_.n, lambda i,j:0)
        A=sympy.matrices.Matrix([0 for i in range(F_.n)])
        C=Q
        for i in range(F_.n):
            qi=sympy.var(F_.internal_atoms[i])
            C=C.subs(qi,0)
            A[i] = Q.diff(qi)/sympy.Number(2)
            for j in range(F_.n):
                qj=sympy.var(F_.internal_atoms[j])
                A[i]=A[i].subs(qj,0)
                if i>=j:
                    M[i,j] = Q.diff(qi).diff(qj)/sympy.Number(2)
                    if i<>j:
                        M[j,i] = M[i,j]

        

        e = sympy.var('e')
        print F_.alpha,(F_.graph.model.space_dim - e)/2
        if M.shape == (1,1):
            M_cofactormatrix = sympy.matrices.Matrix([sympy.Number(1)])
        else:
            M_cofactormatrix = M.cofactorMatrix()
        F = (C*M.det()-(A.T*(M_cofactormatrix*A))[0])

        
        F_s = F
        ext_moment_strech = sympy.var("p_strech")
        for str_atom in F_.external_atoms:
            atom = sympy.var(str_atom)
            F_s = F_s.subs(atom, atom*ext_moment_strech)
        
        
        print " F_s = ",F_s
        F_.B = F_s.subs(ext_moment_strech,0)
        F_.D = F_s.diff(ext_moment_strech).diff(ext_moment_strech).subs(ext_moment_strech,0)/sympy.Number(2)    



        F_m = 1
        for key in F_.terms:
            term = F_.terms[key]
            F_m = F_m * F_.u_map[key]**(term.lambd-1) 
        F_m = F_m * M.det()**(-(sympy.Number(int(F_.graph.model.space_dim))-e)/2-(F_.n*(sympy.Number(int(F_.graph.model.space_dim)) - e)/2 - F_.alpha))
        F_.E = F_m
        
    def L_n(F):
        
        ext_moment = sympy.var('p')
        e=sympy.var('e')
        sympy.var('E B D')
        t_res = (F.Gammas() * (B + ext_moment**2 * D) ** 
                 (F.n * (sympy.Number(int(F.graph.model.space_dim)) 
                            - e)/2 - F.alpha))
        print t_res
#        t_res = t_res.subs(E,F.Gammas())
        
        d_res = t_res
        t_res = t_res.subs(ext_moment,0)            
        for i in range(F.graph.dim+1):
            t_res = d_res.subs(ext_moment,0)
            d_res = d_res.diff(ext_moment)/(i+1)
        
            
        print t_res, "dim = ", F.graph.dim
        
        res = 0
        d_res = t_res
        
        if reduce(lambda x,y: x or y, 
                  map(lambda x: (str(x)=='inf') or (str(x)=='-inf') or (str(x)=='+inf'), 
                      d_res.expand().subs(e,0).atoms())):
            raise NotImplementedError, "Series on eps includes 1/eps term"
        print d_res.expand().subs(e,0), d_res.expand().subs(e,0).atoms()
        print "-----------------"
        for i in range(F.graph.model.target - F.graph.NLoops()+1):
            print e**i*d_res.expand().subs(e,0)
            res = res+e**i*d_res.expand().subs(e,0)
            d_res = d_res.diff(e)/(i+1)
        return res
            
        
    phi2_terms = dict()
    for (idxL,cnt) in F.graph.phi2_terms:
        phi2_terms[F.line_map[idxL]] = cnt
    
    F.u_map = dict()
    F.reverse_u_map = dict()
    lambda_map = dict()
    cnt=0
    for idxT in F.terms:
        F.u_map[idxT] = sympy.var('u%s'%cnt)
        F.reverse_u_map[F.u_map[idxT]] = idxT
        lambda_map[idxT] = sympy.var('lambda%s'%cnt)
        cnt = cnt + 1
        
    t_phi2_part = 1
    
    for key in phi2_terms:
        t_phi2_part = t_phi2_part * (1-F.u_map[key])**phi2_terms[key]
        
    t_phi2_part = t_phi2_part.expand().as_poly()
    symbols = t_phi2_part.symbols
    monoms = t_phi2_part.monoms
    coeffs = t_phi2_part.coeffs
    
    phi2_part = list()
    for idxM in range(len(monoms)):
        monom = monoms[idxM]
        coeff = coeffs[idxM]
        term = coeff
        for idxS in range(len(symbols)):
            symbol = symbols[idxS]
            term = term * symbol ** monom[idxS]
        term = term * monom_coeff(F, monom, symbols)
        phi2_part.append(term)
        
    print phi2_part, F.Gammas()
    
    QForm(F)
    print
    print "F.B = ", F.B
    print
    print "F.D = ", F.D
    print
    print "F.E = ",F.E
    print    
    print L_n(F)
        
    
            
    
            
           
# model initialization
model=rggrf.Model("phi3R1")
model.space_dim = 6.
# definition of line types (1 line type)
model.AddLineType(1, propagator=propagator, directed=0, fields=["start","end","dots","momenta"])

# definition of node types

#External Node always have number 0 and no Lines requirement
model.AddNodeType(0, Lines=[], Factor=node_factor, gv={"color": "red"}) 
# phi3 node
model.AddNodeType(1, Lines=[1, 1, 1], Factor=node_factor, feynman=0, feynman_sign=1)

# nodes from Sigma subgraphs inf counterterms graphs
model.AddNodeType(2, Lines=[1, 1], Factor=node_factor)

# node for factorized vertex subgraphs 
model.AddNodeType(3, Lines=[1, 1, 1], Factor=feynman4)

# node for factorized sigma subgraphs 
model.AddNodeType(4, Lines=[1, 1], Factor=feynman4)

model.AddStrech=AddStrech
model.AddDiff=AddDiff

# relevant subgraph types
model.AddSubGraphType(1, Lines=[1, 1, 1], dim=0, substitute=3)
model.AddSubGraphType(2, Lines=[1, 1], dim=2, substitute=4)

# definition of dots
model.AddDotType(1, dim=2, action=dot_action, gv={"penwidth":"3"}, feynman=1, feynman_sign=-1)

model.basepath = rggrf.storage.filesystem.NormalizeBaseName("~/work/rg-graph/testR1/")

try:
    os.listdir(rggrf.storage.filesystem.NormalizeBaseName(model.basepath))
except:
    raise ValueError, "invalid storage path  %s" %model.basepath
model.SaveGraphMethod = rggrf.storage.filesystem.SaveGraphAsPickle
model.LoadGraphMethod = rggrf.storage.filesystem.LoadGraphFromPickle

model.SaveResults = rggrf.storage.filesystem.SaveResults
model.LoadResults = rggrf.storage.filesystem.LoadResults

model.GetGraphList = rggrf.storage.filesystem.GetGraphList
model.WorkDir = rggrf.storage.filesystem.ChangeToWorkDir

model.target = 4

model.feynman = dict()
#eps=sympy.var('eps')
model.feynman['e11-e-']=("eps=sympy.var('e')\nu=sympy.var('a_%s'%parent_subgraph)\nres = ((-1+eps/4-sympy.pi**2*eps**2/24+sympy.pi**2*eps**3/96-sympy.pi**4*eps**4/5760)*( (sqmoment*u*(1-u))+( (1+sqmoment*u*(1-u))*sympy.ln(1+sqmoment*u*(1-u))*(-1+eps/4*sympy.ln(1+sqmoment*u*(1-u))-eps**2/24*(sympy.ln(1+sqmoment*u*(1-u)))**2+eps**3/192*(sympy.ln(1+sqmoment*u*(1-u)))**3-eps**4/1920*(sympy.ln(1+sqmoment*u*(1-u)))**4))))",
                         "eps=sympy.var('e')\nu=sympy.var('a_%s'%parent_subgraph)\nres = ((-1+3*eps/4-eps**2*(1./8+sympy.pi**2/24)+eps**3*sympy.pi**2/32-eps**4*(sympy.pi**2/192+sympy.pi**4/5760))*(sympy.ln(1+sqmoment*u*(1-u))*(-1+eps/4*sympy.ln(1+sqmoment*u*(1-u))-eps**2/24*(sympy.ln(1+sqmoment*u*(1-u)))**2+eps**3/192*(sympy.ln(1+sqmoment*u*(1-u)))**3-eps**4/1920*(sympy.ln(1+sqmoment*u*(1-u)))**4)    ))")

model.feynman['e12-e2-e-']=("eps=sympy.var('e')\nu2=sympy.var('a_%s_v1'%parent_subgraph)\nx=sympy.var('a_%s_v2'%parent_subgraph)\nu3=(1-u2)*x\nres = -(1 - 3*e/4 + e**2*(1./8 + sympy.pi**2/24) + e**4*(sympy.pi**2/192 + 7*sympy.pi**4/5760) - sympy.pi**2*e**3/32)*(1-u2)*(sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3) - e*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**2/4 + e**2*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**3/24 - e**3*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**4/192 + e**4*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**5/1920  )",
                            "eps=sympy.var('e')\nu2=sympy.var('a_%s_v1'%parent_subgraph)\nx=sympy.var('a_%s_v2'%parent_subgraph)\nu3=(1-u2)*x\nres = -(1-u2)*(1 - 3*e/4 + e**2*(1./8 + sympy.pi**2/24) + e**4*(sympy.pi**2/192 + 7*sympy.pi**4/5760) - sympy.pi**2*e**3/32)/(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)*(1 - e*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)/2 + e**2*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**2/8 - e**3*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**3/48 + e**4*sympy.ln(1+k2sq*u2*(1-u2)+k3sq*u3*(1-u3) + 2*u2*u3*k2xk3)**4/384 ) ")

# TODO: e12-23-3-e- only for 1-4 loops
model.feynman['e12-23-3-e-']=("eps=sympy.var('e')\n\
v1=sympy.var('a_%s_v1'%parent_subgraph)\n\
v2=sympy.var('a_%s_v2'%parent_subgraph)\n\
v3=sympy.var('a_%s_v3'%parent_subgraph)\n\
v4=sympy.var('a_%s_v4'%parent_subgraph)\n\
a=sympy.var('a_%s_v5'%parent_subgraph)\n\
b=sympy.var('a_%s_v6'%parent_subgraph)\n\
D=sympy.var('D')\n\
B=sympy.var('B')\n\
k2=sqmoment\n\
u1=v1\nu2=(1-u1)*v2\n\
u3=(1-u1-u2)*v3\n\
u4=(1-u1-u2-u3)*v4\n\
u5=1-u1-u2-u3-u4\n\
Det=(u1+b*b*u3+u4)*(u2+a**2*u3+u5)-a*a*b*b*u3**2\n\
B_=( (a*a*u4+b*b*u5)*D - a*a*u4*u4*(u2+a*a*u3+u5) - b*b*u5*u5*(u1+b*b*u3+u4) - 2*a*a*b*b*u3*u4*u5 )\n\
res = e*(0.5*sympy.log(D)/D**3 - 0.5*sympy.log(D + B*k2)/D**3 + 3*sympy.log(D)*sympy.log(D + B*k2)/(2*D**3) - \
0.5*B*k2*sympy.log(D + B*k2)/D**4 + 3*B*k2*sympy.log(D)*sympy.log(D + B*k2)/(2*D**4) + 0.5*B*k2/D**4 - \
0.5*sympy.log(D + B*k2)**2/D**3 - 1.*sympy.log(D)**2/D**3 - 0.5*B*k2*sympy.log(D + B*k2)**2/D**4 - \
1.*B*k2*sympy.log(D)**2/D**4) + 1/D**3*sympy.log(D + B*k2) - 1.*sympy.log(D)/D**3 + B*k2*sympy.log(D + B*k2)/D**4 - \
1.*B*k2*sympy.log(D)/D**4 - 1.*B*k2/D**4\n\
res=(1-u1-u2-u3)*(1-u1-u2)*(1-u1)*res.subs(B,B_).subs(D,Det).subs(e,0).diff(a).diff(b)",
                              "eps=sympy.var('e')\n\
v1=sympy.var('a_%s_v1'%parent_subgraph)\n\
v2=sympy.var('a_%s_v2'%parent_subgraph)\n\
v3=sympy.var('a_%s_v3'%parent_subgraph)\n\
v4=sympy.var('a_%s_v4'%parent_subgraph)\n\
a=sympy.var('a_%s_v5'%parent_subgraph)\n\
b=sympy.var('a_%s_v6'%parent_subgraph)\n\
D=sympy.var('D')\n\
B=sympy.var('B')\n\
k2=sqmoment\n\
u1=v1\nu2=(1-u1)*v2\n\
u3=(1-u1-u2)*v3\n\
u4=(1-u1-u2-u3)*v4\n\
u5=1-u1-u2-u3-u4\n\
Det=(u1+b*b*u3+u4)*(u2+a**2*u3+u5)-a*a*b*b*u3**2\n\
B_=( (a*a*u4+b*b*u5)*D - a*a*u4*u4*(u2+a*a*u3+u5) - b*b*u5*u5*(u1+b*b*u3+u4) - 2*a*a*b*b*u3*u4*u5 )\n\
res_t = e*(1.50000000000000*sympy.log(D)/D**3 - 1.50000000000000*sympy.log(D + B*k2)/D**3 + 3*sympy.log(D)*sympy.log(D + B*k2)/(2*D**3) - 1/D**3*sympy.log(D)**2 - sympy.log(D + B*k2)**2/(2*D**3)) + 1/D**3*sympy.log(D + B*k2) - 1/D**3*sympy.log(D)\n\
res=(1-u1-u2-u3)*(1-u1-u2)*(1-u1)*u3*res_t.subs(B,B_).subs(D,Det).subs(a,1).subs(b,1)\n\
res=res+4*(1-u1-u2-u3)*(1-u1-u2)*(1-u1)*u1*res_t.subs(B,B_).subs(D,Det).subs(a,1).diff(b)")
#model.feynman['e11-e-']=("eps=sympy.var('e')\nu=sympy.var('a_%s'%parent_subgraph)\nk2=sqmoment\nres=(-1)*(k2*u*(1-u)+(1+k2*u*(1-u))*sympy.ln(1+k2*u*(1-u))*(-1) )",
#                         "eps=sympy.var('e')\nu=sympy.var('a_%s'%parent_subgraph)\nk2=sqmoment\nres=sympy.ln(1+k2*u*(1-u))")



model.methods = dict()


def MCT_SV(G, debug=False):
    import progressbar
    G.GenerateNickel()
    G.method = "MCT_SV"
    base_name = "%s_%s"%(G.method,str( G.nickel))
    n_epsilon_series =G.model.target -G.NLoops()
    NPOINTS = 10000
    NTHREADS = 2
    SPACE_DIM = 6.
    prepared_eqs = []
    bar = progressbar.ProgressBar(maxval=100, term_width=70, 
                                  widgets=["%s  "%G.nickel, progressbar.Percentage(), 
                                           " ", progressbar.Bar(), 
                                           progressbar.ETA()]).start()
    Kres = L_dot(G,progress=(bar,25),debug=debug)
    progress=bar.currval
    step = 25./len(Kres)
    for idxK22 in range(len(Kres)):
            kterm = Kres[idxK2]  
            s_prep =   ExpandScalarProdsAndPrepareFactorized(kterm,debug)
            rggrf.utils.print_debug( "--------- %s --------- " %(idxK2), debug)
            prepared_eqs.append(rggrf.integration.PrepareFactorizedStrVars(s_prep, SPACE_DIM, 
                                                                           simplify=False, 
                                                                           debug=debug))
            progress = progress + step
            bar.update(progress)
               
    sys.stdout.flush()
          
    prog_names = rggrf.integration.GenerateMCCodeForTermStrVars(base_name, prepared_eqs, 
                                                                SPACE_DIM, n_epsilon_series, 
                                                                NPOINTS, NTHREADS,
                                                                debug=debug, 
                                                                progress=(bar,25.)) 
    
    t_res = rggrf.integration.CalculateEpsilonSeries(prog_names, 
                                                     build=True, debug=debug, 
                                                     progress=(bar,24.9))
    
    (G.r1_dot_gamma, err) = ResultWithSd(t_res, G.NLoops(), n_epsilon_series)
    G.r1_dot_gamma_err = rggrf.utils.RelativeError(G.r1_dot_gamma, err, 
                                                   sympy.var('eps'))
    
    rggrf.utils.print_debug(str(G.r1_dot_gamma), debug)
    G.npoints = NPOINTS 
    
    G.SaveResults()
    bar.finish()


model.methods['MCT_SV'] = MCT_SV

def MCO_SV(G, debug=False):
    import progressbar
    G.GenerateNickel()
    G.method = "MCO_SV"
    base_name = "%s_%s"%(G.method,str( G.nickel))
    n_epsilon_series =G.model.target -G.NLoops()
    NPOINTS = 10000
    NTHREADS = 2
    SPACE_DIM = 6.
    prepared_eqs = []
    bar = progressbar.ProgressBar(maxval=100, term_width=70, 
                                  widgets=["%s  "%G.nickel, progressbar.Percentage(), 
                                           " ", progressbar.Bar(), 
                                           progressbar.ETA()]).start()
    Kres = L_dot(G,progress=(bar,25),debug=debug)
    progress=bar.currval
    step = 25./len(Kres)
    for idxK2 in range(len(Kres)):
            kterm = Kres[idxK2]  
            s_prep =   ExpandScalarProdsAndPrepareFactorized(kterm,debug)
            rggrf.utils.print_debug( "--------- %s --------- " %(idxK2), debug)
            prepared_eqs.append(rggrf.integration.PrepareFactorizedStrVars(s_prep, SPACE_DIM, 
                                                                           simplify=False, 
                                                                           debug=debug))
            progress = progress + step
            bar.update(progress)
               
    sys.stdout.flush()
          
    prog_names = rggrf.integration.GenerateMCCodeForGraphStrVars(base_name, prepared_eqs, 
                                                                SPACE_DIM, n_epsilon_series, 
                                                                NPOINTS, NTHREADS,
                                                                debug=debug, 
                                                                progress=(bar,25.)) 
    
    t_res = rggrf.integration.CalculateEpsilonSeries(prog_names, 
                                                     build=True, debug=debug, 
                                                     progress=(bar,24.9))
    
    (G.r1_dot_gamma, err) = ResultWithSd(t_res, G.NLoops(), n_epsilon_series)
    G.r1_dot_gamma_err = rggrf.utils.RelativeError(G.r1_dot_gamma, err, 
                                                   sympy.var('eps'))
    
    rggrf.utils.print_debug(str(G.r1_dot_gamma), debug)
    G.npoints = NPOINTS 
    
    G.SaveResults()
    bar.finish()


model.methods['MCO_SV'] = MCO_SV


def MCT_SVd(G, debug=False):
    import progressbar
    G.GenerateNickel()
    G.method = "MCT_SVd"
    base_name = "%s_%s"%(G.method,str( G.nickel))
    n_epsilon_series =G.model.target -G.NLoops()
    NPOINTS = 10000
    NTHREADS = 2
    SPACE_DIM = 6.
    prepared_eqs = []
    bar = progressbar.ProgressBar(maxval=100, term_width=70, 
                                  widgets=["%s  "%G.nickel, progressbar.Percentage(), 
                                           " ", progressbar.Bar(), 
                                           progressbar.ETA()]).start()
    
    Kres = L_dot(G,progress=(bar,25),debug=debug)
    progress=bar.currval
    step = 25./len(Kres)
    for idxK2 in range(len(Kres)):
            kterm = Kres[idxK2]  
            s_prep =   ExpandScalarProdsAndPrepareFactorized(kterm,debug)
            rggrf.utils.print_debug( "--------- %s --------- " %(idxK2), debug)
            prepared_eqs.append(rggrf.integration.PrepareFactorizedStrVars(s_prep, SPACE_DIM, 
                                                                           simplify=False, 
                                                                           debug=debug))
            progress = progress + step
            bar.update(progress)
               
    sys.stdout.flush()
          
    prog_names = rggrf.integration.GenerateMCCodeForTermStrVars(base_name, prepared_eqs, 
                                                                SPACE_DIM, n_epsilon_series, 
                                                                NPOINTS, NTHREADS,
                                                                debug=debug, 
                                                                progress=(bar,25.),
                                                                MCCodeGenerator=rggrf.integration.SavePThreadsMCCodeDelta) 
    
    t_res = rggrf.integration.CalculateEpsilonSeries(prog_names, 
                                                     build=True, debug=debug, 
                                                     progress=(bar,24.9),
                                                     calc_delta=0.)
    
    (G.r1_dot_gamma, err) = ResultWithSd(t_res, G.NLoops(), n_epsilon_series)
    G.r1_dot_gamma_err = rggrf.utils.RelativeError(G.r1_dot_gamma, err, 
                                                   sympy.var('eps'))
    
    rggrf.utils.print_debug(str(G.r1_dot_gamma), debug)
    G.npoints = NPOINTS 
    
    G.SaveResults()
    bar.finish()


model.methods['MCT_SVd'] = MCT_SVd

def MCO_SVd(G, debug=False):
    import progressbar
    G.GenerateNickel()
    G.method = "MCO_SVd"
    base_name = "%s_%s"%(G.method,str( G.nickel))
    n_epsilon_series =G.model.target -G.NLoops()
    NPOINTS = 10000
    NTHREADS = 2
    SPACE_DIM = 6.
    prepared_eqs = []
    bar = progressbar.ProgressBar(maxval=100, term_width=70, 
                                  widgets=["%s  "%G.nickel, progressbar.Percentage(), 
                                           " ", progressbar.Bar(), 
                                           progressbar.ETA()]).start()
    Kres = L_dot(G,progress=(bar,25),debug=debug)
    progress=bar.currval
    step = 25./len(Kres)
    for idxK2 in range(len(Kres)):
            kterm = Kres[idxK2]  
            s_prep =   ExpandScalarProdsAndPrepareFactorized(kterm,debug)
            rggrf.utils.print_debug( "--------- %s --------- " %(idxK2), debug)
            prepared_eqs.append(rggrf.integration.PrepareFactorizedStrVars(s_prep, SPACE_DIM, 
                                                                           simplify=False, 
                                                                           debug=debug))
            progress = progress + step
            bar.update(progress)
                   
    sys.stdout.flush()
          
    prog_names = rggrf.integration.GenerateMCCodeForGraphStrVars(base_name, prepared_eqs, 
                                                                SPACE_DIM, n_epsilon_series, 
                                                                NPOINTS, NTHREADS,
                                                                debug=debug, 
                                                                progress=(bar,25.),
                                                                MCCodeGenerator=rggrf.integration.SavePThreadsMCCodeDelta) 
    
    t_res = rggrf.integration.CalculateEpsilonSeries(prog_names, 
                                                     build=True, debug=debug, 
                                                     progress=(bar,24.9),
                                                     calc_delta=0.)
    
    (G.r1_dot_gamma, err) = ResultWithSd(t_res, G.NLoops(), n_epsilon_series)
    G.r1_dot_gamma_err = rggrf.utils.RelativeError(G.r1_dot_gamma, err, 
                                                   sympy.var('eps'))
    
    rggrf.utils.print_debug(str(G.r1_dot_gamma), debug)
    G.npoints = NPOINTS 
    
    G.SaveResults()
    bar.finish()


model.methods['MCO_SVd'] = MCO_SVd

def Reduce(G):
    def cmp_subgraphs(sub1,sub2):
        # чем больше линий тем раньше идет
        if len(sub1.internal_lines)< len(sub2.internal_lines):
            return 1
        elif len(sub1.internal_lines) == len(sub2.internal_lines):
            return 0
        else:
            return -1
        
#    subgraphs = G.subgraphs
#    subgraphs.sort(cmp_subgraphs)
    
    to_reduce=list()
    reducible=list()
    #скорее всего лучше найти все потенциально инетересные графы а потом подобрать непротиворечивую комбинацию
    # сейчас возможен пропуск графов при наличии в feynman многопетлевых графов с подграфами
    for idxS in range(len(G.subgraphs)):
        sub = G.subgraphs[idxS]
        sub.GenerateNickel()
        sub_nickel = str(sub.nickel)
#        print 
#        print
#        print sub_nickel, sub_nickel in G.model.feynman.keys()
        reduce_sub=True
        if sub_nickel in G.model.feynman:
            for idxS2 in range(len(G.subgraphs)):
                if idxS<>idxS2:
                    sub2 = G.subgraphs[idxS2]
#                    print " %s %s intersect: %s inside: %s"%( idxS, idxS2, rggrf.roperation.IsIntersect(G, [idxS, idxS2]),rggrf.roperation.IsInside(G, idxS, idxS2) ) 
                    if (rggrf.roperation.IsIntersect(G, [idxS, idxS2]) and 
                        not rggrf.roperation.IsInside(G, idxS, idxS2)):
                        reduce_sub=False
                        break
            if reduce_sub:
                reducible.append(idxS)
#    print        
#    print
#    print reducible
    
    for idxS in reducible:
        sub = G.subgraphs[idxS]
        is_max=True
        for idxS2 in reducible:
            if idxS<>idxS2:
                sub2 = G.subgraphs[idxS2]
                if (rggrf.roperation.IsInside(G, idxS, idxS2) and 
                    len(sub.internal_lines)<len(sub2.internal_lines)):
                    is_max=False
        if is_max:
            to_reduce.append(idxS)

    
    (reduced_graph,subgraph_map) =  rggrf.roperation.ExtractSubgraphs( G, to_reduce )
#    print "sub map ",subgraph_map
    for idxN in subgraph_map:
        sub = G.subgraphs[to_reduce[subgraph_map[idxN]]]
        sub.GenerateNickel()
        str_nickel = str(sub.nickel)
        int_lines = list(sub.internal_lines)
        int_lines.sort()
        parent_subgraph = ""
        for idxL in int_lines:
            parent_subgraph = parent_subgraph + "%s_"%idxL
        parent_subgraph = parent_subgraph[:-1]
        reduced_graph.nodes[idxN].str_nickel = str_nickel
        reduced_graph.nodes[idxN].parent_subgraph = parent_subgraph
        
    return reduced_graph           
                    
                
                        
                    
    
    

def MCOR_SVd(G, debug=False):
    import progressbar
    G.GenerateNickel()
    G.method = "MCOR_SVd"
    base_name = "%s_%s"%(G.method,str( G.nickel))
    n_epsilon_series =G.model.target -G.NLoops()
    NPOINTS = 10000
    NTHREADS = 2
    SPACE_DIM = 6.
    prepared_eqs = []
    bar = progressbar.ProgressBar(maxval=100, term_width=70, 
                                  widgets=["%s  "%G.nickel, progressbar.Percentage(), 
                                           " ", progressbar.Bar(), 
                                           progressbar.ETA()]).start()
                                           
    reduced_graph = Reduce(G)
    
#    print 
#    print reduced_graph.internal_lines
#    print reduced_graph.GetNodesTypes()
#    print reduced_graph.NLoops()
    G.reduced_nloops = reduced_graph.NLoops()
    
    reduced_graph.FindSubgraphs()
    reduced_graph.SaveAsPNG("reduced.png")
    
    Kres = L_dot(reduced_graph,progress=(bar,25),debug=debug)
    progress=bar.currval
    step = 25./len(Kres)
    for idxK2 in range(len(Kres)):
            kterm = Kres[idxK2]  
            s_prep =   ExpandScalarProdsAndPrepareFactorized(kterm,debug)
            rggrf.utils.print_debug( "--------- %s --------- " %(idxK2), debug)
            prepared_eqs.append(rggrf.integration.PrepareFactorizedStrVars(s_prep, SPACE_DIM, 
                                                                           simplify=False, 
                                                                           debug=debug))
            progress = progress + step
            bar.update(progress)
                   
    sys.stdout.flush()
          
    prog_names = rggrf.integration.GenerateMCCodeForGraphStrVars(base_name, prepared_eqs, 
                                                                SPACE_DIM, n_epsilon_series, 
                                                                NPOINTS, NTHREADS,
                                                                debug=debug, 
                                                                progress=(bar,25.),
                                                                MCCodeGenerator=rggrf.integration.SavePThreadsMCCodeDelta) 
    
    t_res = rggrf.integration.CalculateEpsilonSeries(prog_names, 
                                                     build=True, debug=debug, 
                                                     progress=(bar,24.9),
                                                     calc_delta=0.)
    
    (G.r1_dot_gamma, err) = ResultWithSd(t_res, G.reduced_nloops, n_epsilon_series)
    G.r1_dot_gamma_err = rggrf.utils.RelativeError(G.r1_dot_gamma, err, 
                                                   sympy.var('eps'))
    
    rggrf.utils.print_debug(str(G.r1_dot_gamma), debug)
    G.npoints = NPOINTS 
    
    G.SaveResults()
    bar.finish()


model.methods['MCOR_SVd'] = MCOR_SVd

def MCTR_SVd(G, debug=False):
    import progressbar
    G.GenerateNickel()
    G.method = "MCTR_SVd"
    base_name = "%s_%s"%(G.method,str( G.nickel))
    n_epsilon_series =G.model.target -G.NLoops()
    NPOINTS = 10000
    NTHREADS = 2
    SPACE_DIM = 6.
    prepared_eqs = []
    bar = progressbar.ProgressBar(maxval=100, term_width=70, 
                                  widgets=["%s  "%G.nickel, progressbar.Percentage(), 
                                           " ", progressbar.Bar(), 
                                           progressbar.ETA()]).start()
                                           
    reduced_graph = Reduce(G)
    
#    print 
#    print reduced_graph.internal_lines
#    print reduced_graph.GetNodesTypes()
#    print reduced_graph.NLoops()
    G.reduced_nloops = reduced_graph.NLoops()
    
    reduced_graph.FindSubgraphs()
    
    Kres = L_dot(reduced_graph,progress=(bar,25),debug=debug)
    progress=bar.currval
    step = 25./len(Kres)
    for idxK2 in range(len(Kres)):
            kterm = Kres[idxK2]  
            s_prep =   ExpandScalarProdsAndPrepareFactorized(kterm,debug)
            rggrf.utils.print_debug( "--------- %s --------- " %(idxK2), debug)
            prepared_eqs.append(rggrf.integration.PrepareFactorizedStrVars(s_prep, SPACE_DIM, 
                                                                           simplify=False, 
                                                                           debug=debug))
            progress = progress + step
            bar.update(progress)
                   
    sys.stdout.flush()
          
    prog_names = rggrf.integration.GenerateMCCodeForTermStrVars(base_name, prepared_eqs, 
                                                                SPACE_DIM, n_epsilon_series, 
                                                                NPOINTS, NTHREADS,
                                                                debug=debug, 
                                                                progress=(bar,25.),
                                                                MCCodeGenerator=rggrf.integration.SavePThreadsMCCodeDelta) 
    
    t_res = rggrf.integration.CalculateEpsilonSeries(prog_names, 
                                                     build=True, debug=debug, 
                                                     progress=(bar,24.9),
                                                     calc_delta=0.)
    
    (G.r1_dot_gamma, err) = ResultWithSd(t_res, G.reduced_nloops, n_epsilon_series)
    G.r1_dot_gamma_err = rggrf.utils.RelativeError(G.r1_dot_gamma, err, 
                                                   sympy.var('eps'))
    
    rggrf.utils.print_debug(str(G.r1_dot_gamma), debug)
    G.npoints = NPOINTS 
    
    G.SaveResults()
    bar.finish()


model.methods['MCTR_SVd'] = MCTR_SVd


    
def ResultWithSd(_dict, nloops, n_eps_series):
    
    eps = sympy.var('eps')
    t_mnog=[1, 
            sympy.Real('0.84882636315677518', prec=15) - sympy.Real('0.093212888565618754', prec=15)*eps
            - sympy.Real('0.0050067349361000383', prec=15)*pow(eps,2) - 
            sympy.Real('0.00052717817355572589', prec=15)*pow(eps,3) - 
            sympy.Real('6.8133402095973142e-5', prec=15)*pow(eps,4),
            sympy.Real('0.54037964609246814', prec=15) - sympy.Real('0.19443607942348598', prec=15)*eps 
            + sympy.Real('0.011647905519767411', prec=15)*pow(eps,2) + 
            sympy.Real('0.00046123456498500229', prec=15)*pow(eps,3) + 
            sympy.Real('4.052794127858356e-5', prec=15)*pow(eps,4),
            sympy.Real('0.21900762143326583', prec=15) - sympy.Real('0.17585458479914437', prec=15)*eps
            + sympy.Real('0.04636648202336683', prec=15)*pow(eps,2) - 
            sympy.Real('0.0040301692384473609', prec=15)*pow(eps,3) + 
            sympy.Real('3.08374601549584e-7', prec=15)*pow(eps,4),
            sympy.Real('0.044380222860623028', prec=15) - sympy.Real('0.068920756507029612', prec=15)*eps + 
            sympy.Real('0.041670033558627036', prec=15)*pow(eps,2) 
            - sympy.Real('0.012317991965140199', prec=15)*pow(eps,3) + 
            sympy.Real('0.0017870514760215828', prec=15)*pow(eps,4)
            ]
    expr = 0
    err = 0
    for idx in _dict:
        expr = expr + eps**idx*_dict[idx][0]
        err = err + eps**idx*_dict[idx][1]
    expr = rggrf.utils.SimpleSeries(expr * t_mnog[nloops-1], eps, 0, n_eps_series)
    err = rggrf.utils.SimpleSeries(err * t_mnog[nloops-1], eps, 0, n_eps_series)
    #print series(expr,eps,0)
    return (expr, err)

def ResultOldNotation(_dict):
    eps = sympy.var('eps')
    expr = 0
    for idx in _dict:
        expr = expr + eps**idx*_dict[idx][0]
     
    #print series(expr,eps,0)
    return expr*2