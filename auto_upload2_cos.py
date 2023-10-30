# -*- coding: UTF-8 -*-
import os
import re
import shutil
import time
import traceback

import params
import util

jenkins_params = params.JenkinsClass
cos_params = params.COSClass
_local_directory_format = "{time}\\FreeStyle\\{version}"


def init_jenkins_params():
    util.console(" call Init Static Params start ".center(200, "#"))
    global jenkins_params, cos_params
    jenkins_params = params.JenkinsClass()
    cos_params = params.COSClass()
    util.console(" call Init Static Params end ".center(200, "#"))


def merger_patch():
    util.console(" call merge patch start ".center(200, "#"))
    __unzip_files_dic = {}
    for __file_name in os.listdir(jenkins_params.WORKSPACE):
        __ret = re.match("Patch_(.*?).zip", __file_name)
        if __ret:
            __path = os.path.join(jenkins_params.WORKSPACE, __file_name)
            util.console("%s > [size : %s]", __file_name, str(util.get_file_size(__path)))
            __unzip_files_dic[str(__ret.group(1))] = util.unzip(__path)
    if len(__unzip_files_dic) == 0:
        raise Exception("Missing patch files! Please Copy artifacts from Jenkins Task.")
    __local_base_dir = os.path.join(jenkins_params.WORKSPACE, jenkins_params.BUILD_NUMBER)
    __local_strtime = time.strftime("%Y%m%d%H%MJL2", time.localtime())
    __local_folder_path = os.path.join(__local_base_dir, _local_directory_format.format(time=__local_strtime, version=cos_params.version))
    if os.path.exists(__local_folder_path):
        shutil.rmtree(__local_folder_path)
    os.makedirs(__local_folder_path)
    for key in __unzip_files_dic:
        util.move(__unzip_files_dic[key], os.path.join(__local_folder_path, key))
    __folder = os.path.join(__local_base_dir, __local_strtime)
    __zip_file = util.zip(__folder)
    shutil.rmtree(__folder)
    shutil.rmtree(__local_folder_path)
    __local = os.path.join(__local_base_dir, os.path.basename(__zip_file))
    util.console("%s\nmerge done!", __local)
    util.console(" call merge patch end ".center(200, "#"))
    return __local


def get_local_path():
    __local = merger_patch()
    util.console("merge file path:%s" % __local)
    return __local


def get_remote_list():
    __remote_list = []
    __remote_list.append(cos_params.remote_path)
    if len(__remote_list) < 1:
        raise Exception("upload remote path is empty!")
    return __remote_list


def upload():
    util.console(" call upload assets to cdn start ".center(200, "#"))
    __local = get_local_path()
    __remote_list = get_remote_list()

    __cos = None
    __upload_error = False
    try:
        __cos = util.init_cos(cos_params.secretId, cos_params.secretKey, cos_params.bucket, cos_params.region)
        __cos.config()
    except Exception as e:
        util.console(u"Error : %s !" % repr(e))

    if __local is None or (not os.path.isfile(__local) and not os.path.isdir(__local)):
        util.console("local path is error!")

    try:
        for __remote in __remote_list:
            __upload_error = False
            if __remote == "":
                util.console("remote_path is empty!")
            else:
                __cos.upload(__local, __remote)
    except Exception as e:
        __upload_error = True
        util.console(u"Error : %s !" % repr(e))
        util.console(u"Traceback format_exc : %s !" % traceback.format_exc())

    if __upload_error:
        raise Exception("upload error !")
    util.console(" call upload assets to cdn end ".center(200, "#"))


def main_function():
    init_jenkins_params()
    upload()


if __name__ == "__main__":
    util.console((" start time : %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).center(200, "#"))
    ERROR_LEVEL = 0
    try:
        main_function()
    except Exception as e:
        util.console(u"Error : %s !" % repr(e))
        ERROR_LEVEL = 1
    util.console((" end time : %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).center(200, "#"))
    exit(ERROR_LEVEL)