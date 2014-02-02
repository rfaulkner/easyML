"""
Class family for Model IO classes to handle read/write of learning models
"""

from versus.config import log
from versus.tools.dataIO import DataIORedis
import cPickle

from hashlib import sha1


class ModelIO(object):

    def __init__(self, model, **kwargs):
        self._model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    def write(self):
        raise NotImplementedError()

    def is_valid(self):
        """ Ensures that the model is valid. """
        raise NotImplementedError()

    def genkey(self):
        """ Generates a key from the model. Presumes model is valid. """
        return sha1(str(self._model).encode('utf-8')).hexdigest()

    def package(self):
        """ Prepares the model for writing. Pickle seriallization"""
        return cPickle.dumps(self._model)


class ModelIORedis(ModelIO):
    """ Performs IO to redis. """

    def __init__(self, model, **kwargs):
        super(ModelIORedis, self).__init__(model, **kwargs)

    def is_valid(self):
        # TODO - test to ensure model is "pickle-able"
        return True

    def write(self):
        """
        Write a model to redis
        """

        dio_r = DataIORedis()
        dio_r.connect()

        # Write the
        if self.is_valid():
            return dio_r.write(key=self.genkey(),
                value=self.package())
        else:
            log.error('Invalid model -> "{0}"'.format(str(self._model)))
            return False

    def read(self, hash):
        pass