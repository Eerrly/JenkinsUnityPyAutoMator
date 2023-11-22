# -*- coding: UTF-8 -*-
import hashlib
import os
import re
import shutil
import time
import traceback

import const
import params
import util

jenkins_params = params.JenkinsClass
cdn_params = params.CDNClass
_local_directory_format = "{time}\\FreeStyle\\{version}"


def init_jenkins_params():
    """
    初始化自动化构建所需的各种参数
    """
    util.console(" call Init Static Params start ".center(200, "#"))
    global jenkins_params, cdn_params
    jenkins_params = params.JenkinsClass()
    cdn_params = params.CDNClass()
    util.console(" call Init Static Params end ".center(200, "#"))


def merger_patch():
    """
    合并热更成一个压缩包
    """
    util.console(" call merge patch start ".center(200, "#"))
    __unzip_files_dic = {}
    for __file_name in os.listdir(jenkins_params.WORKSPACE):
        __ret = re.match("Patch_(.*?).zip", __file_name)
        if __ret:
            __unzip_files_dic[str(__ret.group(1))] = util.unzip(os.path.join(jenkins_params.WORKSPACE, __file_name))
    if len(__unzip_files_dic) == 0:
        raise Exception("Missing patch files! Please Copy artifacts from Jenkins Task.")
    __local_base_dir = os.path.join(jenkins_params.WORKSPACE, jenkins_params.BUILD_NUMBER)
    __local_strtime = time.strftime("%Y%m%d%H%MJL2", time.localtime())
    __local_folder_path = os.path.join(__local_base_dir, _local_directory_format.format(time=__local_strtime, version=cdn_params.version))
    if os.path.exists(__local_folder_path):
        shutil.rmtree(__local_folder_path)
    os.makedirs(__local_folder_path)
    for key in __unzip_files_dic:
        util.move(__unzip_files_dic[key], os.path.join(__local_folder_path, key))
    __folder = os.path.join(__local_base_dir, __local_strtime)
    __zip_file = util.zip(__folder)
    __writer_error = False
    try:
        with open(os.path.join(__local_base_dir, os.path.basename(__zip_file)).replace(".zip", ".md5"), "w") as wf:
            __md5 = hashlib.md5(open(__zip_file, 'rb').read()).hexdigest()
            __base_file_name = os.path.basename(__zip_file)
            wf.write(__md5 + " " + __base_file_name)
            util.console("%s\t%s", __md5, __base_file_name)
    except Exception as e:
        __writer_error = True
        util.console("update zip md5 fail! > %s", repr(e))
    finally:
        shutil.rmtree(__folder)
        shutil.rmtree(__local_folder_path)
    if __writer_error:
        raise Exception("write md5 error !")
    util.console("%s\nmerge done!", __zip_file)
    util.console(" call merge patch end ".center(200, "#"))
    return __local_base_dir


def get_local_path():
    """
    获取本地需要上传的文件路径
    """
    __local = ""
    if const.UploadType[cdn_params.upload_type] == const.UploadType.Zip:
        __local = util.unzip(os.path.join(jenkins_params.WORKSPACE, "upload.zip"))
        util.console("select unzip file path:%s" % __local)
    elif const.UploadType[cdn_params.upload_type] == const.UploadType.Merger:
        __local = merger_patch()
        util.console("merge file path:%s" % __local)
    elif const.UploadType[cdn_params.upload_type] == const.UploadType.Main:
        __local = util.unzip(os.path.join(jenkins_params.WORKSPACE, "Main.zip"))
        util.console("unzip file path:%s", __local)
    elif const.UploadType[cdn_params.upload_type] == const.UploadType.Patch:
        __local = util.unzip(os.path.join(jenkins_params.WORKSPACE, "Patch_%s.zip" % cdn_params.channel))
        if cdn_params.patch_type == "":
            raise Exception("jenkins patch_type is empty but upload type is Patch!")
        for __file in os.listdir(__local):
            __path = os.path.join(__local, __file)
            if const.PatchType[cdn_params.patch_type] == const.PatchType.V and __file != "v.bytes":
                shutil.rmtree(__path) if os.path.isdir(__path) else os.remove(__path)
            elif const.PatchType[cdn_params.patch_type] == const.PatchType.WithoutV and __file == "v.bytes":
                os.remove(__path)
        util.console("unzip file path:%s", __local)
    else:
        raise Exception("upload2cdn patch_type is nil!")
    return __local


