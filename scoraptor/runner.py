"""
Convenience functions to run a series of tests against same environment.
"""
from scoraptor.result import TestResult
from statistics import mean

class TestBundle:
    def __init__(self, tests, stop_on_fail=True, score_reduce_func=mean):
        self.tests = tests
        self.stop_on_fail = stop_on_fail
        self.score_reduce_func = score_reduce_func

    def reduce_results(self, results):
        new_score = self.reduce_scores(results)
        new_summary = self.reduce_summaries(results)
        return TestResult(new_score, new_summary)

    def reduce_summaries(self, results):
        # FIXME: UGH
        summary = {}
        for r in results:
            for mime, value in r.summary_mimebundle.items():
                if mime in summary:
                    summary[mime] += '\n' + value
                else:
                    summary[mime] = value

        return summary

    def reduce_scores(self, results):
        scores = [r.score for r in results]
        if len(results) < len(self.tests):
            # Not all tests were run, so we extend length of scores list
            scores += [0 for _ in range(len(self.tests) - len(self.tests))]
        
        return self.score_reduce_func(scores)

    def __call__(self, global_environment):
        results = []
        for t in self.tests:
            result = t(global_environment)
            results.append(result)

            if self.stop_on_fail and result.score == 0:
                break

        return self.reduce_results(results)