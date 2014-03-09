__author__ = 'gleb'

import unittest
import math

import graphine
from pole_extractor import diagram_calculator
from pole_extractor import numcalc


class TestBaseValuesPhi3(unittest.TestCase):
    def testOneLoop(self):
        e1 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e11|e|'),
                                              rprime=False, momentum_derivative=True)
        e1_ = numcalc.NumEpsExpansion({-1: [-1.0 / 6.0, 0.0], 0: [0.25, 0.0],
                                       1: [-1.0 / 12.0 - math.pi**2 / 36.0, 0.0]}, precise=True)
        self.assertEqual(e1.cut(2), e1_)

        e2 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e2|e|'),
                                              rprime=False, momentum_derivative=False)
        e2_ = numcalc.NumEpsExpansion({-1: [0.5, 0.0], 0: [-0.75, 0.0],
                                       1: [math.pi**2 / 12.0 + 0.25, 0.0]}, precise=True)
        self.assertEqual(e2.cut(2), e2_)

        e3 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e2||'),
                                              rprime=False, momentum_derivative=True)
        e3_ = numcalc.NumEpsExpansion({0: [-1.0 / 12.0, 0.0], 1: [0.125, 0.0],
                                       2: [-math.pi**2 / 72.0 - 1.0 / 24.0, 0.0]}, precise=True)
        self.assertEqual(e3.cut(3), e3_)

    def testTwoLoops(self):
        e3 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|23|3|e|'),
                                              rprime=False, momentum_derivative=True)
        e3_ = numcalc.NumEpsExpansion({-2: [-1.0 / 12.0, 0.0], -1: [7.0 / 36.0, 0.0]}, precise=True)
        self.assertEqual(e3.cut(0), e3_)

        e4 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e3|33||'),
                                              rprime=False, momentum_derivative=True)
        e4_ = numcalc.NumEpsExpansion({-2: [1.0 / 72.0, 0.0], -1: [23.0 / 432.0, 0.0]}, precise=True)
        self.assertEqual(e4.cut(0), e4_)

        e5 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e3|34|4|e|'),
                                              rprime=False, momentum_derivative=False)
        e5_ = numcalc.NumEpsExpansion({-2: [0.125, 0.0], -1: [-0.3125, 0.0]}, precise=True)
        self.assertEqual(e5.cut(0), e5_)

        e6 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e3|e4|44||'),
                                              rprime=False, momentum_derivative=False)
        e6_ = numcalc.NumEpsExpansion({-2: [-1.0 / 24.0, 0.0], -1: [-0.0625, 0.0]}, precise=True)
        self.assertEqual(e6.cut(0), e6_)

        e7 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|34|34|e|e|'),
                                              rprime=False, momentum_derivative=False)
        e7_ = numcalc.NumEpsExpansion({-1: [0.25, 0.0]}, precise=True)
        self.assertEqual(e7.cut(0), e7_)


