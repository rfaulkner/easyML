#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module defines the entry point for flask_ web server implementation
    of the test.com.  This module is consumable
    by the Apache web server via WSGI interface via mod_wsgi.  An Apache
    server can be pointed to api.wsgi such that Apache may be used as a
    wrapper in this way.

    .. _flask: http://flask.pocoo.org

"""

from versus.config import settings, set_log

__author__ = settings.AUTHORS
__date__ = "2013-08-20"
__license__ = settings.LICENSE

import argparse
import sys

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
        settings.ADMINS, 'test encountered error')
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

from versus.src.web.session import login_manager
login_manager.setup_app(app)


def parseargs():
    """Parse command line arguments.

    Returns *args*, the list of arguments left over after processing.

    """
    parser = argparse.ArgumentParser(
        description="This script serves as the entry point for flask.",
        epilog="",
        conflict_handler="resolve",
        usage="run.py [OPTS]"
              "\n\t[-q --quiet] \n\t[-s --silent] \n\t[-v --verbose]"
              "\n\t[-d --debug] \n\t[-r --reloader]"
    )

    parser.allow_interspersed_args = False

    defaults = {
        "quiet": 0,
        "silent": False,
        "verbose": 1,
    }

    # Global options.
    parser.add_argument("-c", "--count",
                        default=1, type=int,
                        help="number of tags to log")
    parser.add_argument("-q", "--quiet",
                        default=defaults["quiet"], action="count",
                        help="decrease the logging verbosity")
    parser.add_argument("-s", "--silent",
                        default=defaults["silent"], action="store_true",
                        help="silence the logger")
    parser.add_argument("-v", "--verbose",
                        default=defaults["verbose"], action="count",
                        help="increase the logging verbosity")
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Run in flask debug mode.")
    parser.add_argument("-r", "--reloader",
                        action="store_true",
                        help="Use flask reloader.")

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    # Parse cli args
    args = parseargs()
    log = set_log(args, sys.stdout, sys.stderr)

    # Apply routing & auth deco to views
    init_views()

    app.run(debug=args.debug,
            use_reloader=args.reloader,
            host=settings.__instance_host__,
            port=settings.__instance_port__,)

else:
    # Invocation by apache mod_wsgi

    # Setup file logger, flask context exceptions will be
    # written to the handler
    #
    # TODO - ensure perms exist

    from logging import FileHandler, Formatter
    log = FileHandler(settings.FLASK_LOG)

    log.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))

    log.setLevel(logging.DEBUG)
    app.logger.addHandler(log)

    # Initialize views
    init_views()

