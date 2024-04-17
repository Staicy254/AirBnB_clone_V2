#!/usr/bin/python3
"""Module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once, sudo

env.hosts = ["34.73.0.174", "35.196.78.105"]
"""List host server IP addresses."""


@runs_once
def do_pack():
    """archives static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = f"versions/web_static_{cur_time.year}{cur_time.month}{cur_time.day}{cur_time.hour}{cur_time.minute}{cur_time.second}.tgz"
    try:
        print(f"Packing web_static to {output}")
        local(f"tar -cvzf {output} web_static")
        archize_size = os.stat(output).st_size
        print(f"web_static packed: {output} -> {archize_size} Bytes")
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys - staticfiles to the host servers.
    Args:
        archive_path (str): Path to archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}/"
    success = False
    try:
        put(archive_path, f"/tmp/{file_name}")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
        run(f"rm -rf /tmp/{file_name}")
        run(f"mv {folder_path}web_static/* {folder_path}")
        run(f"rm -rf {folder_path}web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {folder_path} /data/web_static/current")
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """archives & deploys static files to host servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


def do_clean(number=0):
    """deletes out_of_date archives of static files.

    Args:
        number (int): Number of archives to keep.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink(f'versions/{archive}')
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        f" | sort -r | tr '\\n' ' ' | cut -d ' ' -f{start + 1}-)"
    ]
    run(''.join(cmd_parts))

