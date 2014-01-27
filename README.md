DynamicLearn
============

Interesting ways of mixing human collaboration with Machine Learning.  This project leverages the Theano package [1]
to dynamically train deep neural networks for production environments.  Theano optimizes and simplifies training over
deep models.

[1] http://deeplearning.net/software/theano/

Setup
-----

To get the app running:

    ~ $ git clone https://github.com/rfaulkner/versus.git
    ~ $ cd versus
    ~ $ sudo pip install -e .
    ~ $ ./versus/src/web/run.py [OPTS]

Hosting can be accessed via the endpoint http://127.0.0.1:5000.

For apache setup see - http://flask.pocoo.org/docs/deploying/mod_wsgi/.


Vagrant Initialization
----------------------

The default vagrant instance includes the following in addition to the vagrant "precise32" [1] Ubuntu image:

    gfortran
    g++
    apache2
    git
    vim
    redis-server
    curl
    python 2.7.3
    numpy
    python-redis
    java7
    hadoop (Single)

From a (L)UNIX box

    ~ $ cd versus/vagrant
    ~ $ vagrant up
    ~ $ vagrant ssh

From this point follow the setup commands above.


References
----------

[1] http://www.vagrantbox.es
