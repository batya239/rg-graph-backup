__author__ = 'gleb'

from pole_extractor import diagram_calculator

d1 = diagram_calculator.calculate_diagram(label='e12|e3|e4|56|78|78|78|||',
                                          theory=3,
                                          max_eps=1,
                                          zero_momenta=True,
                                          force_update=False)
d2 = diagram_calculator.get_expansion('e12|e3|e4|56|78|78|78|||', rprime=False, momentum_derivative=False)
print '#####\n' + str(d1)
print d2
print str(d1.cut(2) == d2.cut(2)) + '\n#####'