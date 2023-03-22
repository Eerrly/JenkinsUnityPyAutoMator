import os
import sys

import paramiko


class SSHHelper:
    """
    SSH File Transfer Protocol (SFTP)
    """
    def __init__(self, _host, _port, _user, _passwd):
        self.host = _host
        self.port = _port
        self.user = _user
        self.passwd = _passwd
        __transport = paramiko.Transport((self.host, self.port))
        __transport.connect(username=self.user, password=self.passwd)
        self.sftp = paramiko.SFTPClient.from_transport(__transport)

    def __str__(self):
        return "ssh information >\nuser:%s\npasswd:******\nhost:%s\nport:%d" % (self.user, self.host, self.port)

    def __cwd(self, _remote_path, _can_delete=False):
        _dir_list = _remote_path.split("/")
        index = 0
        while index < len(_dir_list):
            sys.stdout.write("cwd %s ...\n" % _dir_list[index])
            sys.stdout.flush()
            try:
                self.sftp.chdir(_dir_list[index])
                index = index + 1
            except:  # can't use 'Exception' in this
                self.sftp.mkdir(_dir_list[index])
                self.sftp.chdir(_dir_list[index])
                index = index + 1
        if _can_delete:
            sys.stdout.write("'_can_delete' is True, start delete .\n")
            sys.stdout.flush()
            self.del_dir()

    def __exist_ftp_file(self, _remote_file, _remote_dir=None):
        try:
            if _remote_dir is not None:
                self.__cwd(_remote_dir, False)
            if _remote_file in self.sftp.listdir():
                return True
            else:
                return False
        except:
            return False

    def __upload_call_back(self, transferred, toBeTransferred):
        sys.stdout.write("uploading %.2f%% ... \n" % (float(transferred) / toBeTransferred * 100))
        sys.stdout.flush()

    def cd(self, _path):
        self.sftp.chdir(_path)

    def quit(self):
        self.sftp.close()

    def __del_file(self, _f):
        sys.stdout.write(">[-] %s ... \n" % _f)
        sys.stdout.flush()
        self.sftp.remove(_f)

    def del_dir(self):
        for _f in self.sftp.listdir():
            try:
                self.sftp.chdir(_f)
                self.del_dir()
                self.sftp.chdir("..")
                sys.stdout.write("[-] %s ... \n" % _f)
                sys.stdout.flush()
                self.sftp.rmdir(_f)
            except:
                self.__del_file(_f)

    def upload_file(self, _local_file):
        if not os.path.isfile(_local_file):
            sys.stdout.write("is not file > %s ... \n" % _local_file)
            sys.stdout.flush()
            return
        __local_file_name = os.path.basename(_local_file)
        if self.__exist_ftp_file(__local_file_name):
            sys.stdout.write("exist file and delete file > %s ... \n" % __local_file_name)
            sys.stdout.flush()
            self.sftp.remove(__local_file_name)
        sys.stdout.write("start uploading %s ... \n" % _local_file)
        sys.stdout.flush()
        self.sftp.put(_local_file, __local_file_name, callback=self.__upload_call_back)

    def upload_dir(self, _local_dir):
        if not os.path.isdir(_local_dir):
            sys.stdout.write("is not dir > %s ... \n" % _local_dir)
            sys.stdout.flush()
            return
        for _file in os.listdir(_local_dir):
            _local_file = os.path.join(_local_dir, _file)
            if os.path.isfile(_local_file):
                self.upload_file(_local_file)
            elif os.path.isdir(_local_file):
                try:
                    self.sftp.chdir(_file)
                except:
                    self.sftp.mkdir(_file)
                    self.sftp.chdir(_file)
                self.upload_dir(_local_file)
        self.sftp.chdir("..")

    def upload(self, _remote, _local, _delete=False):
        """上传文件
        上传本地到远端

        Args:
            _remote: 远端文件夹或者文件
            _local: 本地文件夹或者文件
            _delete: 是否删除需要上传的远端路径下的其他文件
        """
        _remote = _remote.replace("\\", "/")
        _local = _local.replace("\\", "/")
        sys.stdout.write("remote > %s ... \nlocal > %s\n" % (_remote, _local))
        sys.stdout.flush()

        self.__cwd(_remote, _delete)
        if os.path.isdir(_local):
            self.upload_dir(_local)
        if os.path.isfile(_local):
            self.upload_file(_local)
