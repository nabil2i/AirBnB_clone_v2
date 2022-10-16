#!/usr/bin/python3
"""Use the function deploy() to generate a .tgz archive from the
contents of the web_static folder via the function do_pack() and
distribute the archive to the web server using the function do_deploy"""

from datetime import datetime
from fabric.api import local, env, put, run
from os.path import exists


env.use_ssh_config = True
env.hosts = ['3.218.67.248', '3.236.227.91']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Function that compresses content
    and generates the tgz archive file"""
    date_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(date_time)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(path))
    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    """Function that distributes an archive to a server"""
    if exists(archive_path) is False:
        return False
    file_name = archive_path.split("/")[-1]
    file_noext = file_name.split(".")[0]
    path = "/data/web_static/releases/"
    r = put(archive_path, '/tmp/')
    if r.failed:
        return False
    r = run('mkdir -p {}{}/'.format(path, file_noext))
    if r.failed:
        return False
    r = run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, file_noext))
    if r.failed:
        return False
    r = run('rm /tmp/{}'.format(file_name))
    if r.failed:
        return False
    r = run('mv {0}{1}/web_static/* {0}{1}/'.format(path, file_noext))
    if r.failed:
        return False
    r = run('rm -rf {}{}/web_static'.format(path, file_noext))
    if r.failed:
        return False
    r = run('rm -rf /data/web_static/current')
    if r.failed:
        return False
    r = run('ln -s {}{}/ /data/web_static/current'.format(path, file_noext))
    if r.failed:
        return False
    return True


def deploy():
    """create and distribute an archive to the servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """delete out-of-date archives"""
    archives = local("ls -1t versions", capture=True)
    files = archives.split("\n")
    num = int(number)
    if num in (0, 1):
        num = 1
    for i in files[num:]:
        local("rm versions/{}".format(i))
    server_archives = run("ls -1t /data/web_static/releases")
    server_files = server_archives.split("\n")
    for i in server_files[num:]:
        if i is 'test':
            continue
        run("rm -rf /data/web_static/releases/{}".format(i))
