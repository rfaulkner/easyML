# -*- coding: utf-8 -*-

"""
dynamic_learn.testsuite
~~~~~~~~~~~~~~~~~~~~~~~

:license: BSD, see LICENSE for more details.
"""

import unittest
import tempfile
import os

from versus.tools.dataIO import DataIOHDFS


class LocalTestCase(unittest.TestCase):
    """
    Setup relevant test context in this class
    """
    def setUp(self):
        # TODO - add setup for HDFSIO related testing
        unittest.TestCase.setUp(self)


class TestDataIOHDFS(LocalTestCase):
    """ Test cases for HDFS IO """

    def test_copy_from_local(self):

        io = DataIOHDFS()

        # Create a file on HDFS
        tempdir = tempfile.mkdtemp()
        handle, fullpath = tempfile.mkstemp(dir=tempdir)
        hdfs_path = '/user/test'
        io.copy_from_local(fullpath, hdfs_path)
        filename = os.path.basename(fullpath)

        # Check the hdfs path
        exists_in_hdfs = False
        for item in io.list(hdfs_path):
            if str(item) == filename:
                exists_in_hdfs = True
        self.assertTrue(exists_in_hdfs)

    def test_copy_to_local(self):

        io = DataIOHDFS()

        # Create a file on HDFS
        tempdir = tempfile.mkdtemp()
        handle, fullpath = tempfile.mkstemp(dir=tempdir)
        hdfs_path = '/user/test'
        io.copy_from_local(fullpath, hdfs_path)

        # Copy back to the filesystem
        tempdir = tempfile.mkdtemp()
        handle, fullpath = tempfile.mkstemp(dir=tempdir)
        io.copy_to_local(fullpath, hdfs_path)

        self.assertTrue(os.path.exists(fullpath))


    def test_list(self):

        io = DataIOHDFS()
        hdfs_path = '/user/test'

        tempdir = tempfile.mkdtemp()
        handle1, fullpath1 = tempfile.mkstemp(dir=tempdir)
        handle2, fullpath2 = tempfile.mkstemp(dir=tempdir)

        io.copy_to_local(fullpath1, hdfs_path)
        io.copy_to_local(fullpath2, hdfs_path)

        for i in io.list(hdfs_path):
            self.assertTrue(i[6] == fullpath2 or i[6] == fullpath1)
