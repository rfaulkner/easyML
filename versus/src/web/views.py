"""
Module implementing the view portion of the MVC pattern.
"""

import os
import datetime

from versus.config import log
from versus.config.settings import AUTHORS, LICENSE, HDFS_BUFFER_FILE, \
    __version__, HDFS_STAGE, MAX_BUFFER_SIZE
from versus.src.web import app
from versus.tools.dataIO import DataIOHDFS, DataIOMySQL

from flask import render_template, redirect, url_for, \
    request, escape, flash

__author__ = AUTHORS
__date__ = "2013-08-20"
__license__ = LICENSE


# Flask Login views

from versus.src.web.session import APIUser

from flask.ext.login import login_required, logout_user, \
    confirm_login, login_user, fresh_login_required, current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form:

        username = escape(unicode(str(request.form['username'])))
        passwd = escape(unicode(str(request.form['password'])))
        remember = request.form.get('remember', 'no') == 'yes'

        # Initialize user
        user_ref = APIUser(username)
        user_ref.authenticate(passwd)

        log.debug(__name__ + ' :: Authenticating "{0}"/"{1}" ...'.
            format(username, passwd))

        if user_ref.is_authenticated():
            login_user(user_ref, remember=remember)
            flash('Logged in.')
            return redirect(request.args.get('next')
                            or url_for('api_root'))
        else:
            flash('Login failed.')
    return render_template('login.html')

@app.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    if request.method == 'POST':
        confirm_login()
        flash(u'Reauthenticated.')
        return redirect(request.args.get('next') or url_for('api_root'))
    return render_template('reauth.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('api_root'))


def home():
    """ View for root url - API instructions """

    if current_user.is_anonymous():
        return render_template('index_anon.html')
    else:
        return render_template('index.html')


def about():
    return render_template('about.html')


def contact():
    return render_template('contact.html')


def version():
    return render_template('version.html', version=__version__)


def add_model():
    """ Respond with view for model add form """
    return render_template('add_model.html')


def add_model_process():
    """ Handles processing of add model """
    model_name = request.data['modelName'] if 'modelName' in request.data \
        else None
    model_type = request.data['modelType'] if 'modelType' in request.data \
        else None

    if not model_name or not model_type:
        log.info('Added model (type, name) = "%s", "%s" ' % (model_name,
                                                             model_type))
        mysql = DataIOMySQL()
        mysql.connect()
        mysql.insert('Model', uid=-1, name=model_name, mtype=model_name,
                     date_create=datetime.datetime.now().strftime(''))
    else:
        log.error('Missing model fields in POST data "%s"' % str(request.data))


def ingest():
    """
    Handles form data ingestion.
    """
    # redirect to home with a message
    # return render_template('about.html')

    label = request.form['phraseInput']
    text = request.form['labelInput']
    # model = request.form['modelInput']

    with open(HDFS_BUFFER_FILE, 'a') as f:
        # TODO - use control char as separator
        f.write(str(label) + ':' + str(text) + '\n')

        # Flush the file to HDFS_STAGE if it exceeds MAX_BUFFER_SIZE
        #   TODO - This should be done in a separate thread there'll
        #   TODO - also need to be locking on the file
        if (os.stat(HDFS_BUFFER_FILE).st_size >= MAX_BUFFER_SIZE):
            DataIOHDFS().copy_from_local(HDFS_BUFFER_FILE, HDFS_STAGE)
            os.remove(HDFS_BUFFER_FILE)

    return redirect(url_for('home'))


def train():
    """
    Invoke training from control.
    """

    # TODO - Get form data
    dataset = None
    model_type = None

    # TODO - given model type and data train a new model and store

    return render_template('train.html')


# Add View Decorators
# ##

# Stores view references in structure
view_list = {
    home.__name__: home,
    about.__name__: about,
    contact.__name__: contact,
    version.__name__: version,
    ingest.__name__: ingest,
    train.__name__: train,
    add_model.__name__: add_model,
    add_model_process.__name__: add_model_process,
}

# Dict stores routing paths for each view

from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

route_deco = {
    home.__name__: app.route('/'),
    about.__name__: app.route('/about/'),
    contact.__name__: app.route('/contact/'),
    version.__name__: app.route('/version'),
    ingest.__name__: app.route('/ingest', methods=['GET', 'POST']),
    train.__name__: app.route('/train', methods=['GET', 'POST']),
    add_model.__name__: app.route('/train'),
    add_model_process.__name__: app.route('/train', methods=['POST'])
}

# Dict stores flag for login required on view
views_with_anonymous_access = [
    home.__name__,
    about.__name__,
    contact.__name__,
    ingest.__name__,
    train.__name__,
    add_model.__name__,
    add_model_process.__name__,
]

# Apply decorators to views
def init_views():
    for key in view_list:
        if key not in views_with_anonymous_access:
            view_list[key] = login_required(view_list[key])

    for key in route_deco:
        route = route_deco[key]
        view_method = view_list[key]
        view_list[key] = route(view_method)

    log.info(__name__ + ' :: Registered views - {0}'.format(str(view_list)))