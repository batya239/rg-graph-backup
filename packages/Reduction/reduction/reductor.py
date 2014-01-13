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
import scalar_product


e = symbolic_functions.e


DEBUG = False


class ReductorHolder(object):
    def __init__(self, reductors):
        self._reductors = reductors

    def is_applicable(self, graph):
        for r in self._reductors:
            if r.is_applicable(graph):
                return True
        return False

    def calculate(self, graph, scalar_product_aware_function=None):
        for r in self._reductors:
            v = r.calculate(graph, scalar_product_aware_function)
            if v is not None:
                return v


def _enumerate_graph(graph, init_propagators, to_sector=True):
    """
    propagators - iterable of tuples (1, 0, -1) = q - k2

    to_sector = True => return sector.Sector
    to_sector = False => return graphine.Graph with corresponding colors
    """

    empty_color = graph_state.Rainbow(("EMPTY",))
    def init_colors(graph, zeroColor=graph_state.Rainbow((0, 0)), unitColor=graph_state.Rainbow((1, 0))):
        edges = graph.allEdges()
        initedEdges = list()
        for e in edges:
            if e.colors is None:
                color = zeroColor if graph.externalVertex in e.nodes else unitColor
                initedEdges.append(graph_state.Edge(e.nodes, graph.externalVertex, colors=color))
            else:
                initedEdges.append(e)
        return graphine.Graph(initedEdges, externalVertex=graph.externalVertex, renumbering=False)
    graph = init_colors(graph, empty_color, empty_color)

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
            new_edges = map(lambda e_: e_.copy(colors=graph_state.Rainbow((propagator_indices[e_.colors.colors], e_.colors)) if len(e_.internal_nodes) == 2 else None),
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
                        new_edges.append(not_enumerated[0].copy(colors=graph_state.Rainbow(propagator)))
                        new_graph = graphine.Graph(new_edges, externalVertex=external_vertex, renumbering=False)
                        _enumerate_next_vertex(new_remaining_propagators, new_graph, vertex + 1, result)
                else:
                    new_remaining_propagators = copy.copy(remaining_propagators)
                    new_remaining_propagators.remove(remaining_propagator)
                    new_edges = copy.copy(_graph.allEdges())
                    new_edges.remove(not_enumerated[0])
                    new_edges.append(not_enumerated[0].copy(colors=graph_state.Rainbow(propagator)))
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

    def __str__(self):
        return str(self._final_sector_linear_combinations)

    def evaluate(self, substitute_sectors=False, _d=None, series_n=-1, remove_o=True):
        if not substitute_sectors:
            return self._evaluate_unsubsituted(_d=_d, series_n=series_n, remove_o=remove_o)
        value = self._final_sector_linear_combinations.get_value(self._masters)
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
                remove_o=remove_o).normal()
        return sector.SectorLinearCombination(evaled_sectors_to_coefficients, evaled_additional_part)

    @staticmethod
    def _evaluate_coefficient(c, _d=None, series_n=-1, remove_o=True):
        if _d is None:
            return c
        if isinstance(c, (float, int)):
            return c
        _c = c.subs(sector.d == _d)
        return (_c if series_n == -1 else symbolic_functions.series(_c,
                                                                    e,
                                                                    0,
                                                                    series_n,
                                                                    remove_order=remove_o)).expand().collect(e)


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
        self._open_reduction_rules()
        self._scalar_product_rules = list()
        self._open_scalar_product_rules()
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
    def main_loops_condition(self):
        return self._main_loop_count_condition

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

    def _open_reduction_rules(self):
        dir_path = self._get_dir_path()

        zero_sectors = jrules_parser.read_raw_zero_sectors(os.path.join(dir_path, "ZeroSectors[%s]" % self._env_name),
                                                           self._env_name)
        self._zero_sectors = zero_sectors[1]
        for f in os.listdir(dir_path):
            if f.startswith("jRules"):
                map(lambda (k, r): self._sector_rules[k].append(r),
                    jrules_parser.x_parse_rules(os.path.join(dir_path, f), self._env_name, parse_symmetry=False))
            # elif f.startswith("jSymmetries"):
            #     map(lambda (k, r): self._sector_rules[k].append(r),
            #         jrules_parser.x_parse_rules(os.path.join(dir_path, f), self._env_name, parse_symmetry=True))
        # for v in self._sector_rules.values():
        #     pass #v.reverse()

    def _open_scalar_product_rules(self):
        self._scalar_product_rules = \
            jrules_parser.parse_scalar_products_reducing_rules(self._get_file_path(self._env_name),
                                                               self._env_name)

    def is_applicable(self, graph):
        if graph.getLoopsCount() != self._main_loop_count_condition:
            return False
        for e in graph.allEdges():
            if e.colors[1] != 0:
                return False
        return True

    def calculate(self, graph, scalar_product_aware_function=None):
        """
        scalar_product_aware_function(topology_shrunk, graph) returns iterable of scalar_product.ScalarProduct
        """
        if graph.getLoopsCount() != self._main_loop_count_condition:
            return None
        graph = Reductor.as_internal_graph(graph)
        if not scalar_product_aware_function:
            return self.evaluate_sector(sector.Sector.create_from_topologies_and_graph(graph,
                                                                                       self._topologies,
                                                                                       self._all_propagators_count))
        else:
            res = reduction_util.find_topology_for_graph(graph,
                                                         self._topologies,
                                                         scalar_product.find_topology_result_converter)
            if not res:
                return None
            s = sector.Sector.create_from_shrunk_topology(res[0], res[1], self._all_propagators_count)\
                .as_sector_linear_combinations()
            for sp in scalar_product_aware_function(*res):
                s = sp.apply(s, self._scalar_product_rules)
            return self.evaluate_sector(s)

    def _try_calculate(self, graph):
        return self.evaluate_sector(sector.Sector.create_from_topologies_and_graph(graph,
                                                                                   self._topologies,
                                                                                   self._all_propagators_count))

    def evaluate_sector(self, a_sector):
        if a_sector is None:
            return None
        sectors = a_sector.as_sector_linear_combinations()
        exist = set()
        while len(sectors):
            if DEBUG:
                print len(sectors), sectors.str_without_masters(self._masters.keys())
            not_masters = list()
            raw_sectors = sectors.sectors_to_coefficient.keys()
            for s in raw_sectors:
                if s.as_rule_key() in self._zero_sectors:
                    sectors = sectors.remove_sector(s)
                elif s not in self._masters.keys():
                    not_masters.append(s)

            if not len(not_masters):
                break

            key_to_sector = rggraphutil.emptyListDict()
            for s in not_masters:
                key_to_sector[s.as_rule_key()].append(s)
            minimal_key = min(key_to_sector.keys())
            rules = self._sector_rules[minimal_key]

            current_sectors_to_reduce = set(key_to_sector[minimal_key])
            n_exist = set()
            while len(current_sectors_to_reduce):
                s = current_sectors_to_reduce.pop()
                is_updated = False
                for rule in rules:
                    if rule.is_applicable(s):
                        new_sectors = rule.apply(s)
                        # if sector.Sector(1,0,-1,0,1,1,1,1,1) in new_sectors.sectors_to_coefficient.keys():
                        #     print "\n\n-----"
                        #     print len(filter(lambda r: r.is_applicable(s), rules))
                        #     print rule
                        #     print rule._apply_formula.format(None, *s.propagators_weights)
                        #     d = symbolic_functions.D
                        #     Sector = sector.Sector
                        #     qwe = eval(rule._apply_formula.format(None, *s.propagators_weights))
                        #     print "asd", qwe.sectors_to_coefficient[sector.Sector(1,0,-1,0,1,1,1,1,1)]
                        #     print s
                        #     print "Qeewsector.Sector(1,0,-1,0,1,1,1,1,1)"
                        #     print "\n\n-----"
                        #     exit(1)
                        n_exist.add(s)
                        do_continue = False
                        for x in new_sectors.sectors_to_coefficient.keys():
                            if x in exist:
                                do_continue = True
                                break
                        if do_continue:
                            continue
                        for n_s in new_sectors.sectors:
                            if n_s not in self._masters.keys() and n_s.as_rule_key() == minimal_key:
                                current_sectors_to_reduce.add(n_s)
                        is_updated = True
                        sectors = sectors.replace_sector_to_sector_linear_combination(s, new_sectors)
                        break
                assert is_updated, ("no rule for sector %s found" % s, exist)
            exist = exist | n_exist
        return ReductorResult(sectors, self._masters)

    def _get_file_path(self, file_name):
        dir_path = self._get_dir_path()
        file_path = os.path.join(dir_path, file_name)
        return file_path

    def _get_dir_path(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self._env_path)

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

    @staticmethod
    def as_internal_graph(graph):
        new_edges = list()
        if graph.getGraphStatePropertiesConfig() is graph_state.COLORS_AND_ARROW_PROPERTIES_CONFIG:
            return graph
        for e in graph.allEdges(nickel_ordering=True):
            colors = graph_state.Rainbow((1, 0)) if e.colors is None else e.colors
            arrow = graph_state.Arrow(graph_state.Arrow.NULL) if e.arrow is None else e.arrow
            new_edges.append(graph_state.COLORS_AND_ARROW_PROPERTIES_CONFIG.new_edge(e.nodes, colors=colors, arrow=arrow))
        return graphine.Graph(new_edges)


_MAIN_REDUCTION_HOLDER = ref.Ref.create()
_IS_INITIALIZED = ref.Ref.create(False)


def initialize(*reductors):
    if not _IS_INITIALIZED.get():
        _IS_INITIALIZED.set(True)
        _MAIN_REDUCTION_HOLDER.set(ReductorHolder(reductors))


def calculate(graph, scalar_product_aware_function=None):
    return _MAIN_REDUCTION_HOLDER.get().calculate(graph, scalar_product_aware_function)


def is_applicable(graph):
    return _MAIN_REDUCTION_HOLDER.get().is_applicable(graph)