class TestRprValuesPhi3(unittest.TestCase):
    """
    Vassiliev pg 415
    """
    def testOneLoop(self):
        e1 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e11|e|'),
                                              rprime=True, momentum_derivative=True)
        e1_ = numcalc.NumEpsExpansion({-1: [-1.0 / 6.0, 0.0], 0: [0.25, 0.0],
                                       1: [-1.0 / 12.0 - math.pi**2 / 36.0, 0.0]}, precise=True)
        self.assertEqual(e1.cut(2), e1_)

        e2 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e2|e|'),
                                              rprime=True, momentum_derivative=False)
        e2_ = numcalc.NumEpsExpansion({-1: [0.5, 0.0], 0: [-0.75, 0.0],
                                       1: [math.pi**2 / 12.0 + 0.25, 0.0]}, precise=True)
        self.assertEqual(e2.cut(2), e2_)

    def testTwoLoops(self):
        e1 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|23|3|e|'),
                                              rprime=True, momentum_derivative=True)
        e1_ = numcalc.NumEpsExpansion({-2: [1.0 / 12.0, 0.0], -1: [-2.0 / 36.0, 0.0]}, precise=True)
        self.assertEqual(e1.cut(0), e1_)

        e2 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e3|33||'),
                                              rprime=True, momentum_derivative=True)
        e2_ = numcalc.NumEpsExpansion({-2: [-1.0 / 72.0, 0.0], -1: [11.0 / 432.0, 0.0]}, precise=True)
        self.assertEqual(e2.cut(0), e2_)

        e3 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e3|34|4|e|'),
                                              rprime=True, momentum_derivative=False)
        e3_ = numcalc.NumEpsExpansion({-2: [-1.0 / 8.0, 0.0], -1: [1.0 / 16.0, 0.0]}, precise=True)
        self.assertEqual(e3.cut(0), e3_)

        e4 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|e3|e4|44||'),
                                              rprime=True,
                                              momentum_derivative=False)
        e4_ = numcalc.NumEpsExpansion({-2: [1.0 / 24.0, 0.0], -1: [-7.0 / 144.0, 0.0]}, precise=True)
        self.assertEqual(e4.cut(0), e4_)

        e5 = diagram_calculator.get_expansion(graphine.Graph.fromStr('e12|34|34|e|e|'),
                                              rprime=True,
                                              momentum_derivative=False)
        e5_ = numcalc.NumEpsExpansion({-1: [0.25, 0.0]}, precise=True)
        self.assertEqual(e5.cut(0), e5_)


class TestBaseValuesPhi4(unittest.TestCase):
    def testOneLoop(self):
        e1 = 2.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|ee|'),
                                                    rprime=False,
                                                    momentum_derivative=False)
        e1_ = numcalc.NumEpsExpansion({-1: [1.0, 0.0]}, precise=True)
        self.assertEqual(e1.cut(0), e1_)

    def testSimpleLoops(self):
        e1 = 2.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|ee|'),
                                                    rprime=False,
                                                    momentum_derivative=False)
        e3 = 4.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|22|ee|'),
                                                    rprime=False,
                                                    momentum_derivative=False)
        e3_ = e1 * e1
        self.assertEqual(e3.cut(4), e3_.cut(4))

        e6 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|22|33|ee|'),
                                                    rprime=False,
                                                    momentum_derivative=False)
        e6_ = e1 * e1 * e1
        self.assertEqual(e6.cut(3), e6_.cut(3))


