# -*- coding: UTF-8 -*-
import subprocess
import sys
from enum import Enum


class AWSCMD(Enum):
    Upload = "aws s3 cp {local_path} s3://{bucket_url}/{remote_path}"
    Delete = "aws s3 rm s3://{bucket_url}/{remote_path}"


class AWSHelper:
    """ 亚马逊 AWS S3 工具类 """
    def __init__(self, bucket_url):
        """ 初始化
        Args:
            bucket_url: 桶的链接 s3://bucket_url
        """
        self.bucket_url = bucket_url

    def __str__(self):
        return "aws information >\nbucket_url:%s" % self.bucket_url

    def __function(self, _enum, _local_path=None, _remote_path=None, _bucket_url=None):
        """
        执行方法
        Args:
            _enum: 枚举类型
            _local_path: 本地文件
            _remote_path: 远端文件
            _bucket_url: 桶的链接 s3://bucket_url
        """
        _command = _enum.value.format(local_path=_local_path, remote_path=_remote_path, _bucket_url=self.bucket_url)
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
        """ 上传文件
        上传本地文件到远端文件，有会覆盖

        Args:
            local_path: 本地文件
            remote_path: 远端文件
        """
        self.__function(AWSCMD.Upload, local_path, remote_path)

    def delete(self, remote_path):
        """ 删除文件
        删除远端文件，没有不会报错

        Args:
            remote_path: 远端文件
        """
        self.__function(AWSCMD.Delete, _remote_path=remote_path)
