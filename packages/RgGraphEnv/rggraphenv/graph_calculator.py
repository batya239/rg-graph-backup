#!/usr/bin/python
# -*- coding: utf8
import storage
import atexit
import inject

__author__ = 'daddy-bear'


class GraphCalculatorManager(object):
    def __init__(self, *calculators):
        self._calculators = list(calculators)

    def get_calculator_for_class(self, a_class):
        for c in self._calculators:
            if isinstance(c, a_class):
                return c
        return None

    def add(self, calculator):
        calculator.init()
        self._calculators.append(calculator)
        return self

    def try_calculate(self, graph, put_value_to_storage=False):
        for c in self._calculators:
            if c.is_applicable(graph):
                res = c.calculate(graph)
                if res is not None:
                    if put_value_to_storage and not inject.instance(storage.StoragesHolder).get_graph(graph, "value"):
                        inject.instance(storage.StoragesHolder).put_graph(graph, res, "value")
                    return res, c.get_label()
        return None

    def dispose(self):
        while len(self._calculators):
            self._calculators.pop().dispose()

@atexit.register
def dispose():
    if inject.get_injector():
        inject.instance(GraphCalculatorManager).dispose()