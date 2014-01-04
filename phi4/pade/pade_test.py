#!/usr/bin/python
# -*- coding: utf8
import sys

__author__ = 'mkompan'

import sympy
import scipy.integrate as integrate
import math


def pade_aproximant(L, M, tau):
    numerator = 0
    for i in range(0, L + 1):
        coeff = sympy.var('a%s' % i)
        numerator += coeff * tau ** (i )
    denominator = 1
    for i in range(1, M + 1):
        coeff = sympy.var('b%s' % i)
        denominator += coeff * tau ** (i )

    return numerator, denominator


def dict2poly(series_dict, var):
    res = 0
    for power, coeff in series_dict.iteritems():
        res += var ** power * coeff
    return res


def eqs2matrix(eqs, vars):
    matrix_list = list()
    for eq in eqs:
        row = list()
        const = eq
        for var in vars:
            row.append(eq.coeff(var, 1))
            const = const.subs(var, 0)
        #        print "const", const
        row.append(-const)
        matrix_list.append(row)
    return sympy.Matrix(matrix_list)


def solve_pade_sympy(pade_num, pade_denom, series_dict, n, tau):
    vars = list()
    atoms = set()
    for poly in (pade_num, pade_denom):
        try:
            atoms = atoms | poly.atoms()
        except:
            pass
    for atom in atoms:
        if isinstance(atom, sympy.Symbol) and atom <> tau:
            vars.append(atom)
    series_poly = dict2poly(series_dict, tau)
    eq = (pade_num - pade_denom * series_poly).expand()
    eqs = list()
    for i in range(n + 1):
        eqs.append(eq.coeff(tau, i))
#    print "eq", eq , n
#    print "eqs", eqs
    return sympy.solve_linear_system(eqs2matrix(eqs, vars), *vars)


def borel_transform(series_dict, b=0):
    return dict(map(lambda x: (x, series_dict[x] / sympy.gamma(x + b + 1).evalf()), series_dict))


def resummation_pade(L, M, series_dict):
    tau = sympy.var('tau')
    padeNum, padeDenom = pade_aproximant(L, M, tau)
    padeFunc = padeNum / padeDenom
    res = solve_pade_sympy(padeNum, padeDenom, series_dict, L + M, tau)
#    print padeNum, padeDenom, res
    padeFunc_ = padeFunc
    for var, value in res.iteritems():
        var_ = sympy.var(str(var))
        padeFunc_ = padeFunc_.subs(var_, value)

    return padeFunc_.subs(tau, 1)

#FIXME : b!=0 !!!!
func_template = """
def func(x):
    tau = x/(1-x)
    res = math.exp(-tau) * ({pade})/(1-x)**2
    return res
"""


def resummation_pade_borel(L, M, series_dict, b=0):
    tau = sympy.var('tau')
    borel_dict = borel_transform(series_dict, b=b)
    padeNum, padeDenom = pade_aproximant(L, M, tau)
    padeFunc = padeNum / padeDenom
    res = solve_pade_sympy(padeNum, padeDenom, borel_dict, L + M, tau)
    #    print res
    padeFunc_ = padeFunc
    for var, value in res.iteritems():
        var_ = sympy.var(str(var))
        padeFunc_ = padeFunc_.subs(var_, value)


#    print func_template.format(pade=padeFunc_)
    exec(func_template.format(pade=padeFunc_))
    try:
        output = integrate.quad(func, 0., 1., full_output=1)
        result = output[0]
        if len(output)==4:
            warn = output[3]
        else:
            warn = None
        return result, warn
    except:
        return None, None
    #flag, result, error = integrate.qagiu(gfunc, 0, 1e-12, 1e-12, 100000, w)
    #return result


gStar_05 = {1: 1, 2: 0.716173621, 3: 0.095042867, 4: 0.086080396, 5: -0.204139}
gamma_minus_05 = {0: 1, 1: -1. / 3, 2: -0.113701246, 3: 0.024940678, 4: -0.039896059, 5: 0.0645212}
nu_minus_05 = {0: 2, 1: -2. / 3, 2: -0.2613686, 3: 0.0145746, 4: -0.0913127, 5: 0.118121}

from collections import namedtuple

results2013 = namedtuple('results2013', ('gamma', 'gamma_minus', 'nu', 'nu_minus', 'eta'))
#13
#n=1
n1 = results2013({0: 1, 1: 1. / 3, 2: 0.224812357, 3: 0.087897190, 4: 0.086443008, 5: -0.0180209},
                 {0: 1, 1: -1. / 3, 2: -0.113701246, 3: 0.024940678, 4: -0.039896059, 5: 0.0645210},
                 {0: 1./2, 1: 1. / 6, 2: 0.120897626, 3: 0.0584361287, 4: 0.056891652, 5: 0.00379868},
                 {0: 2., 1: -2. / 3, 2: -0.261368281, 3: 0.0145750797, 4: -0.091312521, 5: 0.118121},
                 {0: 0., 1: 0., 2: 0.0339661470, 3: 0.0466287623, 4: 0.030925471, 5: 0.0256843})


