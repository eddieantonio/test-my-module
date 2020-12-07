#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import inspect
import sys
import traceback
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


class TestResults(namedtuple("BaseTestResults", "passed_tests total_tests")):
    @property
    def failed_tests(self):
        return self.total_tests - self.passed_tests


def run_all_tests():
    """
    Runs all tests in the module that called it.

    Prints dumb emoji to make you feel bad.
    """

    # figure out who called us
    caller = inspect.currentframe().f_back
    try:
        # What does the namespace look like?
        namespace = caller.f_globals
    finally:
        del caller

    test_cases = collect_tests(namespace)
    results = run_collected_test_cases(test_cases)

    print("ran", results.total_tests, "tests")

    if results.failed_tests > 0:
        print("💥💥💥", results.failed_tests, "failed 💔💔💔")
    else:
        print("✨ all tests passed ✨ ☠️☠️☠️")


def run_collected_test_cases(test_cases):
    """
    Calls the test cases in order.
    """
    num_tests = 0
    passed_tests = 0

    for name, test_function in test_cases:
        num_tests += 1
        try:
            test_function()
        except AssertionError:
            _exc_type, _exc_value, exc_traceback = sys.exc_info()

            try:
                crashed_frame = exc_traceback.tb_next.tb_frame
                locals_ = crashed_frame.f_locals
            finally:
                del crashed_frame
            crashed_stack = traceback.extract_tb(exc_traceback)
            assertion_failure = crashed_stack[-1]

            filename = assertion_failure.filename

            # TODO: parse the line, get its AST, figure out
            # TODO: what names are being used,
            # TODO: then just print THOSE names
            line = assertion_failure.line
            lineno = assertion_failure.lineno

            print("failed at", filename, end=", ")
            print("line", lineno)
            print(line)

            print("where:")
            for name, value in locals_.items():
                print("   ", name, "=", repr(value))
        else:
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
