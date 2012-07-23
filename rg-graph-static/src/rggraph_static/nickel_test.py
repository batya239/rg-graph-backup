#!/usr/bin/python

import nickel
import unittest

#TODO: Exclude generator tests from nickel tests

class TestNickel(unittest.TestCase):
    def testNickelFromEdges(self):
        e = nickel.Nickel(edges=[[0, -1], [-1, 0]])
        self.assertEqual(e.nickel, [[-1, -1]])
        self.assertEqual(e.string, 'ee-')

        s = nickel.Nickel(string='ee-')
        self.assertEqual(s.nickel, [[-1, -1]])
        self.assertEqual(s.edges, e.edges)

        ee = nickel.Nickel(edges=[[0, -1], [-1, 0], [2, 1], [1, 0]])
        self.assertEqual(ee.nickel, [[-1, -1, 1], [2]])
        self.assertEqual(ee.string, 'ee1-2-')

        ss = nickel.Nickel(string='ee1-2-')
        self.assertEqual(ss.nickel, [[-1, -1, 1], [2]])
        self.assertEqual(ss.edges, ee.edges)

        s1 = nickel.Nickel(string='eE-')
        self.assertEqual(s1.nickel, [[-1, 14]])
        self.assertEqual(s1.edges, [[-1, 0], [0, 14]])


class TestCanonicalize(unittest.TestCase):
    def testInit(self):
        c = nickel.Canonicalize([[-1, 0]])
        init = c.InitStates([[-1, 10]])
        self.assertEqual(len(init), 1)
        self.assertEqual(len(c.InitStates([[-1, 10], [10, 11], [11, -1]])), 2)

    def testRaise(self):
        self.assertRaises(nickel.InputError, nickel.Canonicalize, [[0, 1]])
        self.assertRaises(nickel.InputError, nickel.Canonicalize, [[0, 1], [2, 3]])

    def testCanon(self):
        c = nickel.Canonicalize([[-1, 0]])
        self.assertEqual(c.num_symmetries, 1)
        self.assertEqual(c.nickel, [[-1]])

    def testCanon1(self):
        c = nickel.Canonicalize([[-1, 0], [-1, 0]])
        self.assertEqual(c.num_symmetries, 1)
        self.assertEqual(c.nickel, [[-1, -1]])

    def testCanon2(self):
        c = nickel.Canonicalize([[-1, 10], [-1, 11], [10, 11]])
        self.assertEqual(c.nickel, [[-1, 1], [-1]])
        self.assertEqual(c.num_symmetries, 2)
        self.assertEqual(c.node_maps, [{10: 0, 11: 1}, {10: 1, 11: 0}])

    def testCanon3(self):
        c = nickel.Canonicalize([[-1, 11], [-1, 11], [-1, 10], [10, 11]])
        self.assertEqual(c.num_symmetries, 1)
        self.assertEqual(c.nickel, [[-1, -1, 1], [-1]])

    def testCanon4(self):
        c = nickel.Canonicalize([[-1, 0], [0, 1], [0, 2], [1, 2], [1, 3], [2, 3],
                                                        [3, -1]])
        self.assertEqual(c.num_symmetries, 4)
        self.assertEqual(c.nickel, [[-1, 1, 2], [2, 3], [3], [-1]])

    def testCanon5(self):
        c = nickel.Canonicalize([[-1, 3], [-1, 4], [-1, 5], [3, 4], [3, 5],
                                 [4, 6], [5, 7], [6, 8], [6, 8], [7, 9], [7, 9],
                                 [8, 10], [9, 11], [10, 11], [10, 11]])
        self.assertEqual(c.num_symmetries, 2)
        self.assertEqual(c.nickel, [[-1, 1, 2], [-1, 3], [-1, 4], [5, 5],
                                    [6, 6], [7], [8], [8, 8], []])

    def testCanon6(self):
        c = nickel.Canonicalize([[-1, 3], [-1, 4], [-1, 7], [3, 4], [3, 5],
                                 [4, 6], [5, 6], [5, 7], [6, 8], [7, 9], [8, 9],
                                 [8, 10], [9, 11], [10, 11], [10, 11]])
        self.assertEqual(c.num_symmetries, 1)
        self.assertEqual(c.nickel, [[-1, 1, 2], [-1, 3], [3, 4], [5], [-1, 6],
                                    [6, 7], [8], [8, 8], []])

    def testCanon7(self):
        c = nickel.Canonicalize([[-1, 2], [-1, 3], [2, 3], [2, 4], [3, 5],
                                 [4, 6], [4, 7], [5, 6], [5, 7], [6, 8], [7, 9],
                                 [8, 9], [8, 9]])
        self.assertEqual(c.num_symmetries, 4)
        self.assertEqual(c.nickel, [[-1, 1, 2], [-1, 3], [4, 5], [4, 5], [6],
                                    [7], [7, 7], []])


