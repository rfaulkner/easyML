"""
Implements an RBM.
"""

import numpy
import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams


class RBM(object):
    """Restricted Boltzmann Machine (RBM) """

    def __init__(self,
                 _input=None,
                 n_visible=784,
                 n_hidden=500,
                 W=None,
                 hbias=None,
                 vbias=None,
                 numpy_rng=None,
                 theano_rng=None):
        """
        RBM constructor. Defines the parameters of the model along with
        basic operations for inferring hidden from visible (and vice-versa),
        as well as for performing CD updates.

        :param input: None for standalone RBMs or symbolic variable if RBM is
        part of a larger graph.

        :param n_visible: number of visible units

        :param n_hidden: number of hidden units

        :param W: None for standalone RBMs or symbolic variable pointing to a
        shared weight matrix in case RBM is part of a DBN network; in a DBN,
        the weights are shared between RBMs and layers of a MLP

        :param hbias: None for standalone RBMs or symbolic variable pointing
        to a shared hidden units bias vector in case RBM is part of a
        different network

        :param vbias: None for standalone RBMs or a symbolic variable
        pointing to a shared visible units bias
        """

        self.n_visible = n_visible
        self.n_hidden = n_hidden


        if numpy_rng is None:
          # create a number generator
          numpy_rng = numpy.random.RandomState(1234)

        if theano_rng is None:
          theano_rng = RandomStreams(numpy_rng.randint(2 ** 30))

        if W is None :
         # W is initialized with `initial_W` which is uniformely sampled
         # from -4.*sqrt(6./(n_visible+n_hidden)) and 4.*sqrt(6./(n_hidden+n_visible))
         # the output of uniform if converted using asarray to dtype
         # theano.config.floatX so that the code is runable on GPU
         initial_W = numpy.asarray(numpy.random.uniform(
                   low=-4 * numpy.sqrt(6. / (n_hidden + n_visible)),
                   high=4 * numpy.sqrt(6. / (n_hidden + n_visible)),
                   size=(n_visible, n_hidden)),
                   dtype=theano.config.floatX)
         # theano shared variables for weights and biases
         W = theano.shared(value=initial_W, name='W')

        if hbias is None :
         # create shared variable for hidden units bias
         hbias = theano.shared(value=numpy.zeros(n_hidden,
                             dtype=theano.config.floatX), name='hbias')

        if vbias is None :
          # create shared variable for visible units bias
          vbias = theano.shared(value =numpy.zeros(n_visible,
                              dtype = theano.config.floatX),name='vbias')


        # initialize input layer for standalone RBM or layer0 of DBN
        self.input = input if input else T.dmatrix('input')

        self.W = W
        self.hbias = hbias
        self.vbias = vbias
        self.theano_rng = theano_rng
        # **** WARNING: It is not a good idea to put things in this list
        # other than shared variables created in this function.
        self.params = [self.W, self.hbias, self.vbias]

    def propup(self, vis):
        ''' This function propagates the visible units activation upwards to
        the hidden units

        Note that we return also the pre_sigmoid_activation of the layer. As
        it will turn out later, due to how Theano deals with optimization and
        stability this symbolic variable will be needed to write down a more
        stable graph (see details in the reconstruction cost function)
        '''
        pre_sigmoid_activation = T.dot(vis, self.W) + self.hbias
        return [pre_sigmoid_activation, T.nnet.sigmoid(pre_sigmoid_activation)]

    def sample_h_given_v(self, v0_sample):
        ''' This function infers state of hidden units given visible units '''
        # compute the activation of the hidden units given a sample of the visibles
        pre_sigmoid_h1, h1_mean = self.propup(v0_sample)
        # get a sample of the hiddens given their activation
        # Note that theano_rng.binomial returns a symbolic sample of dtype
        # int64 by default. If we want to keep our computations in floatX
        # for the GPU we need to specify to return the dtype floatX
        h1_sample = self.theano_rng.binomial(size=h1_mean.shape, n=1, p=h1_mean,
                                             dtype=theano.config.floatX)
        return [pre_sigmoid_h1, h1_mean, h1_sample]

    def propdown(self, hid):
        '''This function propagates the hidden units activation downwards to
        the visible units

        Note that we return also the pre_sigmoid_activation of the layer. As
        it will turn out later, due to how Theano deals with optimization and
        stability this symbolic variable will be needed to write down a more
        stable graph (see details in the reconstruction cost function)
        '''
        pre_sigmoid_activation = T.dot(hid, self.W.T) + self.vbias
        return [pre_sigmoid_activation, T.nnet.sigmoid(pre_sigmoid_activation)]

    def sample_v_given_h(self, h0_sample):
        ''' This function infers state of visible units given hidden units '''
        # compute the activation of the visible given the hidden sample
        pre_sigmoid_v1, v1_mean = self.propdown(h0_sample)
        # get a sample of the visible given their activation
        # Note that theano_rng.binomial returns a symbolic sample of dtype
        # int64 by default. If we want to keep our computations in floatX
        # for the GPU we need to specify to return the dtype floatX
        v1_sample = self.theano_rng.binomial(size=v1_mean.shape,n=1, p=v1_mean,
                                             dtype=theano.config.floatX)
        return [pre_sigmoid_v1, v1_mean, v1_sample]

    def gibbs_hvh(self, h0_sample):
        ''' This function implements one step of Gibbs sampling,
            starting from the hidden state'''
        pre_sigmoid_v1, v1_mean, v1_sample = self.sample_v_given_h(h0_sample)
        pre_sigmoid_h1, h1_mean, h1_sample = self.sample_h_given_v(v1_sample)
        return [pre_sigmoid_v1, v1_mean, v1_sample, pre_sigmoid_h1, h1_mean, h1_sample]

    def gibbs_vhv(self, v0_sample):
        ''' This function implements one step of Gibbs sampling,
            starting from the visible state'''
        pre_sigmoid_h1, h1_mean, h1_sample = self.sample_h_given_v(v0_sample)
        pre_sigmoid_v1, v1_mean, v1_sample = self.sample_v_given_h(h1_sample)
        return [pre_sigmoid_h1, h1_mean, h1_sample, pre_sigmoid_v1, v1_mean, v1_sample]

    def free_energy(self, v_sample):
        ''' Function to compute the free energy '''
        wx_b = T.dot(v_sample, self.W) + self.hbias
        vbias_term = T.dot(v_sample, self.vbias)
        hidden_term = T.sum(T.log(1 + T.exp(wx_b)), axis=1)
        return -hidden_term - vbias_term

    def get_cost_updates(self, lr=0.1, persistent=None, k=1):
        """
        This functions implements one step of CD-k or PCD-k

        :param lr: learning rate used to train the RBM

        :param persistent: None for CD. For PCD, shared variable containing old state
        of Gibbs chain. This must be a shared variable of size (batch size, number of
        hidden units).

        :param k: number of Gibbs steps to do in CD-k/PCD-k

        Returns a proxy for the cost and the updates dictionary. The
        dictionary contains the update rules for weights and biases but
        also an update of the shared variable used to store the persistent
        chain, if one is used.
        """

        # compute positive phase
        pre_sigmoid_ph, ph_mean, ph_sample = self.sample_h_given_v(self.input)

        # decide how to initialize persistent chain:
        # for CD, we use the newly generate hidden sample
        # for PCD, we initialize from the old state of the chain
        if persistent is None:
            chain_start = ph_sample
        else:
            chain_start = persistent