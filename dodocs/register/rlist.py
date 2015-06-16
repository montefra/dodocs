"""List ``dodocs`` cron jobs

Copyright (c) 2015 Francesco Montesano
MIT Licence
"""

from crontab import CronTab

import dodocs.logger as dlog


def rlist(args):
    """List the profiles

    Parameters
    ----------
    args : namespace
        parsed command line arguments
    """
    log = dlog.getLogger()

    cron = CronTab()

    cron_iter = cron.find_command("dodocs")

    for ci in cron_iter:
        log.info(ci)
