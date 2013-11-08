
import sys
import logging

# Configure global logger
#   TODO - add new log handlers and loggers
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%b-%d %H:%M:%S')