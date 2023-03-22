import subprocess
import sys
from enum import Enum


class SVN(Enum):
    CleanUp = "svn cleanup {clean_path} --username {user} --password {password}"
    ResolveTheirsFull = "svn resolve -R --accept theirs-full {path} --username {user} --password {password}"
    ResolveWorking = "svn resolve -R --accept working {path} --username {user} --password {password}"
    Revert = "svn revert -R -q {path} --username {user} --password {password}"
    UpdateTheirsFull = "svn update --accept theirs-full {path} --username {user} --password {password}"
    Diff = "svn diff -r {l_version}:{r_version} --summarize {path} --username {user} --password {password}"
    Status = "svn status {file_path} --username {user} --password {password}"
    Commit = "svn commit {file_path} -m \"{commit_message}\""


class SVNHelper:
    """SVN工具类"""
    def __init__(self, _user, _password, _path, _clean_path=None):
        self.user = _user
        self.password = _password
        self.path = _path
        self.clean_path = _clean_path if _clean_path is not None else _path

    def __str__(self):
        return "svn information >\nuser:%s\npassword:******\npath:%s\nclean_path:%s" % (self.user, self.path, self.clean_path)

    def __function(self, _enum, _lv=None, _rv=None, _out_file=None, _file_path=None, _commit_message=None):
        _command = _enum.value.format(user=self.user, password=self.password, path=self.path, clean_path=self.clean_path, l_version=_lv, r_version=_rv, file_path=_file_path,
                                      commit_message=_commit_message)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _out = _out_file if _out_file is not None else subprocess.PIPE
        _process = subprocess.Popen(_command, shell=True, stdout=_out, stderr=subprocess.PIPE, universal_newlines=True)
        _out, _err = _process.communicate()
        sys.stdout.write("out=%s\n"
                         "err=%s \n" % (str(_out), str(_err)))
        sys.stdout.flush()
        if str(_err) == "":
            sys.stdout.write("%s success !\n" % _enum)
        else:
            sys.stdout.write("%s fail !\n" % _enum)
        sys.stdout.flush()
        return str(_out), str(_err)

    def clean_revert_update(self):
        self.__function(SVN.CleanUp)
        self.__function(SVN.ResolveTheirsFull)
        self.__function(SVN.ResolveWorking)
        self.__function(SVN.Revert)
        self.__function(SVN.UpdateTheirsFull)
        self.__function(SVN.ResolveWorking)

    def diff(self, _lv, _rv, _out_file=None):
        """获取差异文件
        通过SVN获取差异文件

        Args:
            _lv: SVN起始版本
            _rv: SVN结束版本
            _out_file: 导出文件路径
        """
        return self.__function(SVN.Diff, _lv=_lv, _rv=_rv, _out_file=_out_file)

    def status(self, _file_path):
        """获取文件状态
        通过SVN获取文件状态

        Args:
            _file_path: 文件路径
        """
        return self.__function(SVN.Status, _file_path=_file_path)

    def commit(self, _file_path, _commit_message):
        """提交文件
        通过SVN提交文件

        Args:
            _file_path: 文件路径
            _commit_message: 提交信息
        """
        return self.__function(SVN.Commit, _file_path=_file_path, _commit_message=_commit_message)

    def update(self):
        return self.__function(SVN.UpdateTheirsFull)
