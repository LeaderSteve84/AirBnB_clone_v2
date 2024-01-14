#!/usr/bin/python3
"""deletes out-of-date archives, using
the function do_clean
"""

import os
from fabric.api import *

env.hosts = ['54.167.187.121', '100.25.3.235']


def do_clean(number=0):
    """delete outdated archives.
    Args:
        number (int): The number of archives to keep.
        If number is 0 or 1, keep only the most recent
        version of your archive.
        if number is 2, keep the most recent, and
        second most recent versions of your archive.
        etc
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
