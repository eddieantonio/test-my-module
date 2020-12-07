#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import inspect


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


def run_all_tests():
    """
    Runs all tests in the module that called it.
    """

    # figure out who called us
    caller = inspect.currentframe().f_back
    try:
        namespace = caller.f_globals
    finally:
        del caller

    test_cases = collect_tests(namespace)
    print(list(test_cases))


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
