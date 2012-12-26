#!/usr/bin/python
# -*- coding:utf8
"""Module for generating of topologies of feynman graphs.
"""
import sys

import collections
import itertools

if sys.version_info < (2, 7):
    import comb
    itertools.combinations_with_replacement = comb.combinations_with_replacement

import nickel

# The node denoting a leg of a graph.
LEG = -1


def GetTopologies(valences_to_num_nodes):
    '''Yields nickel strings of one particle irreducible graphs.

    Arg:
         dict mapping valencies to num of nodes.
    '''
    topologies = set()
    initial_state = NickelPool(nickel=[], pool=valences_to_num_nodes)
    for nickpool in AddAllNodesFromPool(initial_state):
        topology = CanonicalString(nickpool.nickel)
        if topology in topologies:
            continue
        topologies.add(topology)
        yield topology


NickelPool = collections.namedtuple('NickelPool', 'nickel pool')


def AddAllNodesFromPool(nickpool):
    '''Yields NickelPool objects all nodes from pool added to nickel.'''
    nodes_left = CountNodesInPool(nickpool.pool)
    if nodes_left > 1:
        for deeper in AddNodeFromPool(nickpool):
            for recursive in AddAllNodesFromPool(deeper):
                yield recursive
    elif nodes_left == 1:
        for deepest in AddNodeFromPool(nickpool):
            if deepest.pool.get(1, 0) == 0:
                yield deepest
    else:
        yield nickpool


def AddNodeFromPool(nickpool):
    if IsOneParticleReducible(nickpool.nickel):
        return
    canonicals = set()

    node = len(nickpool.nickel)
    taken_valence = CountNode(nickpool.nickel, node)
    free_node = MaxNode(nickpool.nickel) + 1
    end_node = CountInternalNodes(nickpool)
    num_legs = nickpool.pool.get(1, 0)
    for valence in nickpool.pool:
        if nickpool.pool[valence] <= 0:
            continue
        if valence == 1:
            continue
        if valence < taken_valence:
            continue
        for add_nickel in AddEdges(valence - taken_valence,
                                   node, free_node, end_node, num_legs):
            new_nickel = list(nickpool.nickel) + [list(add_nickel)]
            # Update pool.
            new_pool = dict(nickpool.pool)
            new_pool[valence] -= 1
            if num_legs > 0:
                new_pool[1] -= add_nickel.count(LEG)

            if not NickelFitsPool(new_nickel, new_pool):
                continue

            canonical = CanonicalString(new_nickel)
            if canonical in canonicals:
                continue
            canonicals.add(canonical)

            yield NickelPool(nickel=new_nickel, pool=new_pool)


def IsOneParticleReducible(nickel_list):
    if not nickel_list:
        return False
    free_node = len(nickel_list)
    edges_to_pool = CountNode(nickel_list, free_node)
    # Disconnected.
    if edges_to_pool == 0:
        return True
    # Single edge goes to pool.
    if edges_to_pool == 1:
        if CountNode(nickel_list, free_node + 1) == 0:
            return True
    # Generated part is one particle reducible.
    edges = nickel.Nickel(nickel=nickel_list).edges
    if IsNCutDisconnectable(edges, 1):
        return True

    return False


def CountNode(nickel_list, node):
    return sum([nodes.count(node) for nodes in nickel_list])


def IsNCutDisconnectable(edges, num_to_cut):
    '''Returns true if cutting of num_to_cut edges disconnects the graph.'''
    # Brute force solution.
    for edges_part in itertools.combinations(edges, len(edges) - num_to_cut):
        if not nickel.IsConnected(edges_part):
            return True
    return False


def MaxNode(nickel_list):
    in_nickel = len(nickel_list) - 1
    from_pool = max(nickel.flatten(nickel_list) + [-1])
    return max(in_nickel, from_pool)


def CountInternalNodes(nickpool):
     return len(nickpool.nickel) + CountNodesInPool(nickpool.pool)


def CountNodesInPool(pool):
    return sum(pool.values()) - pool.get(1, 0)


def CountAllNodesInPool(pool):
    return sum(pool.values())


def CanonicalString(nickel_list):
    edges = nickel.Nickel(nickel=nickel_list).edges
    return str(nickel.Canonicalize(edges=edges))


def AddEdges(num_edges, start_node, free_node, end_node, num_legs):
    '''Yields all sorted combinations of legs and available nodes.

    Args:
        num_edges: number of edges to add
        start_node: first internal node to connect edges to. The edges connected to
             it are considered self-connected.
        free_node: the first node in pool which is not referenced in nickel.
        end_node: limit of the number of nodes.
        num_legs: maximum number of legs.
    '''
    # assert free_node > start_node
    free_node = free_node if free_node > start_node else start_node + 1
    leg = [LEG] if num_legs > 0 else []
    reachable_end =  min(free_node + num_edges, end_node)
    reachable_nodes = leg + range(start_node, reachable_end)
    for nodes in itertools.combinations_with_replacement(reachable_nodes, num_edges):
        if nodes.count(LEG) > num_legs:
            continue

        pool_nodes = [node for node in nodes if node >= free_node]
        if pool_nodes and not AreMinimalNodesFromPool(free_node, pool_nodes):
            continue

        # Avoid double accounting of self connected nodes.
        self_count = nodes.count(start_node)
        if self_count != 0:
            if self_count % 2 == 1:
                continue
            self_index = nodes.index(start_node)
            nodes = (nodes[:self_index + self_count/2] +
                     nodes[self_index + self_count:])

        yield nodes


def NickelFitsPool(nickel_list, node_pool):
    free_node = len(nickel_list)
    pool_nodes = [node for node in nickel.flatten(nickel_list) if node >= free_node]
    pool_nodes.sort()
    wanted_pool = {}
    for _, group_iter in itertools.groupby(pool_nodes):
        group_len = len(tuple(group_iter))
        wanted_pool[group_len] = wanted_pool.get(group_len, 0) + 1
    if MaxValenceInPool(wanted_pool) > MaxValenceInPool(node_pool):
        return False
    if CountAllNodesInPool(wanted_pool) > CountNodesInPool(node_pool):
        return False

    return True


def MaxValenceInPool(pool):
    valences = [valence for valence in pool if valence != 1 and pool[valence] > 0]
    if not valences:
        return 0
    return max(valences)


def AreMinimalNodesFromPool(free_node, pool_nodes):
    '''Optimization to find early non-minimal nickel list.'''
    if not pool_nodes:
        return True
    unique_nodes = []
    group_lengths = []
    for node, group_iter in itertools.groupby(pool_nodes):
        unique_nodes.append(node)
        group_lengths.append(len(tuple(group_iter)))
    # Detect gap.
    if unique_nodes[0] > free_node:
        return False
    if unique_nodes[-1] - unique_nodes[0] + 1 != len(unique_nodes):
        return False
    # Lengths of groups should be non-increasing.
    if group_lengths != sorted(group_lengths, reverse=True):
        return False

    return True


if __name__ == '__main__':
    pass
