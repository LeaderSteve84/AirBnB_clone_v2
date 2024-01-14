#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy
"""

from fabric.api import put, run, env, local
from datetime import datetime
from os.path import exists
env.hosts = ['54.167.187.121', '100.25.3.235']


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


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    try:
        if not exists(archive_path):
            print("Error: Archive '{}' not found.".format(archive_path))
            return False

        fileN = archive_path.split("/")[-1]
        wtht_ext = fileN.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, wtht_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(fileN, path, wtht_ext))
        run('rm /tmp/{}'.format(fileN))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, wtht_ext))
        run('rm -rf {}{}/web_static'.format(path, wtht_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, wtht_ext))
        return True
    except Exception as e:
        print("An error occured: {}".format(e))
        return False


def deploy():
    """create and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
