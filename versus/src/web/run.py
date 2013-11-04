#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This module defines the entry point for flask_ web server implementation
    of the versus.com.  This module is consumable
    by the Apache web server via WSGI interface via mod_wsgi.  An Apache
    server can be pointed to api.wsgi such that Apache may be used as a
    wrapper in this way.

    .. _flask: http://flask.pocoo.org

"""

from versus.config import settings

__author__ = settings.AUTHORS
__date__ = "2013-08-20"
__license__ = settings.LICENSE

from flask import Flask, render_template, Markup, redirect, url_for, \
    request, escape, flash, jsonify, make_response
from versus.src.web import app
from views import init_views

######
#
# Execution
#
#######

#Send serious errors to devs

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter

    mail_handler = SMTPHandler('127.0.0.1',
        'bobs.ur.uncle@gmail.com',
        settings.ADMINS, 'versus encountered error')
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    app.logger.addHandler(mail_handler)

# With the presence of flask.ext.login module
if settings.__flask_login_exists__:
    from versus.src.web.session import login_manager
    login_manager.setup_app(app)


if __name__ == '__main__':
    init_views()
    app.run(debug=True,
        use_reloader=False,
        host=settings.__instance_host__,
        port=settings.__instance_port__,)
