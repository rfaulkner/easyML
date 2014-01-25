DynamicLearn
============

Interesting ways of mixing human collaboration with Machine Learning.  This project leverages the Theano package [1]
to dynamically train deep neural networks for production environments.  Theano optimizes and simplifies training over
deep models.

[1] http://deeplearning.net/software/theano/

Setup
-----

To get the app running:

    $ git clone https://github.com/rfaulkner/versus.git
    $ cd versus
    $ sudo pip install -e .
    $ python versus/src/web/run.py

Hosting can be accessed via the endpoint http://127.0.0.1:5000.

For apache setup see - http://flask.pocoo.org/docs/deploying/mod_wsgi/.
