import subprocess
import sys
from enum import Enum


class AWSCMD(Enum):
    Upload = "aws s3 cp {local_path} s3://jielan2-usa-storage-bucket/{remote_path}"
    Delete = "aws s3 rm s3://jielan2-usa-storage-bucket/{remote_path}"


class AWSHelper:

    def __init__(self):
        sys.stdout.write("nothing to init.")
        sys.stdout.flush()

    def __str__(self):
        return ""

    def __function(self, _enum, _local_path=None, _remote_path=None, _thread_count=None):
        _command = _enum.value.format(local_path=_local_path, remote_path=_remote_path, thread_count=_thread_count)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True)
        _process.wait()
        if _process.returncode != 0:
            sys.stdout.write("{enum_type} failed ! error : {error}\n".format(enum_type=_enum, error=_process.stderr))
        else:
            sys.stdout.write("{enum_type} successful !\n".format(enum_type=_enum))
        sys.stdout.flush()

    def upload(self, local_path, remote_path):
        self.__function(AWSCMD.Upload, local_path, remote_path)

    def delete(self, remote_path):
        self.__function(AWSCMD.Delete, _remote_path=remote_path)
