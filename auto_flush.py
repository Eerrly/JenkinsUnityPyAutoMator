# -*- coding: UTF-8 -*-
import os
import time

import const
import util

_flush_type = ""
_file_path = None


def init_jenkins_params():
    util.console(" call Init Static Params start ".center(200, "#"))
    global _flush_type, _file_path
    _flush_type = os.environ["flush_type"]

    if _flush_type == "item":
        _file_path = os.environ["path"]

    util.console("path %s" % _file_path)
    util.console(" call Init Static Params end ".center(200, "#"))


def flush_node():
    util.console(" flush start ".center(200, "#"))
    __flush = util.init_cdn_flush(const.CDN_FLUSH_URL, const.CDN_FLUSH_HEADERS, const.CDN_FLUSH_USER, const.CDN_FLUSH_PASS, const.CDN_FLUSH_PAD, _file_path, const.CDN_FLUSH_EMAIL)
    __flush.flush()
    util.console(" flush end ".center(200, "#"))


def main_function():
    init_jenkins_params()
    flush_node()


if __name__ == "__main__":
    util.console((" start time : %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).center(200, "#"))
    main_function()
    util.console((" end time : %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).center(200, "#"))
