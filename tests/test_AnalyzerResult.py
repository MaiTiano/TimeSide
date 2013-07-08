#! /usr/bin/env python

from unit_timeside import *
from timeside.analyzer.core import *
from numpy import ones, array
from math import pi

verbose = 0

class TestAnalyzerResult(TestCase):
    """ test AnalyzerResult """

    def setUp(self):
        self.result = AnalyzerResult(id = "foo_bar", name = "Foo bar", unit = "foo")

    def testOnFloat(self):
        "float result"
        self.result.value = 1.2

    def testOnInt(self):
        "integer result"
        self.result.value = 1

    def testOnList(self):
        "list result"
        self.result.value = [1., 2.]

    def testOnString(self):
        "string result"
        self.result.value = "hello"

    def testOnListOfString(self):
        "list of strings result"
        self.result.value = ["hello", "hola"]

    def testOnListOfList(self):
        "list of lists result"
        self.result.value = [[0,1], [0,1,2]]

    def testOnNumpyVectorOfFloat(self):
        "numpy vector of float"
        self.result.value = ones(2, dtype = 'float') * pi

    def testOnNumpy2DArrayOfFloat64(self):
        "numpy 2d array of float64"
        self.result.value = ones([2,3], dtype = 'float64') * pi

    def testOnNumpy3DArrayOfInt32(self):
        "numpy 3d array of int32"
        self.result.value = ones([2,3,2], dtype = 'int32') * pi

    def testOnNumpyArrayOfStrings(self):
        "numpy array of strings"
        self.result.value = array(['hello', 'hola'])

    def testOnEmptyList(self):
        "empty list"
        self.result.value = []

    def testOnNone(self):
        "None"
        self.result.value = None

    def testOnUnicode(self):
        "None"
        self.result.value = None

    def tearDown(self):
        pass

good_numpy_data_types = [
    'float64',
    'float32',
#    'float16',
    'int64',
    'int16',
    'int32',
    'int8',
    'uint16',
    'uint32',
    'uint64',
    'uint8',
]

bad_numpy_data_types = [
    # not understood by json or yaml
    'float128',
    # complex can not be serialized in json
    'complex256',
    'complex128',
    'complex64',
    # ?
    'datetime64',
    'timedelta64',
    ]

def create_good_method_func (numpy_data_type):
    def method(self):
        "numpy %s" % numpy_data_type
        import numpy
        self.result.value = getattr(numpy, numpy_data_type)(pi)
    return method

def create_bad_method_func (numpy_data_type):
    def method(self):
        "numpy %s" % numpy_data_type
        import numpy
        try:
            value = getattr(numpy, numpy_data_type)(pi)
        except ValueError:
            value = getattr(numpy, numpy_data_type)()
        self.assertRaises(TypeError, self.result.__setattr__, 'value', value)
    return method

for numpy_data_type in good_numpy_data_types:
    test_method = create_good_method_func (numpy_data_type)
    test_method.__name__ = 'testOnNumpy_%s' % numpy_data_type
    test_method.__doc__ = 'groks a numpy %s' % numpy_data_type
    setattr (TestAnalyzerResult, test_method.__name__, test_method)

for numpy_data_type in bad_numpy_data_types:
    test_method = create_bad_method_func (numpy_data_type)
    test_method.__name__ = 'testOnNumpy_%s' % numpy_data_type
    test_method.__doc__ = 'gasps on numpy %s' % numpy_data_type
    setattr (TestAnalyzerResult, test_method.__name__, test_method)

class TestAnalyzerResultNumpy(TestAnalyzerResult):
    """ test AnalyzerResult numpy serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_numpy = results.to_numpy('/tmp/t.npy')
        d_numpy = results.from_numpy('/tmp/t.npy')
        if verbose:
            print '%15s' % 'from numpy:',
            print d_numpy
        for i in range(len(d_numpy)):
            self.assertEquals(d_numpy[i], results[i])

class TestAnalyzerResultHdf5(TestAnalyzerResult):
    """ test AnalyzerResult hdf5 serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        results.to_hdf5('/tmp/t.h5')
        res_hdf5 = results.from_hdf5('/tmp/t.h5')
        if verbose:
            print '%15s' % 'from hdf5:',
            print res_hdf5
        self.assertEquals(res_hdf5, results)

class TestAnalyzerResultYaml(TestAnalyzerResult):
    """ test AnalyzerResult yaml serialize """
    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_yaml = results.to_yaml()
        if verbose:
            print 'to yaml:'
            print r_yaml
        d_yaml = results.from_yaml(r_yaml)
        if verbose:
            print '%15s' % 'from yaml:',
            print d_yaml
        for i in range(len(d_yaml)):
            self.assertEquals(results[i], d_yaml[i])

class TestAnalyzerResultXml(TestAnalyzerResult):
    """ test AnalyzerResult xml serialize """
    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_xml = results.to_xml()
        if verbose:
            print 'to xml:'
            print r_xml

        d_xml = results.from_xml(r_xml)
        if verbose:
            print '%15s' % 'from xml:',
            print d_xml

        for i in range(len(d_xml)):
            self.assertEquals(d_xml[i], results[i])

class TestAnalyzerResultJson(TestAnalyzerResult):
    """ test AnalyzerResult json serialize """
    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_json = results.to_json()
        if verbose:
            print 'to json:'
            print r_json

        d_json = results.from_json(r_json)
        if verbose:
            print d_json
            print '%15s' % 'from yaml:',

        for i in range(len(d_json)):
            self.assertEquals(d_json[i], results[i])

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())