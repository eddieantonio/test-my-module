#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import test_my_module


def test_collect_tests_from_dict():
    def inc(x):
        return x + 1

    def test_answer():
        assert inc(3) == 5

    def test():
        assert 2 + 2 == 4
        assert 4 - 1 == 3, "quick maths"

    global_object = {
        "test": test,
        "inc": inc,
        "test_answer": test_answer,
    }

    all_tests = list(test_my_module.collect_tests(global_object))
    assert len(all_tests) == 2
    for name, fn in all_tests:
        assert name.startswith("test")
        assert callable(fn)
