#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import inspect
from collections import namedtuple

"""
test-my-module

    def hi():
        return "hello"

    def test():
        assert hi() == "hello"

    if __name__ == "__main__":
        import test_my_module
        test_my_module.run_all_tests()
"""

TestResults = namedtuple("TestResults", "passed_tests total_tests")


def run_all_tests():
    """
    Runs all tests in the module that called it.
    """

    # figure out who called us
    caller = inspect.currentframe().f_back
    try:
        # What does the namespace look like?
        namespace = caller.f_globals
    finally:
        del caller

    test_cases = collect_tests(namespace)
    run_collected_test_cases(test_cases)


def run_collected_test_cases(test_cases):
    """
    Calls the test cases in order.
    """
    num_tests = 0
    passed_tests = 0

    for name, test_function in test_cases:
        num_tests += 1
        test_function()
        passed_tests += 1

    return TestResults(passed_tests=passed_tests, total_tests=num_tests)


def collect_tests(global_object):
    """
    Yield possible test functions: (name, callable) pairs.
    """

    for name in global_object:
        if not name.startswith("test"):
            continue

        fn = global_object[name]

        if callable(fn):
            yield name, fn
