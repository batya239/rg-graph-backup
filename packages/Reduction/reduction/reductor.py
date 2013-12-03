#!/usr/bin/python
# -*- coding: utf8
import copy
from rggraphenv import symbolic_functions
import rggraphutil

__author__ = 'dimas'

import os
from rggraphutil import ref
from rggraphenv import abstract_graph_calculator
import graphine

import jrules_parser
import sector
import reduction_util
import graph_state


class ReductorHolder(object):
    def __init__(self, reductors):
        self._reductors = reductors

    def is_applicable(self, graph):
        for r in self._reductors:
            if r.is_applicable(graph):
                return True
        return False

    def calculate(self, graph):
        for r in self._reductors:
            v = r.calculate(graph)
            if v is not None:
                return v


def _enumerate_graph(graph, init_propagators, to_sector=True):
    """
    propagators - iterable of tuples (1, 0, -1) = q - k2

    to_sector = True => return sector.Sector
    to_sector = False => return graphine.Graph with corresponding colors
    """

    empty_color = graph_state.Rainbow(("EMPTY",))
    graph = graphine.Graph.initEdgesColors(graph, empty_color, empty_color)

    neg_init_propagators = dict()
    for p in init_propagators:
        neg_p = tuple(map(lambda q: -q, p))
        neg_init_propagators[p] = neg_p

    propagator_indices = dict()
    for p in enumerate(init_propagators):
        propagator_indices[p[1]] = p[0]
        propagator_indices[neg_init_propagators[p[1]]] = p[0]

    momentum_count = len(init_propagators[0])
    external_vertex = graph.externalVertex
    graph_vertices = graph.vertices()

    def _enumerate_next_vertex(remaining_propagators, _graph, vertex, result):
        if vertex not in graph_vertices:
            new_edges = map(lambda e_: e_.copy(
                colors=propagator_indices[e_.colors.colors] if len(e_.internal_nodes) == 2 else None),
                            _graph.allEdges())
            result.add(graphine.Graph(new_edges, external_vertex, renumbering=False))
            return
        vertex_known_factor = [0] * momentum_count
        not_enumerated = list()
        for e in _graph.edges(vertex):
            if e.colors is not empty_color:
                for i in xrange(momentum_count):
                    if vertex == e.nodes[0]:
                        vertex_known_factor[i] += e.colors[i]
                    else:
                        vertex_known_factor[i] -= e.colors[i]
            elif len(e.internal_nodes) == 1:
                if vertex == 0:
                    vertex_known_factor[0] += 1
                else:
                    vertex_known_factor[0] -= 1
            else:
                not_enumerated.append(e)
        if not len(not_enumerated):
            for x in vertex_known_factor:
                if x != 0:
                    return
            _enumerate_next_vertex(remaining_propagators, _graph, vertex + 1, result)
            return
        for remaining_propagator in remaining_propagators:
            neg_propagator = neg_init_propagators[remaining_propagator]
            for propagator in (remaining_propagator, neg_propagator):
                if len(not_enumerated) == 1:
                    is_zero = True
                    for x in zip(vertex_known_factor, propagator):
                        if x[0] + x[1] != 0:
                            is_zero = False
                            break
                    if is_zero:
                        new_remaining_propagators = copy.copy(remaining_propagators)
                        new_remaining_propagators.remove(remaining_propagator)
                        new_edges = copy.copy(_graph.allEdges())
                        new_edges.remove(not_enumerated[0])
                        new_edges.append(not_enumerated[0].copy(colors=propagator))
                        new_graph = graphine.Graph(new_edges, externalVertex=external_vertex, renumbering=False)
                        _enumerate_next_vertex(new_remaining_propagators, new_graph, vertex + 1, result)
                else:
                    new_remaining_propagators = copy.copy(remaining_propagators)
                    new_remaining_propagators.remove(remaining_propagator)
                    new_edges = copy.copy(_graph.allEdges())
                    new_edges.remove(not_enumerated[0])
                    new_edges.append(not_enumerated[0].copy(colors=propagator))
                    new_graph = graphine.Graph(new_edges, externalVertex=external_vertex, renumbering=False)
                    _enumerate_next_vertex(new_remaining_propagators, new_graph, vertex, result)

    _result = set()
    _enumerate_next_vertex(init_propagators, graph, 0, _result)
    if not to_sector:
        return _result
    else:
        sector_result = set()
        for g in _result:
            raw_sector = [0] * len(init_propagators)
            for e in g.internalEdges():
                raw_sector[e.colors[0]] = 1
            sector_result.add(sector.Sector(raw_sector))
        return sector_result


