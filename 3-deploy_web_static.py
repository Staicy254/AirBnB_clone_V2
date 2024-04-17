#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once, sudo


# Load server IPs from environment variables (assuming they are set)
env.user = "username"  # Assuming you have SSH access with username
env.hosts = [os.getenv("HOST1_IP", ""), os.getenv("HOST2_IP", "")]


@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = f"versions/web_static_{cur_time.strftime('%Y%m%d%H%M%S')}.tgz"
    try:
        print(f"Packing web_static to {output}")
        local(f"tar -cvzf {output} web_static")
        archive_size = os.stat(output).st_size
        print(f"web_static packed: {output} -> {archive_size} Bytes")
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """The static files should be deployed to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}/"
    SUCCESS = False
    try:
        put(archive_path, f"/tmp/{file_name}")
        with sudo():
            run(f"mkdir -p {folder_path}")
            run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
            run(f"rm -rf /tmp/{file_name}")
            run(f"mv {folder_path}web_static/* {folder_path}")
            run(f"rm -rf {folder_path}web_static")
            run(f"rm -rf /data/web_static/current")
            run(f"ln -s {folder_path} /data/web_static/current")
        print('New version deployed!')
        SUCCESS = True
    except Exception:
        SUCCESS = False
    return SUCCESS


def deploy():
    """Archives & deployment of - the static files to the host servers.

    Logs the deployment process and returns success/failure status.
    """

    print("Starting deployment...")

    archive_path = do_pack()
    if not archive_path:
        print("Packing failed. Aborting deployment.")
        return False

    try:
        print("Uploading archive...")
        do_deploy(archive_path)
        print("Deployment successful!")
        return True
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False


# Example usage with basic logging
if __name__ == "__main__":
    SUCCESS = deploy()
    if SUCCESS:
        print("Deployment completed successfully.")
    else:
        print("Deployment failed.")

