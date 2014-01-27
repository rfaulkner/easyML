#!/usr/bin/python
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

global log

# NullHandler was added in Python 3.1.
try:
    NullHandler = logging.NullHandler
except AttributeError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Add a do-nothing NullHandler to the module logger to prevent "No handlers
# could be found" errors. The calling code can still add other, more useful
# handlers, or otherwise configure logging.
log = logging.getLogger(__name__)
log.addHandler(NullHandler())


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

# With the presence of flask.ext.login module
if settings.__flask_login_exists__:
    from versus.src.web.session import login_manager
    login_manager.setup_app(app)


def parseargs():
    """Parse command line arguments.

    Returns *args*, the list of arguments left over after processing.

    """
    parser = argparse.ArgumentParser(
        description="This script serves as the entry point for git deploy.",
        epilog="",
        conflict_handler="resolve",
        usage="git-deploy method [remote] [branch]"
              "\n\t[-q --quiet] \n\t[-s --silent] "
              "\n\t[-d --debug] \n\t[-c --count [0-9]+] \n\t[-f --force] "
              "\n\t[-t --tag] \n\t[-a --auto_sync] "
              "\n\t[-y --sync SCRIPT NAME] "
              "\n\nmethod=[start|sync|abort|revert|diff|show_tag|"
              "log_deploys|finish]"
    )

    parser.allow_interspersed_args = False

    defaults = {
        "quiet": 0,
        "silent": False,
        "verbose": 1,
    }

    # Global options.
    parser.add_argument('ordered_args', metavar='ordered_args', type=str,
                        nargs='+', help='Specifies the git deploy method and '
                                        'additional args depending on the '
                                        'method called.')
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

    # Apply routing & auth deco to views
    init_views()

    log = set_log(args, sys.stdout, sys.stderr)

    app.run(debug=args.debug,
            use_reloader=args.reloader,
            host=settings.__instance_host__,
            port=settings.__instance_port__,)