def get_remote_list():
    """
    获取远端上传的文件路径地址
    """
    __remote_list = []
    if cdn_params.upload_channel_list != "" and len(cdn_params.upload_channel_list.split("*")) > 0:
        if const.UploadType[cdn_params.upload_type] != const.UploadType.Main and const.UploadType[cdn_params.upload_type] != const.UploadType.Patch:
            raise Exception("Only whole package and hot change resources are supported")
        __channel_list = cdn_params.upload_channel_list.split("*")
        for __channel in __channel_list:
            if const.UploadType[cdn_params.upload_type] == const.UploadType.Main:
                __remote_list.append(cdn_params.remote_path + "/%s/Main/%s" % (cdn_params.version, __channel))
            elif const.UploadType[cdn_params.upload_type] == const.UploadType.Patch:
                __remote_list.append(cdn_params.remote_path + "/%s/%s" % (cdn_params.version, __channel))
    else:
        if const.UploadType[cdn_params.upload_type] == const.UploadType.Main:
            __remote_list.append(cdn_params.remote_path + "/%s/Main/%s" % (cdn_params.version, cdn_params.channel))
        elif const.UploadType[cdn_params.upload_type] == const.UploadType.Zip:
            __remote_list.append(cdn_params.remote_path + "/%s" % cdn_params.version)
        elif const.UploadType[cdn_params.upload_type] == const.UploadType.Patch:
            __remote_list.append(cdn_params.remote_path + "/%s/%s" % (cdn_params.version, cdn_params.channel))
        elif const.UploadType[cdn_params.upload_type] == const.UploadType.Merger:
            __remote_list.append(cdn_params.remote_path)

    if len(__remote_list) < 1:
        raise Exception("upload remote path is empty!")
    return __remote_list


def upload():
    """
    上传逻辑
    """
    util.console(" call upload assets to cdn start ".center(200, "#"))

    __local = get_local_path()
    __remote_list = get_remote_list()

    __host = cdn_params.cdn_address.split("*")[1]
    __port = "0" if len(cdn_params.cdn_address.split("*")) < 3 else cdn_params.cdn_address.split("*")[2]
    __username = cdn_params.account_information.split("*")[1]
    __password = cdn_params.account_information.split("*")[2]
    util.console("account_information:" + str(cdn_params.account_information))

    __ftp = None
    __upload_error = False
    try:
        # sftp port is 22
        if __port == "22":
            __ftp = util.init_ssh(__host, int(__port), __username, __password)
        else:
            __ftp = util.init_ftp(__host, int(__port), __username, __password, 0, const.CONST_FTP_BUF_SIZE)
    except Exception as e:
        util.console(u"Error : %s !" % repr(e))

    if __local is None or (not os.path.isfile(__local) and not os.path.isdir(__local)):
        util.console("local path is error!")
    elif __ftp is None:
        util.console("%s is None!", "sftp" if __port == "22" else "ftp")

    try:
        for __remote in __remote_list:
            __upload_error = False
            if __remote == "":
                util.console("remote_path is empty!")
            else:
                __ftp.upload(__remote, __local, cdn_params.delete_other)
            __ftp.cd("/root" if __port == "22" else "/")
    except Exception as e:
        __upload_error = True
        util.console(u"Error : %s !" % repr(e))
        util.console(u"Traceback format_exc : %s !" % traceback.format_exc())
    finally:
        if __ftp is not None:
            __ftp.quit()
    if __upload_error:
        raise Exception("upload error !")

    util.console(" call upload assets to cdn end ".center(200, "#"))


def main_function():
    """
    主函数
    """
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
