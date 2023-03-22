# -*- coding: UTF-8 -*-
import subprocess
import sys
from enum import Enum


class COSCMD(Enum):
    Config = "coscmd config -a {secretId} -s {secretKey} -b {bucket} -r {region}"
    Upload = "coscmd upload -r {local_path} {remote_path}/"
    Delete = "cosmod delete -r {remote_path}"


class COSHelper:
    """ 腾讯云 COS 工具类 """
    def __init__(self, secretId, secretKey, bucket, region):
        self.secretId = secretId
        self.secretKey = secretKey
        self.bucket = bucket
        self.region = region

    def __str__(self):
        return "cos information >\nsecretId:%s\nbucket:%s\nregion:%s" % (self.secretId, self.bucket, self.region)

    def __function(self, _enum, _local_path=None, _remote_path=None):
        _command = _enum.value.format(
            secretId=self.secretId, secretKey=self.secretKey, bucket=self.bucket, region=self.region,
            local_path=_local_path, remote_path=_remote_path
        )
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True)
        _process.wait()
        if _process.returncode != 0:
            sys.stdout.write("{enum_type} failed ! error : {error}\n".format(enum_type=_enum, error=_process.stderr))
        else:
            sys.stdout.write("{enum_type} successful !\n".format(enum_type=_enum))
        sys.stdout.flush()

    def config(self):
        """配置
        配置COS
        """
        self.__function(COSCMD.Config)

    def upload(self, _local_path, _remote_path):
        """上传文件
        上传本地文件到远端文件

        Args:
            _local_path: 本地文件路径
            _remote_path: 远端文件路径
        """
        self.__function(COSCMD.Upload, _local_path, _remote_path)

    def delete(self, _remote_path):
        """删除文件
        删除远端文件，如果是文件夹，路径后面有'/'

        Args:
            _remote_path: 远端文件路径
        """
        self.__function(COSCMD.Delete, _remote_path)
