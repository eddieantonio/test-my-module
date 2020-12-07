#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from unittest.mock import Mock

import test_my_module


def test_collect_tests_from_dict():
    """
    if you give collect_tests() a dictionary produced by globals() or the frame object
    globals, it should return all of the test cases.
    """

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


def test_run_tests_collected_tests():
    """
    Check that our test runner ACTUALLY calls our tests.
    """
    mock = Mock()

    fake_test_cases = [("test_mock", mock)]
    results = test_my_module.run_collected_test_cases(fake_test_cases)

    assert mock.called, "our test was not called"

    assert results.passed_tests == 1
    assert results.total_tests == 1
