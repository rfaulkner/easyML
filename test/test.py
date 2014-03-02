# -*- coding: utf-8 -*-

"""
dynamic_learn.testsuite
~~~~~~~~~~~~~~~~~~~~~~~

:license: BSD, see LICENSE for more details.
"""

import unittest
import theano.tensor as T
import tempfile
import os

from versus.src.logistic import LogisticRegression
from versus.tools.dataIO import DataIORedis, DataIOHDFS

BATCH_SIZE = 50


class LocalTestCase(unittest.TestCase):
    """
    Setup relevant test context in this class

    """
    def setUp(self):
        unittest.TestCase.setUp(self)


class TestLogistic(LocalTestCase):
    """ Test cases for Logistic model """

    def test_init(self):

        # allocate symbolic variables for the data
        x = T.fmatrix()  # the data is presented as rasterized images (each being a 1-D row vector in x)

        # construct the logistic regression class
        try:
            LogisticRegression(_input=x.reshape((BATCH_SIZE , 28 * 28)), n_in=28 * 28, n_out=10)
        except Exception:
            assert False

        assert True

    def test_negative_log_likelihood(self):

        # allocate symbolic variables for the data
        x = T.fmatrix()  # the data is presented as rasterized images (each being a 1-D row vector in x)
        y = T.lvector()  # the labels are presented as 1D vector of [long int] labels

        # construct the logistic regression class
        try:
            classifier = LogisticRegression(x.reshape((BATCH_SIZE , 28 * 28)), 28 * 28, 10)
            cost = classifier.negative_log_likelihood(y)
        except Exception:
            assert False

        assert cost == 0


class TestRedis(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_init(self):
        dior = DataIORedis()
        dior.connect()  # connect to local instance

        del dior
        assert True

    def test_simple(self):
        dior = DataIORedis()
        dior.connect()  # connect to local instance

        if not dior.write(key='try', value=1):
            assert False

        if not (dior.read(key='try') == 1):
            assert False

        del dior
        assert True


class TestDataIOHDFS(LocalTestCase):
    """ Test cases for HDFS IO """

    def test_copy_from_local(self):

        tempdir = tempfile.mkdtemp()
        handle, fullpath = tempfile.mkstemp(dir=tempdir)
        hdfs_path = '/user/test'

        io = DataIOHDFS()
        io.copy_from_local(fullpath, hdfs_path)
        filename = os.path.basename(fullpath)

        exists_in_hdfs = False
        for item in io.list(hdfs_path):
            if str(item) == filename:
                exists_in_hdfs = True
        self.assertTrue(exists_in_hdfs)

    def test_copy_to_local(self):
        assert False

    def test_list(self):
        assert False
