# -*- coding: utf-8 -*-

"""
dynamic_learn.testsuite
~~~~~~~~~~~~~~~~~~~~~~~

:license: BSD, see LICENSE for more details.
"""

import unittest

from versus.tools.dataIO import DataIORedis


class LocalTestCase(unittest.TestCase):
    """
    Setup relevant test context in this class
    """
    def setUp(self):
        # TODO - add setup for RedissIO related testing
        unittest.TestCase.setUp(self)


class TestRedis(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_init(self):
        dior = DataIORedis()
        dior.connect()  # connect to local instance

        del dior

    def test_simple(self):
        dior = DataIORedis()
        dior.connect()  # connect to local instance

        self.assertTrue(dior.write(key='try', value=1))
        self.assertTrue(dior.read(key='try') == 1)

        del dior
