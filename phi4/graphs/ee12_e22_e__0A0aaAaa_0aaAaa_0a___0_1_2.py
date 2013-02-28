#!/usr/bin/python
# -*- coding:utf8

from dynamics import diff1, diff2

graphName = "ee12-e22-e-:0A0aaAaa-0aaAaa-0a-:"

tVersion = (0, 1, 2)

sectors = [
    ([(3, [100, 101, 6]), (101, [6])], (diff1('a0'),)),
    ([(3, [100, 101, 6]), (6, [101])], (diff1('a0'),)),
    ([(100, [3, 101, 6]), (101, [6])], (diff1('a0'),)),
    ([(100, [3, 101, 6]), (6, [101])], (diff1('a0'),)),
    ([(6, [3, 100, 101]), (3, [100, 101])], ()),
    ([(6, [3, 100, 101]), (100, [3, 101])], ()),
    ([(6, [3, 100, 101]), (101, [3, 100])], ()),
    ([(101, [3, 100, 6])], ()),

]

# sectors = [
#     [(3, (6, 100, 101)), (6, (100, 101))],
#     [(3, (6, 100, 101)), (100, (6, 101))],
#     [(3, (6, 100, 101)), (101, (6, 100))],
#     [(6, (3, 100, 101)), (3, (100, 101))],
#     [(6, (3, 100, 101)), (100, (3, 101))],
#     [(6, (3, 100, 101)), (101, (3, 100))],
#     [(100, (3, 6, 101)), (3, (6, 101))],
#     [(100, (3, 6, 101)), (6, (3, 101))],
#     [(100, (3, 6, 101)), (101, (3, 6))],
#     [(101, (3,  6, 100)) ],
# ]
