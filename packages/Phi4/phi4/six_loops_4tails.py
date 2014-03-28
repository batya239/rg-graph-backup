#!/usr/bin/python
# -*- coding: utf8

__author__ = 'dima'


import logging
import graph_state
import graphine
import graph_util
import common
import r
import itertools
import time
import configure
import numerators_util
import ir_uv
import const
import smtplib
from rggraphenv import symbolic_functions, graph_calculator, storage, theory, g_graph_calculator, StorageSettings, StoragesHolder
from email.mime.text import MIMEText


class SixLoops4Tails(object):
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s")
    LOG = logging.getLogger("SixLoops4Tails")
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(logging.FileHandler("6loops_4tails_log.txt", mode='w'))
    r.ROperation.set_debug(True)

    def __init__(self, do_r_star=False, calculators=tuple(), calculated_mappings=dict()):
        self._calculator = calculators[0].get_label() if len(calculators) else None
        self._calculated_mappings = calculated_mappings
        graph_calculators_to_use = (g_graph_calculator.GLoopCalculator(const.DIM_PHI4),) + tuple(calculators)
        configure.Configure()\
            .with_k_operation(common.MSKOperation())\
            .with_ir_filter(ir_uv.IRRelevanceCondition(const.SPACE_DIM_PHI4))\
            .with_uv_filter(ir_uv.UVRelevanceCondition(const.SPACE_DIM_PHI4))\
            .with_dimension(const.DIM_PHI4)\
            .with_calculators(*graph_calculators_to_use)\
            .with_storage_holder(StorageSettings("phi4", "main method", "6 loops 4 tails").on_shutdown(revert=True)).configure()
        operator = r.ROperation()
        self._operation = operator.kr_star if do_r_star else operator.kr1

    def start(self, graph_states_to_calculate):
        SixLoops4Tails.LOG.info("start calculation using %s graph_calculator, %s operation" % (self._calculator, self._operation.__name__))
        ms = time.time()
        not_calculated = list()
        for gs in graph_states_to_calculate:
            gs = str(graph_state.GraphState.fromStr(gs))
            graph = graph_util.graph_from_str(gs, do_init_weight=True)
            try:
                SixLoops4Tails.LOG.info("start evaluate %s" % gs)
                res = self._operation(graph)
                SixLoops4Tails.LOG.info("kr1[%s] = %s" % (gs, res))
                self._calculated_mappings[gs] = res
            except common.CannotBeCalculatedError:
                SixLoops4Tails.LOG.warning("can't calculate %s used %s graph_calculator, %s operation"
                                           % (gs, self._calculator, self._operation.__name__))
                not_calculated.append(gs)
            except StandardError as e:
                SixLoops4Tails.LOG.error("error while calculate %s used %s graph_calculator, %s operation"
                                         % (gs, self._calculator, self._operation.__name__))
                SixLoops4Tails.LOG.exception(e)
                not_calculated.append(gs)
        SixLoops4Tails.LOG.info("calculation with %s graph_calculator, %s operation done in %s, calculated %s graphs"
                                % (self._calculator, self._operation.__name__, (time.time() - ms), (len(graph_states_to_calculate) - len(not_calculated))))
        return not_calculated

    # noinspection PyMethodMayBeStatic
    def dispose(self):
        configure.Configure.clear()


def main():
    reductions_loops = (2, 3, 4),
    operations = (False, True)

    calculated_mappings = dict()
    current_graphs = SIX_LOOPS
    for config in itertools.product(operations, reductions_loops):
        if config[1] is None:
            calculator = tuple()
        else:
            calculator = (numerators_util.create_calculator(*config[1]),)
        operation = config[0]
        master = SixLoops4Tails(operation, calculator, calculated_mappings)
        current_graphs = master.start(current_graphs)
        master.dispose()

