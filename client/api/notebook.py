"""
Backwards compatibility shim for old okpy API
"""
import os
from glob import glob
import inspect
import statistics
from okgrade.parser import parse_ok_test
from scoraptor.runner import TestBundle

def _all_pass_score_reduce_func(scores):
    if all([s == 1.0 for s in scores]):
        return 1
    return 0

class Notebook:
    def __init__(self, okfile):
        """
        okfile is path to .ok file.

        This implementation does not read the .ok files.
        However, their path is used as basedir when looking
        for tests.
        """
        self.basedir = os.path.dirname(os.path.abspath(okfile))

    def _display(self, *objs):
        """
        Display *objs if running in IPython
        """
        try:
            __IPYTHON__
            # We are in a Notebook / IPython! Let's display output
            from IPython.display import display
            display(*objs)
        except NameError:
            pass

    def auth(self, inline=False):
        """
        Legacy interface for authenticating to an okpy server.

        Not supported, so we ignore for now.
        """
        # FIXME: A warning here?
        pass

    def submit(self):
        """
        Legacy interface for submitting a notebook to okpy server.

        Not supported, so we ignore for now.
        """
        # FIXME: A warning here?
        pass

    def grade_glob(self, question_glob, global_env=None):
        test_files = glob(question_glob)
        tests = []
        for tf in test_files:
            # In each file, all tests must pass to get a score!
            tests.append(TestBundle(parse_ok_test(tf), score_reduce_func=_all_pass_score_reduce_func))
        # Across all files, total score is mean of all scores.
        # Also we don't want to stop when one test fails
        test_bundle = TestBundle(tests, stop_on_fail=False, score_reduce_func=statistics.mean)
        if global_env is None:
            # Get the global env of our callers - one level below us in the stack
            # The grade method should only be called directly from user / notebook
            # code. If some other method is calling it, it should also use the
            # inspect trick to pass in its parents' global env.
            global_env = inspect.currentframe().f_back.f_globals
        return test_bundle(global_env)


    def grade(self, question, global_env=None):
        path = os.path.join(self.basedir, "tests", "{}.py".format(question))

        tests = TestBundle(parse_ok_test(path), score_reduce_func=_all_pass_score_reduce_func)
        if global_env is None:
            # Get the global env of our callers - one level below us in the stack
            # The grade method should only be called directly from user / notebook
            # code. If some other method is calling it, it should also use the
            # inspect trick to pass in its parents' global env.
            global_env = inspect.currentframe().f_back.f_globals
        result = tests(global_env)
        return result