class TestGetGroupedEdges(unittest.TestCase):
    def testPermutatedFromCanonical(self):
        perm = nickel.PermutatedFromCanonical([{1: 'a', 2: 'b'},
                                               {1: 'b', 2: 'a'}])
        self.assertEqual(perm, [{1: 1, 2: 2}, {1: 2, 2: 1}])

    def test1(self):
        c = nickel.Canonicalize([[-1, 1], [1, 2], [2, -1]])
        self.assertEqual(c.GetGroupedEdges(),
                         [[[-1, 1], [2, -1]], [[1, 2]]])

    def test2(self):
      c = nickel.Canonicalize([[-1, 1], [1, 2], [1, 2], [2, -1]])
      self.assertEqual(c.GetGroupedEdges(),
                       [[[-1, 1], [2, -1]], [[1, 2], [1, 2]]])

    def test3(self):
      c = nickel.Canonicalize([[-1, 1], [1, 2], [1, 3], [2, 3],
                               [2, 4], [3, 4], [4, -1]])
      self.assertEqual(sorted(c.GetGroupedEdges()),
                       sorted([[[-1, 1], [4, -1]], [[2, 3]],
                               [[1, 2], [1, 3], [2, 4], [3, 4]]]))


class TestExpander(unittest.TestCase):
    def compareExpanders(self, l, r):
        self.assertEqual(l.curr_node, r.curr_node)
        self.assertEqual(l.free_node, r.free_node)
        self.assertEqual(l.edges, r.edges)
        self.assertEqual(l.nickel_list, r.nickel_list)
        self.assertEqual(l.node_map, r.node_map)

    def testExpand(self):
        input = nickel.Expander([[-1, 0]], [], {}, 0, 1)
        output = nickel.Expander([], [[-1]], {}, 1, 1)
        l = list(input.Expand())
        self.assertEqual(len(l), 1)
        self.compareExpanders(l[0], output)

    def testExpand2(self):
        input = nickel.Expander([[-1, 1], [1, 2], [1, 13], [1, 14]], [[1, 2]],
                                {10: 0, 11: 1, 12: 2}, 1, 3)
        output = nickel.Expander([], [[1, 2], [-1, 2, 3, 4]],
                                 {10: 0, 11: 1, 12: 2, 13: 3, 14: 4}, 2, 5)
        l = list(input.Expand())
        self.assertEqual(len(l), 2)
        self.compareExpanders(l[0], output)

    def testStopExpand(self):
        output = nickel.Expander([], [[-1, 1]], {10: 1}, 1, 2)
        l = list(output.Expand())
        self.assertEqual(l[0].nickel_list, [[-1, 1], []])

    def testCmp(self):
        input = nickel.Expander([[-1, 0], [0, 10]], [], {}, 0, 1)
        output = nickel.Expander([], [[-1, 1]], {10: 1}, 1, 2)
        self.assertEqual(input, output)



class TestUtil(unittest.TestCase):
    def testAdjacentNodes(self):
        self.assertEqual(nickel.AdjacentNodes(1, [[1, 0], [0, 2], [2,1]]),
                         [0, 2])
        self.assertEqual(nickel.AdjacentNodes(0, [[-1, 0]]), [-1])

    def testIsConnected(self):
        conn = nickel.IsConnected
        self.assertFalse(conn([]))
        self.assertTrue(conn([[0, 1]]))
        self.assertTrue(conn([(0, 1)]))
        self.assertTrue(conn(((0, 1),)))
        self.assertTrue(conn([[-1, 0], [0, 1]]))
        self.assertFalse(conn([[-1, 0], [2, 1]]))
        self.assertTrue(conn([[1, 0], [3, 4], [1, 2], [2, 3]]))


if __name__ == "__main__":
    unittest.main()

