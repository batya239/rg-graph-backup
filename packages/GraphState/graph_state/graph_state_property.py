#!/usr/bin/python
# -*- coding: utf8

__author__ = 'dima'


class PropertyGetAttrTrait(object):
    def __init__(self, from_edge=True):
        self._from_edge = from_edge

    def __getattr__(self, item):
        if self._properties is None:
            return None
        elif self._properties.has_property(item, from_edge=self._from_edge):
            return getattr(self._properties, item)
        return None


class Node(PropertyGetAttrTrait):
    def __init__(self, index, properties):
        super(Node, self).__init__(from_edge=False)
        assert properties is not None
        self._index = index
        self._node_index_str = str(index)
        self._properties = properties

    @property
    def index(self):
        return self._index

    def key(self):
        return self._properties.key()

    @property
    def node_index_str(self):
        return self._node_index_str

    def copy(self, new_node_index=None, **kwargs):
        if 'new_node' in kwargs:
            new_node = kwargs['new_node']
            return new_node if isinstance(new_node, Node) else Node(new_node, self._properties)
        properties_is_none = self._properties.is_none(from_edge=True)
        updated_properties = dict() if properties_is_none else self._properties.update(from_edge=False, **kwargs)
        return Node(self.index if new_node_index is None else new_node_index, updated_properties)

    def is_by_properties_equal(self, other_node_and_property):
        return self.index == other_node_and_property.index and self._properties == other_node_and_property._property

    def __cmp__(self, other):
        return cmp(self.index, other.index if isinstance(other, Node) else other)

    def __str__(self):
        return 'n[%s, %s]' % (self.node_index_str, str(self._properties)) if len(self._properties) else str(self.index)

    __repr__ = __str__

    def __eq__(self, other):
        return self.index == (other.index if isinstance(other, Node) else other)

    def __hash__(self):
        return hash(self.index)

    @staticmethod
    def build_if_need(node_indices_or_nodes, default_node_properties):
        return tuple(sorted(map(lambda n: n if isinstance(n, Node) else Node(n, default_node_properties), node_indices_or_nodes)))


# noinspection PyMethodMayBeStatic
class PropertyExternalizer(object):
    """
    Base externalizer superclass, can be used as is for numeric types
    """
    def serialize(self, obj):
        return str(obj)

    def deserialize(self, string):
        return eval(string)


class FakePropertyExternalizer(PropertyExternalizer):
    def deserialize(self, string):
        raise NotImplementedError()

    def serialize(self, obj):
        raise NotImplementedError()


class ExternalableProperty(object):
    def make_external(self, nodes, external_node):
        raise NotImplementedError()


class PropertyKey(object):
    def __init__(self,
                 name,
                 is_directed=False,
                 is_edge_property=True,
                 externalizer=FakePropertyExternalizer()):
        assert not is_directed or is_edge_property, 'node property can\'t be vector'
        self._name = name
        self._is_directed = is_directed
        self._externalizer = externalizer
        self._is_edge_property = is_edge_property

    @property
    def is_edge_property(self):
        return self._is_edge_property

    @property
    def name(self):
        return self._name

    @property
    def is_directed(self):
        return self._is_directed

    @property
    def externalizer(self):
        return self._externalizer

    def __eq__(self, other):
        assert isinstance(other, PropertyKey)
        return \
            self.name == other.name and \
            self.is_directed == other.is_directed and \
            self.externalizer == other.externalizer and \
            self.is_edge_property == other.is_edge_property

    def __hash__(self):
        h = hash(self.name)
        h = 31 * h + hash(self.is_directed)
        h = 31 * h + hash(self.externalizer)
        h = 31 * h + hash(self.is_edge_property)
        return h