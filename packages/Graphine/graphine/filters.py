#!/usr/bin/python
# -*- coding: utf8
import graph_operations


def graphFilter(qualifier):
    """
    graphFilter should be used as decorator

    @graphFilter
    def myFilter(...):
      ...
    """
    return [qualifier]


def isRelevant(model):
    def wrapper(edgesList, superGraph, superGraphEdges):
        return model.isRelevant(edgesList, superGraph, superGraphEdges)
    return [wrapper]


oneIrreducible = graphFilter(graph_operations.isGraph1Irreducible)
connected = graphFilter(graph_operations.isGraphConnected)
noTadpoles = graphFilter(graph_operations.isGraphVertexIrreducible)