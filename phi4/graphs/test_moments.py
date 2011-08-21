#!/usr/bin/python
# -*- coding:utf8

import sympy

from nose.tools import raises

from dummy_model import _phi3,_phi4
import moments
from graphs import Graph
from lines import Line

class Test_convert:
    def  test_str2dict(self):
        """ Test str2dict conversion for moments
        """
        assert moments._str2dict('p')=={'p':1}
        assert moments._str2dict('')=={}
        assert moments._str2dict('p+q')=={'p':1,'q':1}
        assert moments._str2dict('p-q')=={'p':1,'q':-1}
        assert moments._str2dict('-p+q')=={'p':-1,'q':1}
        assert moments._str2dict('-p-q')=={'p':-1,'q':-1}
        assert moments._str2dict('-p-q+v')=={'p':-1,'q':-1,'v':1}
    def test_dict2sympy(self):
        """ Test dict2sympy conversion for moments
        """
        (p,q,v) = sympy.var('p q v')
        assert  moments._dict2sympy({})==0
        assert  moments._dict2sympy({'p':1})==p
        assert  moments._dict2sympy({'p':1,'q':1})==p+q
        assert  moments._dict2sympy({'p':1,'q':-1})==p-q
        assert  moments._dict2sympy({'p':1,'q':1,'v':-1})==p+q-v
        assert  moments._dict2sympy({'p':-1,'q':-1,'v':-1})==-p-q-v

class Test_Momenta:
    def test_init_string(self):
        """ initialization of Momenta instance with string
        """
        (p,q,v)=sympy.var('p q v')
        pq=moments.Momenta(string='p+q')
        assert pq._string=='p+q'
        assert pq._dict=={'p':1,'q':1}
        assert pq.sympy()==p+q

    def test_init_dict(self):
        """ initialization of Momenta instance with dict
        """
        (p,q,v)=sympy.var('p q v')
        pq=moments.Momenta(dict={'p':1,'q':1})
        assert pq._string=='p+q' or pq._string=='q+p'
        assert pq._dict=={'p':1,'q':1}
        assert pq.sympy()==p+q

    def test_init_sympy(self):
        """ initialization of Momenta  instance with sympy
        """
        (p,q,v)=sympy.var('p q v')
        pq=moments.Momenta(sympy=p+q)
        assert pq._string=='p+q'
        assert pq._dict=={'p':1,'q':1}
        assert pq._sympy==p+q

    @raises(TypeError)
    def test_init_err(self):
        """ Momenta initialization with empty args
        """        
        p=moments.Momenta()

    def test_neg(self):
        """ Momenta __neg__ operation
        """
        p,q=sympy.var('p q')
        m1=moments.Momenta(sympy=p-q)
        m2=-m1
        assert m1.sympy()==-m2.sympy()
        
    def test_add(self):
        """ Momenta addition
        """        
        assert moments.Momenta(string='p-q')+moments.Momenta(string='q-v')==moments.Momenta(string='p-v')

    def test_sub(self):
        """ Momenta substraction
        """
        assert moments.Momenta(string='p-q')-moments.Momenta(string='v-q')==moments.Momenta(string='p-v')

    def test_abs(self):
        """ Momenta absolute value
        """
        p,q,pOq=sympy.var('p q pOq')
        assert abs(moments.Momenta(sympy=p))==sympy.sqrt(p*p)
        print abs(moments.Momenta(sympy=p+q))
        assert abs(moments.Momenta(sympy=p+q))==sympy.sqrt(p*p+q*q+2*p*q*pOq)

    def test_mull(self):
        """ Momenta scalar product
        """       
        p,q,v,pOq,pOv,qOv=sympy.var('p q v pOq pOv qOv')
        print moments.Momenta(sympy=-p+q)*moments.Momenta(sympy=q-v)
        assert moments.Momenta(sympy=-p+q)*moments.Momenta(sympy=q-v)==-p*q*pOq+q*q+p*v*pOv-q*v*qOv

    def test_eq(self):
        """ Momenta __eq__ operation
        """        
        assert moments.Momenta(sympy=0) == moments.Momenta(dict={})
        assert moments.Momenta(string="p+q") == moments.Momenta(string="q+p")


    def test_setZerosByAtoms(self):
        """ setting to zeros some atomic momenta
        """
        q,v=sympy.var("q v")
        assert moments.Momenta(string='p+q-v+t').setZerosByAtoms(set([q,v]))==moments.Momenta(string='p+t')


def compare_moments(dict1,dict2):
    """ compare moments generated by Generic (Kirghoff). keys are lines or lins indexes
        information about Line class instance dropped, only Line.idx() used.
        After that line indexes renumbered starting from 1
    """
    if isinstance(dict1.keys()[0],Line):
        minidx=min([x.idx() for x in dict1.keys()])
        _dict1=dict([(x.idx()-minidx+1,dict1[x]) for x in dict1.keys()])
    else:
        minidx=min(dict1.keys())
        _dict1=dict([(x-minidx+1,dict1[x]) for x in dict1.keys()])

    if isinstance(dict2.keys()[0],Line):
        minidx=min([x.idx() for x in dict2.keys()])
        _dict2=dict([(x.idx()-minidx+1,dict2[x]) for x in dict2.keys()])
    else:
        minidx=min(dict2.keys())
        _dict2=dict([(x-minidx+1,dict2[x]) for x in dict2.keys()])
    return _dict1==_dict2

