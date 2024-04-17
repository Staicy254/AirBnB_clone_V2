#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from tarfile import CompressionError
from fabric.api import local, runs_once
from fabric.exceptions import NetworkError, CommandExecutionError


@runs_once
def do_pack(
    archive_dir="web_static",
    compression="gz"
):
    """
    Archives the static files from a specified directory.

    Args:
        archive_dir (str, optional): The directory to archive.
            Defaults to "web_static".
        compression (str, optional): The compression format to use.
            Defaults to "gz".

    Returns:
        str: The path to the created archive file, or None on error.
    """
    if not os.path.isdir(archive_dir):
        print(f"Error: Directory '{archive_dir}' does not exist.")
        return None

    cur_time = datetime.now()
    output = (
        f"versions/web_static_{cur_time.year}{cur_time.month}{cur_time.day}"
        f"{cur_time.hour}{cur_time.minute}{cur_time.second}.{compression}"
    )

    try:
        print(f"Packing {archive_dir} to {output}")
        local(f"tar -c{compression}f {output} {archive_dir}")
        archive_size = os.stat(output).st_size
        print(f"{archive_dir} packed: {output} -> {archive_size} Bytes")
    except FileNotFoundError as e:
        print(f"Error packing directory: {e}")
        output = None
    except CompressionError as e:
        print(f"Compression error: {e}")
        output = None
    except NetworkError as e:
        print(f"Network error: {e}")
        output = None
    except CommandExecutionError as e:
        print(f"Command execution error: {e}")
        output = None
    except Exception as e:
        print(f"Unexpected error: {e}")
        output = None

    return output

