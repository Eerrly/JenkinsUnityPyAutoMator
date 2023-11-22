# -*- coding: UTF-8 -*-
import os
import io
import sys
import time
from threading import Thread
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


class TailHelper(Thread):
    """
    Trail工具类
    """
    def __init__(self, filename):
        """
        初始化Trail工具类
        Args:
            filename: 文件名
        """
        open(filename, 'w').close()  # clear txt
        self._filename = filename
        self._stop_reading = False
        Thread.__init__(self)

    def __str__(self):
        return "tail information >\n_filename:%s" % self._filename

    def run(self):
        """
        执行方法
        """
        while not os.path.exists(self._filename):
            time.sleep(0.1)
        file = self.open_default_encoding(self._filename, mode='r')
        while not self._stop_reading:
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(1)
                file.seek(where)
            else:
                sys.stdout.write(str(line.rstrip()) + '\n')
                sys.stdout.flush()

    def stop(self):
        """
        停止
        """
        self._stop_reading = True
        self.join(5)

    @staticmethod
    def open_default_encoding(file, mode):
        return open(file, mode=mode, encoding='utf-8-sig')
