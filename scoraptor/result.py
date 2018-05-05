import html


class TestResult:
    def __init__(self, score, summary_mimebundle):
        """
        Result of running a Test of some kind.

        score - float, the score this test produced.
        summary_mimebundle - dict | string, mapping mimetypes to summaries.
                             If string is passed in, assume it is for mimetype 
                             text/plain.
        """
        self.score = score
        if isinstance(summary_mimebundle, str):
            self.summary_mimebundle = {'text/plain': summary_mimebundle}
        else:
            if 'text/plain' not in summary_mimebundle:
                raise ValueError('summary_mimebundle must contain text/plain')
            self.summary_mimebundle = summary_mimebundle

    def get_summary(self, mimetype='text/plain'):
        """
        Return summary for this TestResult.

        If mimetype is not passed in, 'text/plain' is assumed
        """
        return self.summary_mimebundle[mimetype]

    def _repr_html_(self):
        """
        Return HTML representation of this Test Result.

        Used by IPython to display pretty results
        """
        if 'text/html' in self.summary_mimebundle:
            return self.get_summary('text/html')
        else:
            return '<strong>Score: ' + html.escape(str(self.score)) + '</strong>' + \
                   '<pre>' + html.escape(self.get_summary('text/plain')) + '</pre>'

    def __eq__(self, other):
        if not isinstance(other, TestResult):
            raise ValueError('Can not compare TestResult object with object of type {}'.format(type(other)))

        return other.score == self.score and other.summary_mimebundle == self.summary_mimebundle