class ReductorResult(object):
    def __init__(self, final_sector_linear_combinations, masters):
        self._masters = masters
        self._final_sector_linear_combinations = final_sector_linear_combinations

    def evaluate(self, substitute_sectors=False, _d=None, series_n=-1, remove_o=True):
        if not substitute_sectors:
            return self._evaluate_unsubsituted(_d=_d, series_n=series_n, remove_o=remove_o).normalize()
        value = self._final_sector_linear_combinations.normalize().get_value(self._masters)
        return ReductorResult._evaluate_coefficient(value, _d=_d, series_n=series_n, remove_o=remove_o)

    def _evaluate_unsubsituted(self, _d=None, series_n=-1, remove_o=True):
        evaled_additional_part = ReductorResult._evaluate_coefficient(
            self._final_sector_linear_combinations.additional_part,
            _d=_d,
            series_n=series_n,
            remove_o=remove_o)
        evaled_sectors_to_coefficients = rggraphutil.zeroDict()
        for s, c in self._final_sector_linear_combinations.sectors_to_coefficient.items():
            evaled_sectors_to_coefficients[s] = ReductorResult._evaluate_coefficient(
                c,
                _d=_d,
                series_n=series_n,
                remove_o=remove_o)
        return sector.SectorLinearCombination(evaled_sectors_to_coefficients, evaled_additional_part)

    @staticmethod
    def _evaluate_coefficient(c, _d=None, series_n=-1, remove_o=True):
        if _d is None:
            return c
        if isinstance(c, (float, int)):
            return c
        _c = c.subs(sector.d == _d)
        return (_c if series_n == -1 else symbolic_functions.series(_c,
                                                                    symbolic_functions.e,
                                                                    0,
                                                                    series_n,
                                                                    remove_order=remove_o)).expand().collect(symbolic_functions.e)


