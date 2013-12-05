"""
Class family for Data IO classes to handle data ingestion and fetch events
"""

class DataIO(object):

    def __init__(self, **kwargs):
        pass

    def write(self):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()


class DataIOHDFS(DataIO):
    """ Class for instrumenting data IO for HDFS. """

    def __init__(self, **kwargs):
        super(DataIOHDFS, self).__init__(**kwargs)

    def write(self):
        pass

    def read(self):
        pass