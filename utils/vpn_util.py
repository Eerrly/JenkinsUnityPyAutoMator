import subprocess
import sys
from enum import Enum


class VPN(Enum):
    Start = "scutil --nc start '{name}' --user {user} --password {password} --secret {secret}"
    Stop = "scutil --nc stop '{name}'"


class VPNHelper:
    """
    Only Linux Can Use it
    """
    def __init__(self, _name, _user, _password, _secret):
        self.name = _name
        self.user = _user
        self.password = _password
        self.secret = _secret

    def __str__(self):
        return "vpn information >\nname:%s\nuser:%s\npassword:******\nsecret:%s" % (self.name, self.user, self.secret)

    def __function(self, _enum):
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
        self.__function(VPN.Start)

    def stop(self):
        self.__function(VPN.Stop)
