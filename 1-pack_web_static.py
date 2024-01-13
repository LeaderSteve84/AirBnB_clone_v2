#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack
"""

from datetime import datetime
from fabric.api import *


def do_pack():

    """
    generates a .tgz archive
    """

    # use datetime.utcnow() instead of datetime.now()
    # for consistency across time zones
    time = datetime.utcnow()

    # use a consistent date/time format for the archive name
    archive = 'web_static_{}.tgz'.format(time.strftime("%Y%m%d%H%M%S"))

    # Use the os.path function to join paths component
    local('mkdir -p versions')

    # use the capture context manager to capture the result of the command
    create = local('tar -cvzf versions/{} web_static'.format(archive))

    if create.failed:
        return None
    else:
        return 'versions/{}'.format(archive)


if __name__ == "__main__":
    # run the do_pack when th script is directly executed
    result = do_pack()

    if result:
        print('Package: {}'.format(result))
    else:
        print('Failed to create the package.')
