#!/usr/bin/python
# -*- coding: utf8
import unittest
import graph_state
import graphine.filters as filters
import graphine
import ir_uv

__author__ = 'daddy-bear'


uv = ir_uv.UVRelevanceCondition(4)
ir = ir_uv.IRRelevanceCondition(4)

subgraphUVFilters = (filters.one_irreducible
                     + filters.no_tadpoles
                     + filters.vertex_irreducible
                     + filters.is_relevant(uv))

subgraphIRFilters = (filters.connected + filters.is_relevant(ir))


class Phi4Test(unittest.TestCase):
    def _testIRCondition(self):
        self.doTestIRCondition("e12|34|34||e|", ["ee1|2|ee|::"])
        self.doTestIRCondition("e112|e2||", ["eee1|2|eee|::"])
        self.doTestIRCondition("e123|224|4|4|e|", ["eee1|2|eee|::"])

    def doTestIRCondition(self, graphState, expectedGraphGraphs=list()):
        g = graphine.Graph(graph_state.GraphState.fromStr(graphState))
        self.assertEquals(set([str(subg.toGraphState()) for subg in
                               g.xRelevantSubGraphs(subgraphIRFilters, graphine.Representator.asMinimalGraph)]),
                               set(expectedGraphGraphs))

if __name__ == "__main__":
    unittest.main()