class TestRprValuesPhi4(unittest.TestCase):
    """
    Vassiliev pg 277
    """
    def testOneLoop(self):
        e1 = 2.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|ee|'),
                                                    rprime=False,
                                                    momentum_derivative=False)
        e1_ = numcalc.NumEpsExpansion({-1: [1.0, 0.0]}, precise=True)
        self.assertEqual(e1.cut(0), e1_)

    def testTwoLoops(self):
        e2 = 4.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('e111|e|'),
                                                    rprime=True,
                                                    momentum_derivative=True)
        e2_ = numcalc.NumEpsExpansion({-1: [-0.25, 0.0]}, precise=True)
        self.assertEqual(e2.cut(0), e2_)

        e3 = 4.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|22|ee|'),
                                                    rprime=True,
                                                    momentum_derivative=False)
        e3_ = numcalc.NumEpsExpansion({-2: [-1.0, 0.0], -1: [0.0, 0.0]}, precise=True)
        self.assertEqual(e3.cut(0), e3_)

        e4 = 4.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee12|e22|e|'),
                                                    rprime=True,
                                                    momentum_derivative=False)
        e4_ = numcalc.NumEpsExpansion({-2: [-0.5, 0.0], -1: [0.5, 0.0]}, precise=True)
        self.assertEqual(e4.cut(0), e4_)

    def testThreeLoops(self):
        e5 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('e112|22|e|'),
                                                    rprime=True,
                                                    momentum_derivative=True)
        e5_ = numcalc.NumEpsExpansion({-2: [1.0 / 6.0, 0.0], -1: [-1.0 / 12.0, 0.0]}, precise=True)
        self.assertEqual(e5.cut(0), e5_)

        e6 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|22|33|ee|'),
                                                    rprime=True,
                                                    momentum_derivative=False)
        e6_ = numcalc.NumEpsExpansion({-3: [1.0, 0.0], -2: [0.0, 0.0], -1: [0.0, 0.0]}, precise=True)
        self.assertEqual(e6.cut(0), e6_)

        e7 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee11|23|e33|e|'),
                                                    rprime=True,
                                                    momentum_derivative=False)
        e7_ = numcalc.NumEpsExpansion({-3: [0.5, 0.0], -2: [-0.5, 0.0], -1: [0.0, 0.0]}, precise=True)
        self.assertEqual(e7.cut(0), e7_)

        e8 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee12|ee3|333||'),
                                                    rprime=True,
                                                    momentum_derivative=False)
        e8_ = numcalc.NumEpsExpansion({-2: [1.0 / 6.0, 0.0], -1: [-0.375, 0.0]}, precise=True)
        self.assertEqual(e8.cut(0), e8_)

        e9 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee12|e33|e33||'),
                                                    rprime=True,
                                                    momentum_derivative=False)
        e9_ = numcalc.NumEpsExpansion({-3: [1.0 / 3.0, 0.0], -2: [-1.0 / 3.0, 0.0],
                                       -1: [-1.0 / 3.0, 0.0]}, precise=True)
        self.assertEqual(e9.cut(0), e9_)

        e10 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('e112|e3|e33|e|'),
                                                     rprime=True,
                                                     momentum_derivative=False)
        e10_ = numcalc.NumEpsExpansion({-3: [1.0 / 3.0, 0.0], -2: [-1.0 / 3.0, 0.0],
                                       -1: [-1.0 / 3.0, 0.0]}, precise=True)
        self.assertEqual(e10.cut(0), e10_)

        e11 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee12|e23|33|e|'),
                                                     rprime=True,
                                                     momentum_derivative=False)
        e11_ = numcalc.NumEpsExpansion({-3: [1.0 / 6.0, 0.0], -2: [-0.5, 0.0], -1: [2.0 / 3.0, 0.0]}, precise=True)
        self.assertEqual(e11.cut(0), e11_)

        e12 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('e123|e23|e3|e|'),
                                                     rprime=True,
                                                     momentum_derivative=False)
        e12_ = numcalc.NumEpsExpansion({-1: [2.404113806, 0.0]}, precise=True)
        self.assertEqual(e12.cut(0), e12_)

        e13 = 8.0 * diagram_calculator.get_expansion(graphine.Graph.fromStr('ee12|223|3|ee|'),
                                                     rprime=True,
                                                     momentum_derivative=False)
        e13_ = numcalc.NumEpsExpansion({-3: [1.0 / 3.0, 0.0], -2: [-2.0 / 3.0, 0.0],
                                        -1: [1.0 / 3.0, 0.0]}, precise=True)
        self.assertEqual(e13.cut(0), e13_)


