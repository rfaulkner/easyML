"""
Class family for Model IO classes to handle read/write of learning models
"""

import redis


class ModelIO(object):

    def __init__(self, **kwargs):
        pass

    def write(self, model):
        raise NotImplementedError()

    def validate(self, model):
        """ Ensures that the model is valid. """
        pass

    def genkey(self, model):
        """ Generates a key from the model. Presumes model is valid. """
        return str(model)

    def package(self, model):
        """ Prepares the model for writing. """
        return model


class ModelIORedis(ModelIO):
    """ Performs IO to redis. """

    def __init__(self, **kwargs):
        super(ModelIORedis, self).__init__(**kwargs)

    def write(self, model):

        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)

        r.set(self.genkey(model), self.package(model))