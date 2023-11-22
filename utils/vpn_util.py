import subprocess
import sys
from enum import Enum


class VPN(Enum):
    """
    VPN枚举
    Attributes:
        Start: 启动
        Stop: 停止
    """
    Start = "scutil --nc start '{name}' --user {user} --password {password} --secret {secret}"
    Stop = "scutil --nc stop '{name}'"


class VPNHelper:
    """
    VPN工具类
    """
    def __init__(self, _name, _user, _password, _secret):
        """
        初始化VPN工具类
        Args:
            _name: VPN名称
            _user: 用户名
            _password: 密码
            _secret: 密钥
        """
        self.name = _name
        self.user = _user
        self.password = _password
        self.secret = _secret

    def __str__(self):
        return "vpn information >\nname:%s\nuser:%s\npassword:******\nsecret:%s" % (self.name, self.user, self.secret)

    def __function(self, _enum):
        """
        执行方法
        Args:
            _enum: 枚举类型
        """
        _command = _enum.value.format(name=self.name, user=self.user, password=self.password, secret=self.secret)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        _out, _err = _process.communicate()
        sys.stdout.write("out=%s\n"
                         "err=%s \n" % (str(_out), str(_err)))
        sys.stdout.flush()
        if _err == "":
            sys.stdout.write("%s success !\n" % _enum)
        else:
            sys.stdout.write("%s fail !\n" % _enum)
        sys.stdout.flush()

    def start(self):
        """
        启动VPN
        """
        self.__function(VPN.Start)

    def stop(self):
        """
        停止VPN
        """
        self.__function(VPN.Stop)