class TestVacuumLoopsPhi3(unittest.TestCase):
    """
    Check that sum of diagrams adds up to sum of vacuum loops.
    """
    def testTwoLoops(self):
        g2_2 = (('e12|e3|33||', 0.5), ('e12|23|3|e|', 0.5))
        g3_2 = (('e12|e3|e4|44||', 1.5), ('e12|e3|34|4|e|', 3.0), ('e12|34|34|e|e|', 0.5))

        vl = diagram_calculator.get_expansion(graphine.Graph.fromStr('111||'),
                                              rprime=False,
                                              momentum_derivative=False) * (1.0 / 12.0)

        vl *= numcalc.NumEpsExpansion(exp={0: [-3.0, 0.0], 1: [2.0, 0.0]}, precise=True)
        vl *= numcalc.NumEpsExpansion(exp={0: [-2.0, 0.0], 1: [2.0, 0.0]}, precise=True)
        d2 = numcalc.NumEpsExpansion(exp={}, precise=True)
        for l, c in g2_2:
            d2 += diagram_calculator.get_expansion(graphine.Graph.fromStr(l),
                                                   rprime=False,
                                                   momentum_derivative=False) * c
        self.assertEqual(vl.cut(3), d2.cut(3))

        vl *= numcalc.NumEpsExpansion(exp={0: [-1.0, 0.0], 1: [2.0, 0.0]}, precise=True)
        d3 = numcalc.NumEpsExpansion(exp={}, precise=True)
        for l, c in g3_2:
            d3 += diagram_calculator.get_expansion(graphine.Graph.fromStr(l),
                                                   rprime=False,
                                                   momentum_derivative=False) * c
        self.assertEqual(vl.cut(3), d3.cut(3))

    def testThreeLoops(self):
        g0_3 = (('112|3|33||', 0.0625), ('123|23|3||', 1.0/24.0))
        g2_3 = (('e12|23|4|45|5|e|', 0.5),  ('e12|34|35|e|55||', 0.25), ('e12|e3|44|55|5||', 0.25),
                ('e12|23|4|e5|55||', 1.0),  ('e12|e3|45|45|5||', 0.5),  ('e12|34|35|4|5|e|', 1.0),
                ('e12|34|34|5|5|e|', 0.25), ('e12|e3|34|5|55||', 0.5),  ('e12|33|44|5|5|e|', 0.125))
        g3_3 = (('e12|e3|45|46|e|66||', 1.5),  ('e12|e3|34|5|e6|66||', 3.0),  ('e12|e3|45|45|6|6|e|', 1.5),
                ('e12|34|56|e5|e6|6||', 1.0),  ('e12|33|45|6|e6|e6||', 1.5),  ('e12|23|4|e5|56|6|e|', 3.0),
                ('e12|e3|e4|45|6|66||', 1.5),  ('e12|34|35|6|e6|e6||', 1.0),  ('e12|23|4|56|56|e|e|', 1.5),
                ('e12|e3|e4|55|66|6||', 0.75), ('e12|e3|44|56|5|6|e|', 3.0),  ('e12|e3|34|5|56|6|e|', 3.0),
                ('e12|e3|45|46|5|6|e|', 6.0),  ('e12|23|4|e5|e6|66||',  1.5), ('e12|e3|e4|56|56|6||', 1.5),
                ('e12|34|35|6|e5|6|e|', 3.0),  ('e12|e3|44|55|6|6|e|', 0.75))

        vl = numcalc.NumEpsExpansion(exp={}, precise=True)
        d2 = numcalc.NumEpsExpansion(exp={}, precise=True)
        d3 = numcalc.NumEpsExpansion(exp={}, precise=True)

        #for l, c in g0_3:
        #    vl += diagram_calculator.get_expansion(graphine.Graph.fromStr(l),
        #                                           rprime=False,
        #                                           momentum_derivative=False) * c
        for l, c in g2_3:
            d2 += diagram_calculator.get_expansion(graphine.Graph.fromStr(l),
                                                   rprime=False,
                                                   momentum_derivative=False) * c
        for l, c in g3_3:
            d3 += diagram_calculator.get_expansion(graphine.Graph.fromStr(l),
                                                   rprime=False,
                                                   momentum_derivative=False) * c

        vl *= numcalc.NumEpsExpansion(exp={0: [-3.0, 0.0], 1: [3.0, 0.0]}, precise=True)
        vl *= numcalc.NumEpsExpansion(exp={0: [-2.0, 0.0], 1: [3.0, 0.0]}, precise=True)

        #self.assertEqual(vl[-3], d2[-3])
        #self.assertEqual(vl[-2], d2[-2])
        #self.assertEqual(vl[-1], d2[-1])

        vl *= numcalc.NumEpsExpansion(exp={0: [-1.0, 0.0], 1: [3.0, 0.0]}, precise=True)

        #self.assertEqual(vl[-3], d3[-3])
        #self.assertEqual(vl[-2], d3[-2])
        #self.assertEqual(vl[-1], d3[-1])
