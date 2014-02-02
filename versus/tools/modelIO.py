"""
Class family for Model IO classes to handle read/write of learning models
"""

from versus.config import log
from versus.tools.dataIO import DataIORedis
import cPickle

from hashlib import sha1


class ModelIO(object):

    def __init__(self, **kwargs):
        pass

    def write(self, model):
        raise NotImplementedError()

    def is_valid(self, model):
        """ Ensures that the model is valid. """
        pass

    def genkey(self, model):
        """ Generates a key from the model. Presumes model is valid. """
        return sha1(str(model).encode('utf-8')).hexdigest()

    def package(self, model):
        """ Prepares the model for writing. """
        return model


class ModelIORedis(ModelIO):
    """ Performs IO to redis. """

    def __init__(self, **kwargs):
        super(ModelIORedis, self).__init__(**kwargs)

    def package(self, model):
        """ Prepares the model for writing. Pickle seriallization"""
        return cPickle.dumps(model)

    def write(self, model):
        """
        Write a model to redis
        """

        dio_r = DataIORedis()
        dio_r.connect()

        # Write the
        if is_valid(model):
            return dio_r.write(key=self.genkey(model),
                value=self.package(model))
        else:
            log.error('Invalid model -> "{0}"'.format(str(model)))
            return False

    def read(self, hash):
        pass