# -*- coding: utf-8 -*-

"""
dynamic_learn.testsuite
~~~~~~~~~~~~~~~~~~~~~~~

:license: BSD, see LICENSE for more details.
"""

import unittest
import theano.tensor as T

from versus.src.logistic import LogisticRegression

BATCH_SIZE = 50


class LocalTestCase(unittest.TestCase):
    """
    Setup relevant test context in this class
    """
    def setUp(self):
        # TODO - add setup for Logistic related testing
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