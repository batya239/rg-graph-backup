#!/usr/bin/python
# -*- coding: utf8
import copy
import graph_state
import rggraphutil
import graph_operations
import itertools

assert graph_state.Edge.CREATE_EDGES_INDEX


class Representator(object):
    """
    see Graph#xRelevantSubGraphs
    """
    def __init__(self):
        raise AssertionError

    # noinspection PyUnusedLocal
    @staticmethod
    def asList(edgeList, external_vertex):
        return edgeList

    @staticmethod
    def asGraph(edgeList, external_vertex):
        return Graph(edgeList, external_vertex=external_vertex, renumbering=False)

    @staticmethod
    def asMinimalGraph(edgeList, external_vertex):
        return Graph(edgeList, external_vertex=external_vertex, renumbering=True)


class Graph(object):
    """
    representation of graph
    """
    def __init__(self, obj, external_vertex=-1, renumbering=True):
        """
        constructor to create Graph

        obj - adjacency matrix, edges list or GraphState

        self.edges - dict where keys is one vertex of edge and value is list of second vertices

        renumbering - reordering edges using GraphState
        """
        if isinstance(obj, (list, tuple)):
            self._edges = Graph._parseEdges(graph_state.GraphState(obj).edges if renumbering else obj)
        elif isinstance(obj, dict):
            self._edges = obj
        elif isinstance(obj, graph_state.GraphState):
            self._edges = Graph._parseEdges(obj.edges)
        else:
            raise AssertionError("unsupported obj type - %s" % type(obj))
        self._nextVertexIndex = max(self._edges.keys()) + 1
        self._external_vertex = external_vertex
        self._hash = None
        self._loopsCount = None
        self._externalEdges = None
        self._graphState = None
        self._allEdges = None
        self._allEdgesIndices = None
        self._allInternalEdgesCount = None
        self._boundVertexes = None
        self._vertices = None

    @property
    def external_vertex(self):
        return self._external_vertex

    def externalEdges(self):
        if self._externalEdges is None:
            self._externalEdges = self.edges(self.external_vertex)
        return self._externalEdges

    def externalEdgesCount(self):
        return len(self.externalEdges())

    def internalEdges(self):
        res = list()
        for edge in self.allEdges():
            if self.external_vertex not in edge.nodes:
                res.append(edge)
        return res

    def vertices(self):
        if self._vertices is None:
            self._vertices = frozenset(self._edges.keys())
        return self._vertices

    def createVertexIndex(self):
        to_return = self._nextVertexIndex
        self._nextVertexIndex += 1
        return to_return

    def getGraphStatePropertiesConfig(self):
        return self._edges.values()[0][0].properties_config

    def edges(self, vertex, vertex2=None):
        """
        returns all edges with one vertex equals vertex parameter
        """
        if vertex2 is None:
            return copy.copy(self._edges.get(vertex, []))
        return filter(lambda e: vertex2 in e.nodes, self._edges.get(vertex, []))

    def allEdgesIndices(self):
        """
        special method, inserted to Graph for caching
        """
        if self._allEdgesIndices is None:
            self._allEdgesIndices = frozenset(map(lambda e: e.edge_id, self.allEdges()))
        return self._allEdgesIndices

    def allEdges(self, nickel_ordering=False):
        if nickel_ordering:
            return copy.copy(self.toGraphState().edges)
        if self._allEdges is None:
            wrapped_result = set()
            for edges in self._edges.values():
                for e in edges:
                    wrapped_result.add(_IdAwareEdgeDelegate(e))
            self._allEdges = map(lambda ei: ei.edge, wrapped_result)
        return copy.copy(self._allEdges)

    def addEdges(self, edgesToAdd):
        """
        immutable operation
        """
        newEdges = self.allEdges() + edgesToAdd
        return Graph(newEdges, external_vertex=self.external_vertex)

    def addEdge(self, edge):
        return self.addEdges([edge])

    def deleteEdges(self, edgesToRemove):
        """
        immutable operation
        """
        if not len(edgesToRemove):
            return self
        newEdges = Graph.dict_copy(self._edges)
        for edge in edgesToRemove:
            Graph._persDeleteEdge(newEdges, edge)
        return Graph(newEdges, external_vertex=self.external_vertex)

    def change(self, edgesToRemove=None, edgesToAdd=None, renumbering=True):
        """
        transactional changes graph structure
        """
        newEdges = copy.copy(self.allEdges())
        map(lambda e: newEdges.remove(e), edgesToRemove)
        map(lambda e: newEdges.append(e), edgesToAdd)
        return Graph(newEdges, external_vertex=self.external_vertex, renumbering=renumbering)

    def deleteVertex(self, vertex, transformEdgesToExternal=False):
        assert vertex != self.external_vertex
        if transformEdgesToExternal:
            edges = self.edges(vertex)
            for e in edges:
                if self.external_vertex in e.nodes:
                    raise AssertionError
            g = self.deleteEdges(edges)
            nodeMap = {vertex: self.external_vertex}
            nEdges = map(lambda e: e.copy(nodeMap), edges)
            return g.addEdges(nEdges)
        else:
            return self.deleteEdges(self.edges(vertex))

    def deleteEdge(self, edge):
        return self.deleteEdges([edge])

    def contains(self, other_graph):
        self_edges = self._edges
        other_edges = other_graph._edges
        for v, other_es in other_edges.iteritems():
            _self_es = self_edges.get(v, None)
            if _self_es is None and len(other_edges):
                return False
            self_es = copy.copy(_self_es)
            for e in other_es:
                if e in self_es:
                    self_es.remove(e)
                else:
                    return False
        return True

    def batchShrinkToPointWithAuxInfo(self, sub_graphs):
        """
        subGraphs -- list of graphs edges or graph with equivalent numbering of vertices
        """
        if not len(sub_graphs):
            return self, list()

        vertex_transformation = ID_VERTEX_TRANSFORMATION
        g = self
        new_vertices = list()
        for subGraph in sub_graphs:
            all_edges = subGraph.allEdges() if isinstance(subGraph, Graph) else subGraph
            g, new_vertex, vertex_transformation = g._shrinkToPoint(all_edges, vertex_transformation)
            new_vertices.append(new_vertex)
        assert g
        return g, new_vertices

    def batchShrinkToPoint(self, sub_graphs):
        return self.batchShrinkToPointWithAuxInfo(sub_graphs)[0]

    def _shrinkToPoint(self, unTransformedEdges, vertex_transformation=None):
        """
        obj -- list of edges or graph
        immutable operation
        """
        if not vertex_transformation:
            vertex_transformation = ID_VERTEX_TRANSFORMATION

        edges = map(lambda e: e.copy(vertex_transformation.mapping), unTransformedEdges)

        newRawEdges = copy.copy(self.allEdges())
        marked_vertexes = set()
        for edge in edges:
            v1, v2 = edge.nodes
            if v1 != self.external_vertex and v2 != self.external_vertex:
                newRawEdges.remove(edge)
                marked_vertexes.add(v1)
                marked_vertexes.add(v2)
        newEdges = list()
        currVertexTransformationMap = dict()
        for edge in newRawEdges:
            copy_map = {}
            for v in edge.nodes:
                if v in marked_vertexes:
                    currVertexTransformationMap[v] = self._nextVertexIndex
                    copy_map[v] = self._nextVertexIndex
            if len(copy_map):
                newEdges.append(edge.copy(copy_map))
            else:
                newEdges.append(edge)
        return Graph(newEdges, external_vertex=self.external_vertex, renumbering=False), \
               self._nextVertexIndex, \
               vertex_transformation.add(VertexTransformation(currVertexTransformationMap))

    def shrinkToPoint(self, edges):
        return self._shrinkToPoint(edges)[0]

    def shrinkToPointWithAuxInfo(self, edges):
        return self._shrinkToPoint(edges)[0:2]

    def xRelevantSubGraphs(self,
                           filters=list(),
                           resultRepresentator=Representator.asGraph,
                           cutEdgesToExternal=True,
                           exact=True):
        allEdges = self.allEdges()
        simpleCache = dict()
        exactSubGraphIterator = graph_operations.x_sub_graphs(allEdges,
                                                              self._edges,
                                                              self.external_vertex,
                                                              cut_edges_to_external=cutEdgesToExternal)
        sgIterator = exactSubGraphIterator if exact else itertools.chain(exactSubGraphIterator, (allEdges,))
        for subGraphAsList in sgIterator:
            subGraphAsTuple = tuple(subGraphAsList)
            isValid = simpleCache.get(subGraphAsTuple, None)
            if isValid is None:
                isValid = True
                for aFilter in filters:
                    if not aFilter(subGraphAsList, self, allEdges):
                        isValid = False
                        break
            if isValid:
                yield resultRepresentator(subGraphAsList, self.external_vertex)

    def toGraphState(self):
        if self._graphState is None:
            self._graphState = graph_state.GraphState(self.allEdges(nickel_ordering=False))
        return self._graphState

    def getBoundVertexes(self):
        if self._boundVertexes is None:
            self._boundVertexes = set()
            for e in self.edges(self.external_vertex):
                self._boundVertexes.add(e.internal_nodes[0])
        return self._boundVertexes

    def getAllInternalEdgesCount(self):
        if self._allInternalEdgesCount is None:
            internalEdgesCount = 0
            for v, e in self._edges.items():
                internalEdgesCount += len(e)
            self._allInternalEdgesCount = internalEdgesCount / 2 - len(self._edges.get(self.external_vertex, tuple()))
        return self._allInternalEdgesCount

    def getLoopsCount(self):
        if self._loopsCount is None:
            externalLegsCount = len(self.edges(self.external_vertex))
            self._loopsCount = len(self.allEdges()) - externalLegsCount - (len(self.vertices()) -
                                                                           (1 if externalLegsCount != 0 else 0)) + 1
        return self._loopsCount

    def getPresentableStr(self):
        asStr = str(self)
        return asStr.split(":")[0]

    def removeTadpoles(self):
        no_tadpoles = filter(lambda e: e.nodes[0] != e.nodes[1], self.allEdges())
        return Graph(no_tadpoles, external_vertex=self.external_vertex)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.toGraphState())

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.toGraphState()) + 37 * hash(self.vertices())
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Graph):
            return False
        return self.toGraphState() == other.toGraphState() and self.vertices() == other.vertices()

    @staticmethod
    def dict_copy(some_dict):
        copied = dict()
        for (k, v) in some_dict.iteritems():
            copied[k] = list(v)
        return copied

    @staticmethod
    def fromStr(string, properties_config=None):
        return Graph(graph_state.GraphState.fromStr(string, properties_config=properties_config))

    @staticmethod
    def _parseEdges(edgesIterable):
        edgesDict = dict()
        for edge in edgesIterable:
            v1, v2 = edge.nodes
            Graph._insertEdge(edgesDict, v1, edge)
            if v1 != v2:
                Graph._insertEdge(edgesDict, v2, edge)
        return edgesDict

    @staticmethod
    def _persInsertEdge(edgesDict, edge):
        """
        persistent operation
        """
        vertices = set(edge.nodes)
        for v in vertices:
            Graph._insertEdge(edgesDict, v, edge)

    @staticmethod
    def _persDeleteEdge(edgesDict, edge):
        """
        persistent operation
        """
        vertices = set(edge.nodes)
        for v in vertices:
            Graph._deleteEdge(edgesDict, v, edge)

    @staticmethod
    def _insertEdge(edgesDict, vertex, edge):
        if vertex in edgesDict:
            edgesDict[vertex].append(edge)
        else:
            edgesDict[vertex] = [edge]

    @staticmethod
    def _deleteEdge(edgesDict, vertex, edge):
        try:
            edgeList = edgesDict[vertex]
            edgeList.remove(edge)
            if not len(edgesDict[vertex]):
                del edgesDict[vertex]
        except AttributeError as e:
            raise ValueError(e), "edge not exists in graph"


