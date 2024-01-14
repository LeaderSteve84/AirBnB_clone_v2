#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using
the function do_deploy
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.167.187.121', '100.25.3.235']


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    try:
        if not exists(archive_path):
            print(f"Error: Archive '{archive_path}' not found.")
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
        print(f"An error occured: {e}")
        return False