def print_moments(_moments):
    if isinstance(_moments.keys()[0],Line):
        print dict([(x.idx(),_moments[x]._string) for x in _moments])
    else:
        print dict([(x,_moments[x]._string) for x in _moments])

def _momenta_dict(string_dict):
    """ convert dict with string values(moments) to dict with Momenta values
    """
    res=dict()
    for x in string_dict:
        res[x]=moments.Momenta(string=string_dict[x])
    return res
        

class Test_Generate:
    def setUp(self):
        self.phi3=_phi3('dummy')
        self.phi4=_phi4('dummy')
 
    def test_Generic_e11_e_(self):
        g1=Graph('e11-e-')
        self.phi3.SetTypes(g1)
        g1.FindSubgraphs(self.phi3)
        _moments,_subgraphs=moments.Generic(self.phi3, g1)
        print_moments(_moments)
        print_moments(_momenta_dict({8: 'p0+q0', 9: '-q0', 6: 'p0', 7: '-p0'})) 
        assert compare_moments(_moments,_momenta_dict({8: 'p0+q0', 9: '-q0', 6: 'p0', 7: '-p0'}))

#        print_moments(_momenta_dict({1:'p0',2:'-p0',3:'q0',4:'p0-q0'})) 
#        assert compare_moments(_moments,_momenta_dict({1:'p0',2:'-p0',3:'q0',4:'p0-q0'}))

    def test_Generic_e12_e3_33_(self):
        g1=Graph('e12-e3-33--')
        self.phi3.SetTypes(g1)
        g1.FindSubgraphs(self.phi3)
        #print [x.Nodes() for x in g1.xInternalLines()]
        _moments,subgraphs=moments.Generic(self.phi3, g1)
        
        print_moments(_moments)
        print_moments(_momenta_dict({10: 'p0', 11: '-p0', 12: 'p0+q0', 13: '-q0', 14: 'q0', 15: 'q1-q0', 16: '-q1'})) 
        assert compare_moments(_moments,_momenta_dict({10: 'p0', 11: '-p0', 12: 'p0+q0', 13: '-q0', 14: 'q0', 15: 'q1-q0', 16: '-q1'}))
#        print_moments(_momenta_dict({1: 'p0', 2: '-p0', 3: 'p0-q0', 4: 'q0', 5: '-q0', 6: 'q1', 7: 'q0-q1'})) 
 #       assert compare_moments(_moments,_momenta_dict({1: 'p0', 2: '-p0', 3: 'p0-q0', 4: 'q0', 5: '-q0', 6: 'q1', 7: 'q0-q1'}))

    def test_Generic_e12_33_44_5_6_e7_77__(self):
        assert False
#TODO: remove
        g1=Graph('e12-33-44-5-6-e7-77--')
        self.phi3.SetTypes(g1)
        g1.FindSubgraphs(self.phi3)
        _moments,_subgraphs=moments.Generic(self.phi3, g1)
        print dict([(x.idx(),x.Nodes()) for x in g1.xInternalLines()])
        print_moments(_moments)
        print_moments(_momenta_dict({5: 'p0', 6: '-p0', 7: 'p0-q0', 8: 'q0', 9: 'q1', 10: 'p0-q0-q1', 11: 'q2', 12: 'q0-q2', 13: 'p0-q0', 14: 'q0', 15: '-q0', 16: 'q3', 17: 'q0-q3'})) 
        assert compare_moments(_moments,_momenta_dict({5: 'p0', 6: '-p0', 7: 'p0-q0', 8: 'q0', 9: 'q1', 10: 'p0-q0-q1', 11: 'q2', 12: 'q0-q2', 13: 'p0-q0', 14: 'q0', 15: '-q0', 16: 'q3', 17: 'q0-q3'}))


    def test_Generic_e111_e_(self):
#        return
##TODO: remove
        g1=Graph('e111-e-')
        self.phi4.SetTypes(g1)
        g1.FindSubgraphs(self.phi4)
        _moments,_subgraphs=moments.Generic(self.phi4, g1)
        print_moments(_moments)
        print g1._subgraphs, _subgraphs
        print_moments(_momenta_dict({1: 'p0', 2: '-p0', 3: 'p0+q0', 4: 'q1-q0', 5: '-q1'})) 
        print g1
        assert compare_moments(_moments,_momenta_dict({1: 'p0', 2: '-p0', 3: 'p0+q0', 4: 'q1-q0', 5: '-q1'}))

    def test_Generic_e112_e3__333__(self):
        return
##TODO: remove
        g1=Graph('e112-e3-333--')
        self.phi4.SetTypes(g1)
        g1.FindSubgraphs(self.phi4)
        _moments,_subgraphs=moments.Generic(self.phi4, g1)
        print_moments(_moments)
        print g1._subgraphs, _subgraphs
        print_moments(_momenta_dict({1: 'p0', 2: '-p0', 3: 'p0+q0', 4: 'q1-q0', 5: '-q1'})) 
        assert compare_moments(_moments,_momenta_dict({1: 'p0', 2: '-p0', 3: 'p0+q0', 4: 'q1-q0', 5: '-q1'}))


    def test_LoopsAndPaths(self):
        g1=Graph('ee11-ee-')
        print moments.LoopsAndPaths(g1)
        assert False
