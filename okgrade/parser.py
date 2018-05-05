from scoraptor.doctest import SingleDocTest

def parse_ok_test(path):
    """
    Parse a ok test file & return list of SingleDocTests.
    """
    # ok test files are python files, with a global 'test' defined
    test_globals = {}
    with open(path) as f:
        exec(f.read(), test_globals)
    
    test_spec = test_globals['test']

    # We only support a subset of these tests, so let's validate!

    # Make sure there is a name
    assert 'name' in test_spec

    # Do not support multiple suites in the same file
    assert len(test_spec['suites']) == 1

    # Do not support point values other than 1
    assert test_spec['points'] == 1

    test_suite = test_spec['suites'][0]

    # Only support doctest. I am unsure if other tests are implemented
    assert test_suite['type'] == 'doctest'

    # Not setup and teardown supported
    assert not bool(test_suite.get('setup'))
    assert not bool(test_suite.get('teardown'))

    tests = []

    for i, test_case in enumerate(test_spec['suites'][0]['cases']):
        tests.append(SingleDocTest(
            test_spec['name'] + ' ' + str(i + 1),
            test_case['code']
        ))

    return tests