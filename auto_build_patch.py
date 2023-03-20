# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import time
import const
import params
import util

localBuildTime = -1.0
jenkins_params = params.JenkinsClass
path_params = params.PathClass
patch_params = params.PatchClass
sys_params = params.SystemClass


def init_jenkins_params():
    util.console(" call Init Static Params start ".center(200, "#"))
    global jenkins_params, path_params, patch_params, sys_params
    jenkins_params = params.JenkinsClass()
    sys_params = params.SystemClass(sys.argv)
    if not os.path.exists(sys_params.UNITY_EXE) or not os.path.exists(sys_params.UNITY_PROJECT):
        raise Exception("[%s] or [%s] path can not found!" % (sys_params.UNITY_EXE, sys_params.UNITY_PROJECT))
    path_params = params.PathClass(sys_params.UNITY_EXE, sys_params.UNITY_PROJECT)
    patch_params = params.PatchClass()
    util.console(" call Init Static Params end ".center(200, "#"))


def auto_build_patch():
    util.console(" auto unity build patch start ".center(200, "#"))

    time.sleep(10)
    _executeMethodName = "AutoBuild.AutoBuildPatch"

    _paramInfo = ""
    if patch_params.empty_patch == "true":
        _paramInfo = ""
    elif patch_params.patch_version != "":
        _paramInfo = "{patch_version}+{version}".format(patch_version=patch_params.patch_version, version=patch_params.version)
    elif patch_params.start_svn_version != "" and patch_params.end_svn_version != "":
        _paramInfo = "{start_svn_version}-{end_svn_version}+{version}".format(start_svn_version=patch_params.start_svn_version, end_svn_version=patch_params.end_svn_version, version=patch_params.version)
    else:
        raise Exception("not empty patch but svn version is null !")

    util.console("paramInfo : %s ", _paramInfo)

    open(path_params.UNITY_LOG_PATH, 'w').close()
    __tail = util.init_tail(path_params.UNITY_LOG_PATH)
    __tail.start()

    __unity = util.init_unity(sys_params, path_params.UNITY_LOG_PATH, const.Build[patch_params.platform])
    # Self-Unity-Platform Switching
    __unity.switch()

    global localBuildTime
    localBuildTime = time.time()

    __unity.execute(_executeMethodName, _paramInfo, patch_params.no_safe_fast)
    __tail.stop()

    util.console(" auto unity build patch end ".center(200, "#"))


def update_unity_project():
    util.console(" svn clean revert update start ".center(200, "#"))
    __svn = util.init_svn(const.CONST_SVN_USERNAME, const.CONST_SVN_PASSWORD, path_params.PROJECT_PATH, path_params.CLEAN_PATH)
    __svn.clean_revert_update()
    util.console(" svn clean revert update end ".center(200, "#"))


def init_svn_diff_txt():
    util.console(" call svn diff start ".center(200, "#"))
    _svnDiffTxtPath = "{project_path}\\Client\\OutSVNDiff.txt".format(project_path=path_params.PROJECT_PATH)
    _svnDiffTxtFile = open(_svnDiffTxtPath, 'w')
    __svn = util.init_svn(const.CONST_SVN_USERNAME, const.CONST_SVN_PASSWORD, path_params.PROJECT_PATH, path_params.CLEAN_PATH)
    __svn.diff(patch_params.start_svn_version, patch_params.end_svn_version, _svnDiffTxtFile)
    _svnDiffTxtFile.close()
    util.console(" call svn diff end ".center(200, "#"))


def copy_patch_zip_to_artifact():
    util.console(" copy Patch_*.zip to artifact start ".center(200, "#"))
    jenkins_targetPath = os.path.join(jenkins_params.JENKINS_HOME, "workspace\\%s" % jenkins_params.JOB_NAME)

    file_lists = os.listdir(path_params.PATCH_PATH)
    file_lists.sort(key=lambda fn: os.path.getmtime(path_params.PATCH_PATH + "\\" + fn) if not os.path.isdir(path_params.PATCH_PATH + "\\" + fn) else 0)
    __copy_path = os.path.join(jenkins_targetPath, "Patch_%s.zip" % patch_params.channel)
    if os.path.exists(__copy_path):
        os.remove(__copy_path)

    __patch_path = os.path.join(path_params.PATCH_PATH, file_lists[-1])
    __output_time = os.path.getmtime(__patch_path)
    if localBuildTime < 0 or localBuildTime > __output_time:
        raise Exception("unity build or output error!")
    util.console("src_path:%s, copy_path:%s" % (__patch_path, __copy_path))
    shutil.copyfile(__patch_path, __copy_path)
    util.console(" copy Patch_*.zip to artifact end ".center(200, "#"))


def main_function():
    init_jenkins_params()
    if util.get_free_space_mb("C:\\") < const.WIN_MAX_DISK:
        raise Exception("No space left c: disk!")
    if patch_params.clean_update_project == "true":
        update_unity_project()
    if patch_params.empty_patch == "false":
        init_svn_diff_txt()
    auto_build_patch()
    copy_patch_zip_to_artifact()


if __name__ == "__main__":
    util.console((" start time : %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).center(200, "#"))
    main_function()
    util.console((" end time : %s " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).center(200, "#"))