#n=0
n0 = results2013({0: 1, 1: 1. / 4, 2: 0.143242270, 3: 0.018272597, 4: 0.035251118, 5: -0.0634415},
                 {0: 1, 1: -1. / 4, 2: -0.08742270, 3: 0.037723538, 4: -0.028548147, 5: 0.0754631},
                 {0: 1./2, 1: 1. / 8, 2: 0.0787857831, 3: 0.0211750671, 4: 0.028101050, 5: -0.0222040},
                 {0: 2., 1: -1. / 2, 2: -0.190143132, 3: 0.0416216976, 4: -0.071673308, 5: 0.136330},
                 {0: 0., 1: 0., 2: 0.0286589366, 3: 0.0409908542, 4: 0.027138940, 5: 0.0236106})

#n=-1
nm1 = results2013({0: 1, 1: 1. / 7, 2: 0.060380873, 3: -0.023532210, 4: 0.012034268, 5: -0.0638772},
                  {0: 1, 1: -1. / 7, 2: -0.039972710, 3: 0.03786436, 4: -0.018392201, 5: 0.0649966},
                  {0: 1./2, 1: 1. / 14, 2: 0.0348693698, 3: -0.00424514372, 4: 0.011608435, 5: -0.0268913},
                  {0: 2., 1: -2. / 7, 2: -0.0986611527, 3: 0.0510003794, 4: -0.049264800, 5: 0.116842},
                  {0: 0., 1: 0., 2: 0.0187160402, 3: 0.0274103364, 4: 0.017144702, 5: 0.0159901})


#b = 0
#gStarBorel = borel_transform(gStar, b=0)
#print gStarBorel




def print_ds(series_dict):
    tau = sympy.var('tau')
    print "DS", dict2poly(series_dict, tau).subs(tau, 1)


def print_dsm1(series_dict):
    tau = sympy.var('tau')
    print "DS-1", 1/dict2poly(series_dict, tau).subs(tau, 1)


def print_pade(series_dict, N, m0=0, l0=0):
    print "Pade"
    print " "*10,
    for i in range(l0, N + 1):
        print "%10d" % (i),
    print
    for M in range(m0, N + 1):
        if l0 < N - M + 1:
            print "%10d" % M,
        for L in range(l0, N - M + 1):
            print "%10.4f" % (resummation_pade(L, M, series_dict)),
        print

def print_pade_minus(series_dict, N, m0=0, l0=0):
    print "Pade"
    print " "*10,
    for i in range(l0, N + 1):
        print "%10d" % (i),
    print
    for M in range(m0, N + 1):
        if l0 < N - M + 1:
            print "%10d" % M,
        for L in range(l0, N - M + 1):
            print "%10.4f" % (1/resummation_pade(L, M, series_dict)),
        print


def print_pade_borel(series_dict, N, m0=0, l0=0):
    print "Pade-Borel"
    #for L, M  in [(1,4), (3,2), (4,1)]:
    #    print (L,M), resummation_pade_borel(L, M, gamma_13_n1)
    print " "*10,
    for i in range(l0, N + 1):
        print "%10d" % (i),
    print
    for M in range(m0, N + 1):
        if l0 < N - M + 1:
            print "%10d" % M,
        for L in range(l0, N - M + 1):
        #        print M, L,
            #FIXME : unknown exception
            try:
                res, warn = resummation_pade_borel(L, M, series_dict)
            except:
                res = "    Except"
            if res is None:
                print "      None",
            elif isinstance(res, str):
                print res,
            else:
                if warn is not None:
                    print "%9.4fW" % res,
                else:
                    print "%9.4f " % res,
        print


def print_pade_borel_minus(series_dict, N, m0=0, l0=0):
    print "Pade-Borel-1"
    print (2, 3), 1/resummation_pade_borel(2, 3, series_dict)[0]
    print (3, 2), 1/resummation_pade_borel(3, 2, series_dict)[0]
    print " "*10,
    for i in range(l0, N + 1):
        print "%10d" % (i),
    print
    for M in range(m0, N + 1):
        if l0 < N - M + 1:
            print "%10d" % M,
        for L in range(l0, N - M + 1):
        #        print M, L,
            #FIXME : unknown exception
            try:
                res, warn = resummation_pade_borel(L, M, series_dict)
            except:
                res = "    Except"
            if res is None:
                print "      None",
            elif isinstance(res, str):
                print res,
            else:
                if warn is not None:
                    print "%9.4fW" % (1/res),
                else:
                    print "%9.4f " % (1/res),
        print



def calculate2013(result, N):

    print "gamma"

    print_ds(result.gamma)

    print_dsm1(result.gamma_minus)
    print_pade(result.gamma, N)
    print_pade_borel(result.gamma, N)

    print_pade_borel_minus(result.gamma_minus, N)

    print
    print "nu"
    print_ds(result.nu)
    print_dsm1(result.nu_minus)
    print_pade(result.nu, N)
    print_pade_borel(result.nu, N)
    print_pade_borel_minus(result.nu_minus, N)

    print
    print "eta"


    print_ds(result.eta)

    print "DS-1", "-------"

    print_pade(result.eta, N, l0=2)
    print_pade_borel(result.eta, N, l0=2)


if __name__ == "__main__":
    N = 5

    print "\ngStar\n"
    print_pade(gStar_05, N, l0=1)

    print "\ngamma^-1\n"
    print_pade_minus(gamma_minus_05, N)

    print "\nnu^-1\n"
    print_pade_minus(nu_minus_05, N)


    print 2013

    print "\n\nn=1"
    calculate2013(n1, N)

    print "\n\nn=0"
    calculate2013(n0, N)

    print "\n\nn=-1"
    calculate2013(nm1, N)