SIX_LOOPS = [
    "ee12|334|355|e|666|e6||",
    "ee12|234|35|45|e6|66|e|",
    "ee12|e33|445|45|6|66|e|",
    "ee12|e33|e44|45|6|666||",
    "e112|34|356|56|e56|e|e|",
    "ee12|233|34|5|ee6|666||",
    "ee12|334|355|6|ee6|66||",
    "ee12|ee3|456|456|56|6||",
    "ee12|e34|335|5|e66|66||",
    "ee12|345|346|45|6|e6|e|",
    "ee12|334|456|e5|e6|66||",
    "ee12|e33|445|56|e6|66||",
    "ee12|333|445|6|56|e6|e|",
    "ee12|334|455|e6|56|6|e|",
    "ee12|e33|445|e5|66|66||",
    "ee12|e34|356|45|56|6|e|",
    "ee12|334|335||e56|66|e|",
    "ee12|334|456|55|e6|6|e|",
    "ee12|223|4|455|66|e6|e|",
    "ee12|234|34|e5|56|66|e|",
    "ee12|e34|355|66|566|e||",
    "e112|33|e45|46|e5|66|e|",
    "ee12|e34|556|e66|556|||",
    "ee12|ee3|344|56|56|66||",
    "e112|e3|e44|556|66|e6||",
    "ee12|333|456|4|56|e6|e|",
    "ee12|334|556|45|e6|6|e|",
    "ee12|334|556|e6|e56|6||",
    "ee12|e33|344|5|56|66|e|",
    "ee12|345|345|ee|66|66||",
    "ee12|345|345|e6|56|6|e|",
    "e112|e3|456|456|e5|6|e|",
    "ee12|334|345|6|ee|666||",
    "ee12|e34|335|4|66|e66||",
    "ee12|234|35|46|e5|66|e|",
    "ee12|e34|355|45|66|6|e|",
    "ee12|334|345|e|e6|666||",
    "ee12|e33|e34|5|566|66||",
    "ee12|233|44|55|56|6|ee|",
    "e112|34|e56|e45|66|e6||",
    "ee12|234|56|e56|e56|6||",
    "ee12|e23|e4|555|666|6||",
    "ee12|ee3|345|45|66|66||",
    "ee12|334|455|66|ee|66||",
    "e112|e3|445|446||e66|e|",
    "ee12|e34|556|e46|56|6||",
    "ee12|e34|335|4|e6|666||",
    "e123|e23|e4|45|e6|666||",
    "e112|e3|445|466|5|e6|e|",
    "e112|e3|344|45|6|e66|e|",
    "e123|e24|e5|e46|56|66||",
    "ee12|233|45|46|66|ee6||",
    "ee12|e23|45|e66|556|6||",
    "e112|34|556|e45|e6|6|e|",
    "ee12|e34|345|56|56|6|e|",
    "ee12|233|45|66|e56|e6||",
    "ee12|345|346|55|66|e|e|",
    "ee12|233|45|44|6|e66|e|",
    "e112|e3|e44|e45|6|666||",
    "ee12|e33|445|56|66|e6||",
    "e112|33|e34|5|e66|e66||",
    "ee12|334|456|45|6|e6|e|",
    "ee12|223|4|556|566|e|e|",
    "e112|e3|e45|466|56|e6||",
    "ee12|233|34|5|666|ee6||",
    "ee12|e23|44|555|66|6|e|",
    "ee12|ee3|345|46|56|66||",
    "e112|33|e45|46|56|e6|e|",
    "ee12|234|35|ee|566|66||",
    "ee12|e34|556|456|66|e||",
    "ee12|e33|456|45|e6|66||",
    "ee12|e33|e44|55|66|66||",
    "e112|e3|334|5|e66|e66||",
    "e123|e45|e46|e56|56|6||",
    "ee12|334|355|5|e66|6|e|",
    "e112|e3|345|46|56|e6|e|",
    "ee12|345|346|e4|5|66|e|",
    "ee12|233|45|e4|56|66|e|",
    "ee12|e34|335|6|566|e6||",
    "ee12|e34|555|456|66||e|",
    "ee12|234|35|44|6|e66|e|",
    "ee12|334|345|5|e6|66|e|",
    "ee12|e23|45|666|e55|6||",
    "ee12|234|34|e5|e6|666||",
    "ee12|e34|345|45|6|66|e|",
    "e112|e3|e45|446|e|666||",
    "ee12|e23|45|e46|56|66||",
    "ee12|e34|355|56|666|e||",
    "e112|34|e35|46|e6|e66||",
    "e112|34|e35|66|e55|6|e|",
    "e112|34|e35|e6|566|e6||",
    "e123|e24|55|e46|e6|66||",
    "ee12|e34|e56|445|6|66||",
    "ee12|233|45|e4|e6|666||",
    "ee12|e23|34|55|566|6|e|",
    "e123|e23|e4|56|e56|66||",
    "ee12|333|456|4|e5|66|e|",
    "ee12|334|355|6|556||ee|",
    "e112|23|e4|e56|e56|66||",
    "ee12|233|34|5|566|e6|e|",
    "ee12|334|455|46|e|66|e|",
    "ee12|334|345|e|66|e66||",
    "ee12|e34|335|e|566|66||",
    "ee12|334|345|4|6|e66|e|",
    "ee12|e33|445|e6|56|66||",
    "ee12|334|356|e|556|6|e|",
    "ee12|233|45|e6|e56|66||",
    "e112|34|356|e5|e56|6|e|",
    "e112|e3|e45|446|6|e66||",
    "ee12|e34|356|56|556||e|",
    "ee12|334|456|55|66|e|e|",
    "ee12|334|556|e6|556||e|",
    "ee12|233|44|e5|66|e66||",
    "ee12|334|355|e|566|6|e|",
    "ee12|233|45|e6|556|6|e|",
    "ee12|223|4|e56|e56|66||",
    "ee12|e34|345|56|66|e6||",
    "ee12|e33|444|55|6|66|e|",
    "ee12|e33|345|6|556|6|e|",
    "ee12|345|345|45|6|6|ee|",
    "e112|e3|e34|45|e6|666||",
    "ee12|e23|45|446|e|666||",
    "ee12|e23|45|466|56|e6||",
    "ee12|333|445|5|e6|66|e|",
    "ee12|223|4|e45|e6|666||",
    "ee12|334|345|6|e5|66|e|",
    "e112|e3|345|46|e5|66|e|",
    "ee12|e23|44|456|5|66|e|",
    "ee12|334|455|46|5|6|ee|",
    "ee12|e34|356|44|5|66|e|",
    "ee12|334|556|55|e66||e|",
    "ee12|e34|e56|456|56|6||",
    "ee12|234|35|66|e55|6|e|",
    "ee12|223|4|456|56|e6|e|",
    "ee12|334|455|e6|e6|66||",
    "e112|34|e34|56|56|e6|e|",
    "ee12|e33|e44|56|56|66||",
    "ee12|333|445|6|e6|e66||",
    "ee12|e33|456|44|5|66|e|",
    "ee12|e34|356|56|e56|6||",
    "ee12|e23|34|56|556|6|e|",
    "ee12|334|455|e6|66|e6||",
    "ee12|e34|335|6|556|6|e|",
    "ee12|e34|335|5|666|e6||",
    "ee12|e23|34|55|666|e6||",
    "ee12|e34|556|446|6|e6||",
    "ee12|234|35|46|56|e6|e|",
    "ee12|e34|e34|45|6|666||",
    "ee12|e34|556|e44|6|66||",
    "ee12|e33|444|e5|6|666||",
    "e112|23|e4|e45|56|66|e|",
    "e112|34|e56|445|6|e6|e|",
    "ee12|334|556|e5|e66|6||",
    "e123|e24|35|e6|566|e6||",
    "ee12|334|345|6|e6|e66||",
    "ee12|e34|556|e56|566|||",
    "ee12|e23|34|e5|566|66||",
    "ee12|e34|e56|555|666|||",
    "e112|33|456|e4|56|e6|e|",
    "ee12|334|355|6|e66|e6||",
    "ee12|e33|445|46|e|666||",
    "e112|34|e35|e6|556|6|e|",
    "ee12|e34|345|e4|6|666||",
    "ee12|345|346|ee|56|66||",
    "e123|e24|56|e45|e6|66||",
    "ee12|e23|44|556|66|e6||",
    "ee12|ee3|344|45|6|666||",
    "e112|e3|445|456|6|e6|e|",
    "ee12|234|35|46|e6|e66||",
    "ee12|e33|e45|45|66|66||",
    "ee12|e33|445|e4|6|666||",
    "ee12|233|44|45|6|e66|e|",
    "ee12|334|556|e5|566||e|",
    "e112|34|356|e5|e66|e6||",
    "ee12|ee3|445|466|5|66||",
    "e112|33|e45|e4|e6|666||",
    "ee12|ee3|445|456|6|66||",
    "e123|e45|e46|456|5|6|e|",
    "ee12|e33|345|6|e56|66||",
    "e123|e24|56|445|6|e6|e|",
    "e112|34|e56|e56|556||e|",
    "ee12|e23|34|45|66|e66||",
    "ee12|234|35|46|ee|666||",
    "ee12|334|556|56|e56||e|",
    "ee12|e34|335|5|566|6|e|",
    "e112|34|e35|66|e56|e6||",
    "ee12|334|556|e4|56|6|e|",
    "e112|e3|e34|56|556|6|e|",
    "e112|23|44|e55|e6|66|e|",
    "ee12|e23|44|455|6|66|e|",
    "e112|34|e34|55|66|e6|e|",
    "ee12|234|35|e4|56|66|e|",
    "ee12|e33|345|4|e6|666||",
    "e112|e3|445|466|e|e66||",
    "ee12|e33|e45|66|556|6||",
    "ee12|e34|355|56|566||e|",
    "ee12|e34|356|45|66|e6||",
    "ee12|e34|355|44|6|66|e|",
    "ee12|334|556|e4|e6|66||",
    "e112|34|555|e46|e6|6|e|",
    "ee12|234|35|46|55|6|ee|",
    "e112|23|45|e46|e5|66|e|",
    "ee12|334|345|5|66|e6|e|",
    "ee12|e34|556|e45|66|6||",
    "ee12|234|56|e56|556||e|",
    "ee12|334|345|6|55|6|ee|",
    "ee12|345|346|45|5|6|ee|",
    "e112|23|34|56|e56|e6|e|",
    "ee12|e34|e56|455|66|6||",
    "e123|e24|56|e56|556||e|",
    "e123|e24|35|e6|e56|66||",
    "ee12|e34|e35|44|6|666||",
    "ee12|234|35|46|66|ee6||",
    "ee12|e34|356|45|e6|66||",
    "ee12|334|456|56|55||ee|",
    "ee12|e34|555|e46|66|6||",
    "ee12|e23|45|446|5|66|e|",
    "ee12|e34|555|e66|566|||",
    "ee12|334|556|46|e5|6|e|",
    "ee12|233|44|e5|56|66|e|",
    "ee12|e23|45|456|56|6|e|",
    "ee12|e23|44|556|56|6|e|",
    "e112|34|e35|56|566|e|e|",
    "e112|34|e35|56|e66|e6||",
    "ee12|334|345|6|66|ee6||",
    "ee12|334|556|e5|666|e||",
    "ee12|223|4|e56|556|6|e|",
    "ee12|e34|355|46|56|6|e|",
    "ee12|e33|456|45|56|6|e|",
    "ee12|345|346|e5|66|e6||",
    "e123|456|456|456|e|e|e|",
    "ee12|e34|356|e5|566|6||",
    "e112|e3|e45|e46|56|66||",
    "e112|23|e4|556|566|e|e|",
    "e112|e3|e34|55|566|6|e|",
    "e112|e3|444|556|6|e6|e|",
    "ee12|234|34|56|56|e6|e|",
    "e112|23|e4|556|e56|6|e|",
    "e112|34|335|6|e56|e6|e|",
    "e112|23|e4|455|66|e6|e|",
    "e112|e3|e44|e55|66|66||",
    "ee12|e23|44|e56|56|66||",
    "e112|23|e4|455|e6|66|e|",
    "ee12|334|456|e5|56|6|e|",
    "ee12|334|456|56|ee|66||",
    "ee12|234|35|e6|556|6|e|",
    "ee12|e23|34|56|e56|66||",
    "ee12|223|4|455|56|6|ee|",
    "e112|23|45|456|e6|e6|e|",
    "ee12|e34|355|66|e56|6||",
    "e112|e3|e34|55|666|e6||",
    "ee12|333|444|5|6|e66|e|",
    "e112|34|e56|455|66|e|e|",
    "ee12|e33|344|5|e6|666||",
    "ee12|234|56|e44|5|66|e|",
    "e112|e3|344|56|e5|66|e|",
    "ee12|ee3|344|55|66|66||",
    "ee12|345|346|e5|56|6|e|",
    "e112|34|e56|e56|e56|6||",
    "e112|23|45|e45|e6|66|e|",
    "ee12|234|35|e6|e56|66||",
    "ee12|e23|e4|556|566|6||",
    "e112|e3|e34|e5|566|66||",
    "e112|33|445|e5|e6|66|e|",
    "e123|e24|35|66|e56|e6||",
    "e112|34|e35|46|56|e6|e|",
    "e112|34|356|e5|566|e|e|",
    "e112|34|556|e56|e56||e|",
    "ee12|234|56|e55|566||e|",
    "e123|e23|45|46|56|e6|e|",
    "e112|23|45|e46|e6|e66||",
    "ee12|334|356|5|ee6|66||",
    "e112|34|e55|e46|56|6|e|",
    "ee12|e33|e45|46|56|66||",
    "e112|34|e34|e5|e6|666||",
    "ee12|334|345|e|56|66|e|",
    "ee12|234|56|e45|56|6|e|",
    "ee12|334|556|66|e55||e|",
    "e112|34|e35|e6|e56|66||",
    "e112|33|445|e6|e6|e66||",
    "ee12|334|456|e5|66|e6||",
    "e112|34|e35|e5|666|e6||",
    "e112|23|45|466|e5|e6|e|",
    "e112|34|345|e6|56|e6|e|",
    "e112|23|45|e66|e56|e6||",
    "ee12|e34|556|456|56||e|",
    "e112|33|e45|66|e56|e6||",
    "ee12|334|356|e|e56|66||",
    "ee12|234|56|ee5|566|6||",
    "e112|23|44|e56|56|e6|e|",
    "e123|e24|56|e56|e56|6||",
    "ee12|334|335||e66|e66||",
    "ee12|234|34|55|66|e6|e|",
    "e112|e3|e45|456|56|6|e|",
    "ee12|e23|44|e55|66|66||",
    "ee12|334|356|5|556||ee|",
    "e112|e3|e45|446|5|66|e|",
    "ee12|e34|356|55|666|e||",
    "ee12|e34|335|6|e56|66||",
    "ee12|e23|44|556|e6|66||",
    "e112|33|456|45|e6|e6|e|",
    "e112|23|e4|e55|566|6|e|",
    "e112|e3|e34|45|56|66|e|",
    "ee12|e34|345|e5|66|66||",
    "e112|34|345|e6|e6|e66||",
    "ee12|e34|334|5|66|e66||",
    "e112|34|356|45|e6|e6|e|",
    "e112|33|e45|46|e6|e66||",
    "ee12|345|346|e4|e|666||",
    "e123|e24|35|e4|e6|666||",
    "ee12|ee3|445|446||666||",
    "ee12|223|4|e55|e66|66||",
    "e112|33|e44|e5|66|e66||",
    "ee12|233|45|66|e55|6|e|",
    "ee12|e34|355|46|e6|66||",
    "ee12|e33|445|66|e5|66||",
    "ee12|e34|334|5|56|66|e|",
    "e112|34|e35|45|66|e6|e|",
    "ee12|333|445|6|55|6|ee|",
    "e112|23|e4|e55|e66|66||",
    "ee12|334|355|4|e6|66|e|",
    "ee12|334|355|e|e66|66||",
    "ee12|e33|456|e4|56|66||",
    "ee12|223|4|e45|56|66|e|",
    "e112|e3|e44|456|5|66|e|",
    "ee12|e34|e35|66|556|6||",
    "e112|e3|445|566|e6|e6||",
    "e112|e3|e45|666|e55|6||",
    "ee12|234|35|66|ee5|66||",
    "ee12|e34|e34|55|66|66||",
    "ee12|e34|e35|45|66|66||",
    "ee12|233|44|56|56|e6|e|",
    "ee12|345|346|e5|e6|66||",
    "e112|e3|e34|55|e66|66||",
    "ee12|345|345|e6|e6|66||",
    "ee12|334|345|6|56|e6|e|",
    "ee12|e33|345|4|66|e66||",
    "ee12|233|45|45|56|6|ee|",
    "ee12|e33|344|5|66|e66||",
    "ee12|e33|445|66|56|e6||",
    "e123|e24|e5|e45|66|66||",
    "ee12|233|45|46|55|6|ee|",
    "ee12|334|356|5|e66|e6||",
    "ee12|e34|345|46|6|e66||",
    "ee12|e34|355|46|66|e6||",
    "ee12|334|356|4|56|e6|e|",
    "ee12|e33|445|46|6|e66||",
    "ee12|334|356|4|e5|66|e|",
    "ee12|e34|555|e56|666|||",
    "ee12|334|556|e6|566|e||",
    "ee12|333|445|6|66|ee6||",
    "e112|33|345|6|e56|e6|e|",
    "ee12|e34|335|4|56|66|e|",
    "ee12|e33|e45|44|6|666||",
    "ee12|334|355|6|566|e|e|",
    "e112|e3|e44|455|6|66|e|",
    "e112|34|e35|45|e6|66|e|",
    "e123|e45|e45|466|e|66||",
    "ee12|234|56|e55|e66|6||",
    "ee12|234|34|45|6|e66|e|",
    "ee12|e34|334|5|e6|666||",
    "ee12|234|35|e4|66|e66||",
    "e123|e45|e45|e46|6|66||",
    "e112|e3|e44|556|e6|66||",
    "ee12|334|456|e4|5|66|e|",
    "e112|e3|e45|445|6|66|e|",
    "ee12|233|45|e4|66|e66||",
    "e112|23|e4|556|e66|e6||",
    "ee12|e34|356|55|e66|6||",
    "ee12|233|45|46|56|e6|e|",
    "ee12|334|456|56|56|e|e|",
    "e112|34|e56|456|56|e|e|",
    "ee12|e23|45|446|6|e66||",
    "ee12|e23|45|456|e6|66||",
    "ee12|223|4|ee5|566|66||",
    "e123|e23|44|56|56|e6|e|",
    "e112|e3|345|45|e6|66|e|",
    "e112|e3|e34|56|e56|66||",
    "ee12|233|45|46|e6|e66||",
    "e112|e3|334|5|e56|66|e|",
    "ee12|334|556|46|55||ee|",
    "ee12|223|4|e55|666|e6||",
    "ee12|334|355|6|e56|6|e|",
    "ee12|e34|555|446|6|6|e|",
    "ee12|e33|445|46|5|66|e|",
    "e123|e24|56|e45|66|e6||",
    "ee12|e34|556|e55|666|||",
    "ee12|333|445|4|6|e66|e|",
    "ee12|e23|44|e45|6|666||",
    "ee12|334|355|4|66|e6|e|",
    "e112|23|e4|e56|556|6|e|",
    "e112|33|e44|56|56|e6|e|",
    "e112|33|445|56|e6|e6|e|",
    "e112|34|e56|e45|56|6|e|",
    "ee12|334|556|e4|66|e6||",
    "ee12|e23|e4|455|66|66||",
    "e112|34|e56|e45|e6|66||",
    "ee12|233|45|45|e6|66|e|",
    "ee12|e23|34|45|56|66|e|",
    "e123|e23|e4|56|556|6|e|",
    "ee12|e23|45|466|e5|66||",
    "ee12|ee3|445|566|56|6||",
    "e112|34|e35|66|556|e|e|",
    "ee12|e33|444|56|5|66|e|",
    "e112|e3|e44|e56|56|66||",
    "ee12|e34|e34|56|56|66||",
    "ee12|e23|45|e44|6|666||",
    "e123|e24|35|46|56|e6|e|",
    "e112|23|e4|456|56|e6|e|",
    "e112|23|45|e46|56|e6|e|",
    "ee12|e23|e4|445|6|666||",
    "e112|23|e4|e45|e6|666||",
    "e123|e23|e4|e5|566|66||",
    "ee12|334|455|e4|6|66|e|",
    "e112|23|34|e5|e66|e66||",
    "ee12|e34|356|55|566||e|",
    "e123|e24|e5|456|56|6|e|",
    "ee12|233|34|5|e56|66|e|",
    "ee12|223|4|445|6|e66|e|",
    "ee12|233|45|46|e5|66|e|",
    "ee12|e34|e56|556|566|||",
    "e112|e3|e45|456|e6|66||",
    "ee12|233|44|e5|e6|666||",
    "e112|34|e35|46|e5|66|e|",
    "ee12|e33|345|4|56|66|e|",
    "ee12|234|56|e45|66|e6||",
    "ee12|e33|445|56|56|6|e|",
    "ee12|e34|355|e5|666|6||",
    "e112|34|355|e6|e66|e6||",
    "e123|e45|e45|466|6|e6||",
    "ee12|e34|355|e6|566|6||",
    "e112|e3|e45|466|55|6|e|",
    "ee12|e34|345|e6|56|66||",
    "ee12|345|345|e4|6|66|e|",
    "e123|e24|35|56|e56|6|e|",
    "ee12|334|356|5|566|e|e|",
    "ee12|e23|45|e45|66|66||",
    "ee12|345|346|44||e66|e|",
    "e112|34|e35|56|e56|6|e|",
    "ee12|233|44|55|66|e6|e|",
    "ee12|ee3|334|5|566|66||",
    "e112|e3|e44|556|56|6|e|",
    "e112|e3|445|456|e|66|e|",
    "ee12|333|445|5|66|e6|e|",
    "ee12|e23|e4|456|56|66||",
    "e112|34|356|e4|56|e6|e|",
    "e112|34|e56|e55|e66|6||",
    "e123|e45|e45|456|6|6|e|",
    "ee12|e34|556|445|6|6|e|",
    "e112|34|e35|e4|e6|666||",
    "ee12|334|356|5|e56|6|e|",
    "ee12|234|35|e4|e6|666||",
    "ee12|e34|355|66|556||e|",
    "e112|23|e4|e45|66|e66||",
    "ee12|234|34|e5|66|e66||",
    "e112|e3|e44|555|66|6|e|",
    "ee12|234|56|e55|666|e||",
    "e112|33|e45|e6|e56|66||",
    "ee12|334|344|5|6|e66|e|",
    "ee12|233|34|5|e66|e66||",
    "e112|e3|e45|e45|66|66||",
    "ee12|e34|355|56|e66|6||",
    "ee12|334|455|56|e6|6|e|",
    "e123|e24|34|e5|e6|666||",
    "ee12|223|4|e55|566|6|e|",
    "ee12|e23|45|445|6|66|e|",
    "e112|e3|e45|466|e5|66||",
    "ee12|334|455|e5|66|6|e|",
    "ee12|234|35|45|56|6|ee|",
    "ee12|e34|556|455|66||e|",
    "e112|34|e55|e45|66|6|e|",
    "ee12|e34|355|e4|66|66||",
    "ee12|e33|445|66|55|6|e|",
    "e112|33|e45|45|e6|66|e|",
    "e112|e3|e34|45|66|e66||",
    "ee12|e23|34|45|e6|666||",
    "ee12|233|45|46|ee|666||",
    "ee12|223|4|e45|66|e66||",
    "ee12|234|56|e45|e6|66||",
    "ee12|345|346|56|56|e|e|",
    "ee12|e34|345|55|66|6|e|",
    "ee12|333|445|6|e5|66|e|",
    "ee12|e33|445|55|66|6|e|",
    "ee12|234|35|66|e56|e6||",
    "ee12|e23|34|55|e66|66||",
    "ee12|e23|45|466|55|6|e|",
    "e112|33|e45|e6|556|6|e|",
    "ee12|234|56|ee4|56|66||",
    "e123|e24|56|456|56|e|e|",
    "e112|e3|344|56|56|e6|e|",
    "ee12|e34|356|e4|56|66||",
    "ee12|ee3|444|556|6|66||",
    "ee12|e34|e35|46|56|66||",
    "ee12|334|456|45|e|66|e|",
    "e112|e3|344|55|e6|66|e|",
    "ee12|223|4|556|556||ee|",
    "e112|23|e4|456|e5|66|e|",
    "e112|34|355|e6|e56|6|e|",
    "ee12|233|45|66|ee5|66||",
    "e112|e3|445|566|e5|6|e|",
    "e123|e24|56|e45|56|6|e|",
    "ee12|334|456|56|e5|6|e|"
]

if __name__ == "__main__":
    main()
