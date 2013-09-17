#!/usr/bin/python
# -*- coding: utf8
import graphine
import symbolic_functions
import ir_uv

__author__ = 'daddy-bear'


class CannotBeCalculatedError(AssertionError):
    def __init__(self, graph):
        self._graph = graph

    def __str__(self):
        return "cannot calculate " + str(self._graph)


class T0OperationNotDefined(AssertionError):
    pass


class AbstractKOperation(object):
    def calculate(self, graph):
        raise NotImplementedError


class MSKOperation(AbstractKOperation):
    def __init__(self, description=""):
        self._description = description

    def calculate(self, expression):
        return symbolic_functions.polePart(expression)

GFUN_METHOD_NAME_MARKER = "g-functions"
MS_SCHEME_NAME_MARKER = "ms-scheme"

defaultSubgraphUVFilter = (graphine.filters.oneIrreducible
                           + graphine.filters.noTadpoles
                           + graphine.filters.isRelevant(ir_uv.UVRelevanceCondition()))


_DEFAULT_GRAPH_HAS_NOT_IR_DIVERGENCE_RESULT = dict()

subgraphIRFilters = (graphine.filters.connected + graphine.filters.isRelevant(ir_uv.IRRelevanceCondition()))


def defaultGraphHasNotIRDivergence(graph):
    result = _DEFAULT_GRAPH_HAS_NOT_IR_DIVERGENCE_RESULT.get(graph, None)
    if result is None:
        for _ in graph.xRelevantSubGraphs(subgraphIRFilters):
            _DEFAULT_GRAPH_HAS_NOT_IR_DIVERGENCE_RESULT[graph] = False
            return False
        _DEFAULT_GRAPH_HAS_NOT_IR_DIVERGENCE_RESULT[graph] = True
        return True
    return result

defaultGraphHasNotIRDivergenceFilter = [defaultGraphHasNotIRDivergence]