class Reductor(object):
    TOPOLOGIES_FILE_NAME = "topologies"
    MASTERS_FILE_NAME = "masters"

    def __init__(self,
                 env_name,
                 env_path,
                 topologies,
                 main_loop_count_condition,
                 masters):
        self._env_name = env_name
        self._env_path = env_path
        self._main_loop_count_condition = main_loop_count_condition
        self._propagators = jrules_parser.parse_propagators(self._get_file_path(self._env_name),
                                                            self._main_loop_count_condition)
        read_topologies = self._try_read_topologies()

        if read_topologies:
            self._topologies = read_topologies
        else:
            self._topologies = reduce(lambda ts, t: ts | _enumerate_graph(t, self._propagators, to_sector=False),
                                      topologies,
                                      set())
            self._save_topologies()
        self._all_propagators_count = len(self._propagators)
        self._sector_rules = rggraphutil.emptyListDict()
        self._zero_sectors = list()
        self._open_j_rules()
        read_masters = self._try_read_masters()
        if read_masters:
            self._masters = read_masters
        else:
            self._masters = dict()
            master_sectors = jrules_parser.parse_masters(self._get_file_path(self._env_name),
                                                         self._env_name)
            for m, v in masters.items():
                for enumerated in _enumerate_graph(m, self._propagators, to_sector=True):
                    if enumerated in master_sectors:
                        self._masters[enumerated] = v
            self._save_masters()

    @property
    def env_name(self):
        """
        test only
        """
        return self._env_name

    @property
    def env_path(self):
        """
        test only
        """
        return self._env_path

    def evaluate_sector_size(self):
        """
        test only
        """
        for s in self._masters.keys():
            return len(s.propagators_weights)
        raise AssertionError()

    def _open_j_rules(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self._env_path)

        zero_sectors = jrules_parser.read_raw_zero_sectors(os.path.join(dir_path, "ZeroSectors[%s]" % self._env_name),
                                                           self._env_name)
        self._zero_sectors = zero_sectors[1]
        for f in os.listdir(dir_path):
            if f.startswith("jRules"):
                map(lambda (k, r): self._sector_rules[k].append(r),
                    jrules_parser.x_parse_rules(os.path.join(dir_path, f), self._env_name))
        for v in self._sector_rules.values():
            v.reverse()

    def is_applicable(self, graph):
        if graph.getLoopsCount() != self._main_loop_count_condition:
            return False
        for e in graph.allEdges():
            if e.colors[1] != 0:
                return False
        return True

    def calculate(self, graph):
        if graph.getLoopsCount() != self._main_loop_count_condition:
            return None
        return self._try_calculate(graph)

    def _try_calculate(self, graph):
        return self.evaluate_sector(sector.Sector.create_from_topologies_and_graph(graph,
                                                                                   self._topologies,
                                                                                   self._all_propagators_count))

    def evaluate_sector(self, a_sector):
        if a_sector is None:
            return None
        sectors = a_sector.as_sector_linear_combinations()
        calculated_sectors = dict()
        while len(sectors):
            raw_sectors = sectors.sectors_to_coefficient.keys()
            not_masters = list()
            for s in raw_sectors:
                is_break = False
                s.as_rule_key()
                if s.as_rule_key() in self._zero_sectors:
                    sectors = sectors.remove_sector(s)
                    is_break = True
                if is_break:
                    continue
                if s not in self._masters.keys():
                    not_masters.append(s)

            if not len(not_masters):
                break

            biggest = reduction_util.choose_max(not_masters)
            is_updated = False
            if biggest not in calculated_sectors:
                key = biggest.as_rule_key()
                current_rules = self._sector_rules.get(key, None)
                assert current_rules
                for rule in current_rules:
                    if rule.is_applicable(biggest):
                        new_sectors = rule.apply(biggest)
                        calculated_sectors[biggest] = new_sectors
                        sectors = sectors.replace_sector_to_sector_linear_combination(biggest, new_sectors)
                        is_updated = True
                        break
            else:
                is_updated = True
                sectors = sectors.replace_sector_to_sector_linear_combination(biggest, calculated_sectors.get(biggest))

            if not is_updated:
                return None
        return ReductorResult(sectors, self._masters)

    def _get_file_path(self, file_name):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self._env_path)
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def _get_topologies_file_path(self):
        return self._get_file_path(Reductor.TOPOLOGIES_FILE_NAME)

    def _get_masters_file_path(self):
        return self._get_file_path(Reductor.MASTERS_FILE_NAME)

    def _try_read_topologies(self):
        file_path = self._get_topologies_file_path()
        if os.path.exists(file_path):
            topologies = set()
            with open(file_path, 'r') as f:
                for s in f:
                    topologies.add(graphine.Graph.fromStr(s))
                return topologies
        return None

    def _save_topologies(self):
        file_path = self._get_topologies_file_path()
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                for t in self._topologies:
                    f.write(str(t) + "\n")
        else:
            raise ValueError("file %s already exists" % file_path)

    def _try_read_masters(self):
        file_path = self._get_masters_file_path()
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                masters = dict()
                for s in f:
                    raw_sector, raw_value = s.split(";")
                    masters[sector.Sector(eval(raw_sector))] = symbolic_functions.evaluate(raw_value)
                return masters
        return None

    def _save_masters(self):
        file_path = self._get_masters_file_path()
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                for s, v in self._masters.iteritems():
                    f.write(
                        str(s.propagators_weights) + ";" + symbolic_functions.safe_integer_numerators(str(v)) + "\n")
        else:
            raise ValueError("file %s already exists" % file_path)


_MAIN_REDUCTION_HOLDER = ref.Ref.create()

_IS_INITIALIZED = ref.Ref.create(False)

G = symbolic_functions.G
l = symbolic_functions.l

