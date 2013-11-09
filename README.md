Madbox
======

Interesting ways of mixing human collaboration with Machine Learning.

Setup
-----

To get the app running:

    $ cd {%PROJECT HOME%}
    $ cp src/config/settings.py.example src/config/settings.py
    $ sudo pip install -e .
    $ python src/web/run.py

Hosting can be accessed via the endpoint http://127.0.0.1:5000.

For apache setup see - http://flask.pocoo.org/docs/deploying/mod_wsgi/.