class VertexTransformation(object):
    def __init__(self, mapping=None):
        """
        self._mapping - only non-identical index mappings
        """
        self._mapping = mapping if mapping else dict()

    @property
    def mapping(self):
        return self._mapping

    def add(self, anotherVertexTransformation):
        """
        composition of 2 transformations
        """
        composedMapping = dict()
        usedKeys = set()
        for k, v in self._mapping.items():
            av = anotherVertexTransformation.mapping.get(v, None)
            if av:
                composedMapping[k] = anotherVertexTransformation.mapping[v]
                usedKeys.add(v)
            else:
                composedMapping[k] = v
        for k, v in anotherVertexTransformation.mapping.items():
            if k not in usedKeys:
                composedMapping[k] = v
        return VertexTransformation(composedMapping)

    def map(self, vertexIndex):
        indexMapping = self._mapping.get(vertexIndex, None)
        if indexMapping:
            return indexMapping
        return vertexIndex


ID_VERTEX_TRANSFORMATION = VertexTransformation()


class _IdAwareEdgeDelegate(object):
    """
    DO NOT USE IT OUTSIDE THIS PACKAGE

    used for comparing edges by id
    """
    def __init__(self, edge):
        self._edge = edge

    @property
    def edge(self):
        return self._edge

    def __hash__(self):
        return hash(self.edge.edge_id)

    def __eq__(self, other):
        return self.edge.edge_id == other.edge.edge_id