THREE_LOOP_REDUCTOR = Reductor("loop3",
                               "loop3",
                               [graphine.Graph.fromStr("e12-34-35-4-5-e-"),
                                graphine.Graph.fromStr("e12-34-34-5-5-e-")],
                               3,
                               {graphine.Graph.fromStr("e12-34-34-5-5-e-"):
                                symbolic_functions.evaluate("(20*zeta(5))"
                                                                "+(-80*zeta(5)+10/189*Pi**6+68*zeta(3)**2)*e"
                                                                "+(80*zeta(5)+450*zeta(7)+34/15*Pi**4*zeta(3)-40/189*Pi**6-272*zeta(3)**2)*e**2"
                                                                "+(-1800*zeta(7)+8519/13500*Pi**8-136/15*Pi**4*zeta(3)+40/189*Pi**6-9072/5*Z_5_3-2448*zeta(5)*zeta(3)+272*zeta(3)**2)*e**3"
                                                                "+Order(e**4)"),
                                graphine.Graph.fromStr("e11-22-33-e-"): G(1, 1) ** 3,
                                graphine.Graph.fromStr("e112-22-e-"): G(1, 1) * G(1, 1) * G(2 - 2 * l, 1),
                                graphine.Graph.fromStr("e11-222-e-"): G(1, 1) * G(1, 1) * G(1 - l, 1),
                                graphine.Graph.fromStr("e1111-e-"): G(1, 1) * G(1 - l, 1) * G(1 - 2 * l, 1),
                                graphine.Graph.fromStr("e12-223-3-e-"):
                                symbolic_functions.evaluate("1/3*e**(-3)+1/3*e**(-2)+1/3*e**(-1)+(-7/3+14/3*zeta(3))"
                                                            "+(-67/3+7/90*Pi**4+14/3*zeta(3))*e"
                                                            "+(-403/3+126*zeta(5)+7/90*Pi**4+86/3*zeta(3))*e**2"
                                                            "+(-2071/3+126*zeta(5)+43/90*Pi**4+26/81*Pi**6+478/3*zeta(3)-226/3*zeta(3)**2)*e**3"
                                                            "+(-9823/3+534*zeta(5)+1960*zeta(7)-113/45*Pi**4*zeta(3)+239/90*Pi**4+26/81*Pi**6+2446/3*zeta(3)-226/3*zeta(3)**2)*e**4"
                                                            "+Order(e**5)")})


TWO_LOOP_REDUCTOR = Reductor("loop2",
                             "loop2",
                             [graphine.Graph.fromStr("e12-23-3-e-")],
                             2,
                             {graphine.Graph.fromStr("e111-e-"): G(1, 1) * G(1 - l, 1),
                              graphine.Graph.fromStr("e11-22-e-"): G(1, 1) ** 2})


def initialize(*reductors):
    if not _IS_INITIALIZED.get():
        _IS_INITIALIZED.set(True)
        _MAIN_REDUCTION_HOLDER.set(ReductorHolder(reductors))


def calculate(graph):
    return _MAIN_REDUCTION_HOLDER.get().calculate(graph)


def is_applicable(graph):
    return _MAIN_REDUCTION_HOLDER.get().is_applicable(graph)


class TwoAndThreeReductionCalculator(abstract_graph_calculator.AbstractGraphCalculator):
    def get_label(self):
        return "reduction calculator"

    def init(self):
        initialize(TWO_LOOP_REDUCTOR, THREE_LOOP_REDUCTOR)

    def is_applicable(self, graph):
        return is_applicable(graph)

    def calculate(self, graph):
        result = calculate(graph)
        if result is None:
            return None
        return result.evaluate(substitute_sectors=True, _d=symbolic_functions.D, series_n=5, remove_o=True), \
               TwoAndThreeReductionCalculator._calculate_p_factor(graph)

    @staticmethod
    def _calculate_p_factor(graph):
        factor0 = 0
        for e in graph.internalEdges():
            factor0 += e.colors[0]
        return factor0 - graph.getLoopsCount(), - graph.getLoopsCount()

    def dispose(self):
        pass