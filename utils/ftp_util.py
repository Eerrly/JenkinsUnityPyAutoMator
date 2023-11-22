# -*- coding: UTF-8 -*-
import ftplib
import os
import sys

_remote_size = 0
_total_size = 0


class FTPHelper:
    """ FTP 工具类 """
    def __init__(self, _host, _port, _user, _passwd, _debug_lv=0, _buf_size=1024 * 1024):
        self.buf_size = _buf_size
        self.host = _host
        self.port = _port
        self.user = _user
        self.passwd = _passwd
        self.debug_lv = _debug_lv
        self.ftp = ftplib.FTP()
        # self.ftp.set_pasv(0) # korea have to set pasv FALSE
        self.ftp.set_debuglevel(_debug_lv)
        self.ftp.connect(host=_host, port=_port)
        self.ftp.login(user=_user, passwd=_passwd)

    def __str__(self):
        return "ftp information >\nuser:%s\npasswd:******\nhost:%s\ndebug_lv:%d" % (self.user, self.host, self.debug_lv)

    def __exist_ftp_file(self, _remote_file, _remote_dir=None):
        """
        判断远端文件是否存在
        Args:
            _remote_file: 远端文件
            _remote_dir: 远端文件夹
        """
        try:
            if _remote_dir is not None:
                self.__cwd(_remote_dir, False)
            if _remote_file in self.ftp.nlst():
                return True
            else:
                return False
        except ftplib.error_perm:
            return False

    def __upload_callback(self, block):
        """
        上传回调
        Args:
            block: 上传的块
        """
        global _remote_size
        _remote_size = _remote_size + len(block)
        sys.stdout.write("uploading %.2f%% ... (%dkb)\n" % (float(_remote_size) / _total_size * 100, len(block) / 1024))
        sys.stdout.flush()

    def __cwd(self, _remote_path, _can_delete=False):
        """
        切换远端文件夹
        Args:
            _remote_path: 远端文件夹
            _can_delete: 是否删除需要上传的远端路径下的其他文件
        """
        _dir_list = _remote_path.split("/")
        index = 0
        while index < len(_dir_list):
            sys.stdout.write("cwd %s ...\n" % _dir_list[index])
            sys.stdout.flush()
            try:
                self.ftp.cwd(_dir_list[index])
                index = index + 1
            except:  # can't use 'Exception' in this
                self.ftp.mkd(_dir_list[index])
                self.ftp.cwd(_dir_list[index])
                index = index + 1
        if _can_delete:
            sys.stdout.write("'_can_delete' is True, start delete .\n")
            sys.stdout.flush()
            self.del_dir()

    def __del_file(self, _f):
        """
        删除远端文件
        Args:
            _f: 远端文件
        """
        sys.stdout.write(">[-] %s ... \n" % _f)
        sys.stdout.flush()
        self.ftp.delete(_f)

    def cd(self, _path):
        """
        切换远端文件夹
        Args:
            _path: 远端文件夹
        """
        self.ftp.cwd(_path)

    def quit(self):
        """
        退出FTP
        """
        self.ftp.quit()

    def upload_file(self, _local_file, _f):
        """
        上传文件
        Args:
            _local_file: 本地文件
            _f: 本地文件流
        """
        if not os.path.isfile(_local_file):
            sys.stdout.write("is not file > %s ... \n" % _local_file)
            sys.stdout.flush()
            return
        __local_file_name = os.path.basename(_local_file)
        if self.__exist_ftp_file(__local_file_name):
            sys.stdout.write("exist file and delete file > %s ... \n" % __local_file_name)
            sys.stdout.flush()
            self.ftp.delete(__local_file_name)
        sys.stdout.write("start uploading %s ... \n" % _local_file)
        sys.stdout.flush()
        global _total_size
        _total_size = os.path.getsize(_local_file)
        result = self.ftp.storbinary("STOR %s" % __local_file_name, _f, blocksize=self.buf_size, callback=self.__upload_callback)
        if result.find("226") == -1:
            raise Exception("upload %s error !\n" % __local_file_name)

    def del_dir(self):
        """
        删除远端文件夹
        """
        for _f in self.ftp.nlst():
            try:
                self.ftp.cwd(_f)
                self.del_dir()
                self.ftp.cwd("..")
                sys.stdout.write("[-] %s ... \n" % _f)
                sys.stdout.flush()
                self.ftp.rmd(_f)
            except:
                self.__del_file(_f)

    def upload_dir(self, _local_dir):
        """
        上传文件夹
        Args:
            _local_dir: 本地文件夹
        """
        if not os.path.isdir(_local_dir):
            sys.stdout.write("is not dir > %s ... \n" % _local_dir)
            sys.stdout.flush()
            return
        for _file in os.listdir(_local_dir):
            _local_file = os.path.join(_local_dir, _file)
            if os.path.isfile(_local_file):
                f = open(_local_file, "rb")
                self.upload_file(_local_file, f)
                f.close()
            elif os.path.isdir(_local_file):
                try:
                    self.ftp.cwd(_file)
                except:
                    self.ftp.mkd(_file)
                    self.ftp.cwd(_file)
                self.upload_dir(_local_file)
        self.ftp.cwd("..")

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
            f = open(_local, "rb")
            self.upload_file(_local, f)
            f.close()
