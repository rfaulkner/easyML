easyML
======

Interesting ways of mixing human collaboration with Machine Learning.  This project leverages the Theano package [1]
to dynamically train deep neural networks for production environments.  Theano optimizes and simplifies training over
deep models.

The project exposes a web interface via Python's Flask package for data ingestion.


Setup
-----

To get the app running:

    ~ $ git clone https://github.com/rfaulkner/easyML.git
    ~ $ cd versus
    ~ $ sudo pip install -e .
    ~ $ ./versus/src/web/run.py [OPTS]

Hosting from Flask can be accessed via the endpoint http://127.0.0.1:5000.

For apache setup see - http://flask.pocoo.org/docs/deploying/mod_wsgi/.


Frontend
--------

There is a basic front-end supported by Flask that can be used for data ingestion.  See "Setup mod_wsgi for Flask" below.
Styling utilizes bootstrap.js [2]; the libs are in $PROJECT_HOME/versus/src/web/static.


Vagrant Initialization
----------------------

The default vagrant instance includes the following in addition to the vagrant "precise32" [3] Ubuntu image:

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


Setup mod_wsgi for Flask
------------------------

To setup Flask to run with mod_wsgi add this virtualhost to [4]:

    <VirtualHost *>
        ServerName {% [ip|url] %}

        WSGIDaemonProcess flask_ml user=user1 group=group1 threads=5
        WSGIScriptAlias / /path/to/app.wsgi

        <Directory /var/www/flask_ml>
            WSGIProcessGroup flask_ml
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

You can find a template for the config file in $PROJECT_ROOT/vagrant/vhost.conf.  You may want to modify the config
to suit your own environment however, the default process:

    ~ $ cp /home/vagrant/easyML/vagrant/vhost.conf $HTTPD_ROOT/sites-available
    ~ $ mv $HTTPD_ROOT/sites-available/vhost.conf $HTTPD_ROOT/sites-available/flask-easyML
    ~ $ cp ln -s $HTTPD_ROOT/sites-available/flask_easyML $HTTPD_ROOT/sites-enabled/flask-easyML
    ~ $ sudo a2ensite flask-easyML
    ~ $ sudo apache2ctl restart

You can curl the host to ensure that it's functioning properly\*:

    ~ $ curl http://localhost:8080/

If there are issues check the logs in $PROJECT_ROOT/logs.

(\*) That by default for this project Vagrant is setup to forward port 80 in the VM to 4567 on the host machine.  If you
want to use a different port in your apache setup you'll need to ensure that it's also forwarded [5].


References
----------

[1] http://deeplearning.net/software/theano/

[2] http://getbootstrap.com/javascript/

[3] http://www.vagrantbox.es

[4] http://flask.pocoo.org/docs/deploying/mod_wsgi/

[5] https://docs.vagrantup.com/v2/networking/forwarded_ports.html

