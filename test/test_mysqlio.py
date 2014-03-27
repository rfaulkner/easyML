# -*- coding: utf-8 -*-

"""
dynamic_learn.testsuite
~~~~~~~~~~~~~~~~~~~~~~~

:license: BSD, see LICENSE for more details.
"""

import unittest

import versus.tools.dataIO as dio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class LocalTestCase(unittest.TestCase):
    """
    Setup relevant test context in this class
    """
    def setUp(self):
        # TODO - add setup for MySQLIO related testing
        unittest.TestCase.setUp(self)


class TestMySQLConnect(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_simple(self):
        raise NotImplementedError()


class TestMySQLCreateTable(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_simple(self):
        mysql_inst = dio.DataIOMySQL()
        mysql_inst.connect_lite()
        self.assertTrue(mysql_inst.create_table('User'))


class TestMySQLInsert(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_simple(self):
        mysql_inst = dio.DataIOMySQL()
        mysql_inst.connect_lite()
        mysql_inst.create_table('User')

        self.assertTrue(mysql_inst.insert('User',
                                          id=1,
                                          name='me',
                                          fullname='me',
                                          password='pass',
                                          date_join=0))


class TestMySQLFetchRows(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_simple(self):
        mysql_inst = dio.DataIOMySQL()
        mysql_inst.connect_lite()
        mysql_inst.create_table('User')
        mysql_inst.insert('User', id=1, name='me', fullname='me',
                          password='pass', date_join=0)

        self.assertTrue(len(mysql_inst.fetch_all_rows('User')) > 0)


class TestMySQLDelete(LocalTestCase):
    """ Test cases for Redis read/writes """

    def test_simple(self):
        mysql_inst = dio.DataIOMySQL()
        mysql_inst.connect_lite()
        mysql_inst.create_table('User')

        for row in mysql_inst.fetch_all_rows('User'):
            mysql_inst.delete(row)
