"""
Module for learning source.
"""

import theano.tensor as T
import numpy

def logistic(x):
    return 1 / (1 + T.exp(-x))
