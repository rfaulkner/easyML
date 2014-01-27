import logging


def set_log(args, out, err):
    """
    Configures a logger and returns it.

    :param args: command line args
    :param out: stdout
    :param err: stderr
    """
    level = logging.WARNING - ((args.verbose - args.quiet) * 10)
    if args.silent:
        level = logging.CRITICAL + 1

    log_format = "%(asctime)s %(levelname)-8s %(message)s"
    handler = logging.StreamHandler(err)
    handler.setFormatter(logging.Formatter(fmt=log_format,
                         datefmt='%b-%d %H:%M:%S'))

    log = logging.getLogger(__name__)
    log.addHandler(handler)
    log.setLevel(level)

    return log