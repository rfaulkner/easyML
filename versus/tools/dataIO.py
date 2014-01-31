"""
Class family for Data IO classes to handle data ingestion and fetch events
"""

import redis


class DataIO(object):

    def __init__(self, **kwargs):
        pass

    def write(self, **kwargs):
        raise NotImplementedError()

    def read(self, **kwargs):
        raise NotImplementedError()


class DataIOHDFS(DataIO):
    """ Class implementing data IO for HDFS. """

    def __init__(self, **kwargs):
        super(DataIOHDFS, self).__init__(**kwargs)

    def write(self, **kwargs):
        pass

    def read(self, **kwargs):
        pass


class DataIORedis(DataIO):
    """ Class implementing data IO for Redis. """

    def __init__(self, **kwargs):
        super(DataIORedis, self).__init__(**kwargs)

    def write(self, **kwargs):
        pass

    def read(self, **kwargs):
        pass