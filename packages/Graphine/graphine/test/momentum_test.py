#!/usr/bin/python
# -*- coding: utf8
import unittest
import graph
import graph_state
import momentum

__author__ = 'daddy-bear'


class SubGraphReducerTestCase(unittest.TestCase):
    def testArbitrarilyPassMomentum(self):
        self.doTestArbitrarilyPassMomentum("ee12-23-3-ee-::", 6)
        self.doTestArbitrarilyPassMomentum("ee12-3-3-ee-::", 6)
        self.doTestArbitrarilyPassMomentum("11--", 1)

    def testArbitraryPassMomentum(self):
        g = graph.Graph.initEdgesColors(graph.Graph(graph_state.GraphState.fromStr("ee12-e23-44-e44--::")))
        for x in momentum.xArbitrarilyPassMomentum(g):
            self.assertFalse(str(x).startswith("ee"))

    def doTestArbitrarilyPassMomentum(self, graph_state_str, graphs_number):
        g = graph.Graph.initEdgesColors(graph.Graph(graph_state.GraphState.fromStr(graph_state_str)))
        graphs_with_passed_momentum = [x for x in momentum.xArbitrarilyPassMomentum(g)]
        for _g in graphs_with_passed_momentum:
            self.assertEquals(len(_g.edges(_g.externalVertex)), 2)
        self.assertEquals(len(graphs_with_passed_momentum), graphs_number, graphs_with_passed_momentum)

if __name__ == "__main__":
    unittest.main()