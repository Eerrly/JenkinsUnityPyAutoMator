# -*- coding: UTF-8 -*-

import io
import os
import re
import shutil
import sys
import time

import const
import params
import util

IOS_TOOLS_PATH = ""
SHARE_PATH = ""
jenkins_params = params.JenkinsClass
xcode_params = params.XCodeClass


def __get_entitlements(__xcode_project_path):
    """
    获取Xcode Entitlements文件
    Args:
        __xcode_project_path: Xcode工程路径
    """
    __project_pbx = os.path.join(__xcode_project_path, "Unity-iPhone.xcodeproj/project.pbxproj")
    __entitlements = ""
    with io.open(__project_pbx, 'r', encoding='utf-8') as rf:
        __entitlements = re.findall(r"CODE_SIGN_ENTITLEMENTS = (.+?);", rf.read())[0].replace("\"", "")
    return os.path.join(__xcode_project_path, __entitlements)


def __chmod(__file, __permission=0o777):
    """
    调用Linux命令行的chmod命令
    Args:
        __file: 需要赋予权限的文件
        __permission: 读写权限
    Returns:
        是否存在这个文件
    """
    util.console("chmod '%s'", __file)
    if os.path.exists(__file):
        os.chmod(__file, __permission)
        return True
    else:
        util.console("%s not found!", __file)
    return False


def __check_path_exists(__path):
    """
    检测文件路径是否存在
    Args:
        __path: 文件路径
    Returns:
        文件路径是否存在
    """
    if not os.path.exists(__path):
        raise Exception("'%s' can not found!", __path)
    return True


def init_jenkins_params():
    """
    初始化自动化构建所需的各种参数
    """
    util.console(" call Init Static Params start ".center(200, "#"))

    global IOS_TOOLS_PATH, SHARE_PATH, jenkins_params, xcode_params
    IOS_TOOLS_PATH = sys.argv[1]
    __check_path_exists(IOS_TOOLS_PATH)
    SHARE_PATH = sys.argv[2]
    __check_path_exists(SHARE_PATH)
    util.console("IOS_TOOLS_PATH:%s,SHARE_PATH:%s", IOS_TOOLS_PATH, SHARE_PATH)

    jenkins_params = params.JenkinsClass()
    xcode_params = params.XCodeClass()
    util.console(" call Init Static Params end ".center(200, "#"))


# def update_ios_project():
#     util.console(" svn clean revert update start ".center(200, "#"))
#     __svn = util.init_svn(const.CONST_SVN_USERNAME, const.CONST_SVN_PASSWORD, IOS_TOOLS_PATH)
#     __svn.update()
#     util.console(" svn clean revert update end ".center(200, "#"))


def modify_xcode_project(__xcode, __xcode_project_path):
    """
    修改Xcode的设置与参数
    Args:
        __xcode: xcode_util对象
        __xcode_project_path: Xcode工程路径
    """
    # Change ShortVersion And Version
    if xcode_params.xcode_version_build != "" and len(xcode_params.xcode_version_build.split("*")) == 2:
        __xcode.PlistBuddyShortVersion(xcode_params.xcode_version_build.split("*")[0])
        __xcode.PlistBuddyVersion(xcode_params.xcode_version_build.split("*")[1])

    # Add or Del AppleSign to entitlements
    if xcode_params.enable_apple_sign != "":
        __entitlements_path = __get_entitlements(__xcode_project_path)
        util.console("xcode entitlements path : %s", __entitlements_path)
        __check_path_exists(__entitlements_path)
        __re_applesign = io.open(__entitlements_path, 'r', encoding='utf-8').read().find("com.apple.developer.applesignin") != -1
        if xcode_params.enable_apple_sign == "true" and not __re_applesign:
            __xcode.PlistBuddyAddAppleSign(__entitlements_path)
        elif xcode_params.enable_apple_sign == "false" and __re_applesign:
            __xcode.PlistBuddyDelAppleSign(__entitlements_path)
        else:
            util.console("no need modify apple sign in > enable_apple_sign:%s, __re_applesign:%s", xcode_params.enable_apple_sign, str(__re_applesign))


def export_ipa_callback(__xcode, __xcode_project_path, __archivePath):
    """
    导出Ipa之后的操作处理
    Args:
        __xcode: xcode_util对象
        __xcode_project_path: Xcode工程路径
        __archivePath: Xcode工程archive的目标路径
    """
    # upload firebase dsym file
    __firebaseCrashlytics = os.path.join(
        __xcode_project_path,
        "Frameworks/Plugins/iOS/ThirdPartyImport/Firebase/FirebaseCrashlytics/upload-symbols"
    )
    if xcode_params.upload_symbols == "true" and __chmod(__firebaseCrashlytics):
        __vpn = None
        __vpn_state = None
        try:
            __vpn = util.init_vpn(const.CONST_VPN_NAME, const.CONST_VPN_USERNAME, const.CONST_SVN_PASSWORD, const.CONST_VPN_SECRET)
            util.console("open vpn '%s' ...", const.CONST_VPN_NAME)
            __vpn.start()
            __vpn_state = 1
        finally:
            util.console("open vpn '%s' failed ! ", const.CONST_VPN_NAME)
        if __vpn_state is not None:
            time.sleep(10)
        try:
            util.console("uploading firebase dsym file ...")
            __dsymPath = os.path.join(__archivePath, "dSYMs")
            __dsymFile = os.path.join(__dsymPath, os.listdir(__dsymPath)[0]).replace(" ", "\\ ")
            __googleServiceInfoFile = os.path.join(__xcode_project_path, "GoogleService-Info.plist")
            __check_path_exists(__googleServiceInfoFile)
            __xcode.UploadDsym(__firebaseCrashlytics, __googleServiceInfoFile, __dsymFile)
            util.console("uploading firebase dsym file successful !")
        except Exception as e:
            util.console(u"upload firebase dsym file failed : %s !" % repr(e))
        finally:
            if __vpn is not None and __vpn_state is not None:
                util.console("close vpn '%s' ...", const.CONST_VPN_NAME)
                __vpn.stop()


def xcode_build():
    """
    Xcode构建逻辑
    """
    util.console(" call xcode build start ".center(200, "#"))

    __xcode_project_path = util.unzip(os.path.join(jenkins_params.WORKSPACE, "IOSBuild.zip"))

    __build_path = os.path.join(__xcode_project_path, "build")
    if os.path.exists(__build_path):
        shutil.rmtree(__build_path)

    __chmod(os.path.join(__xcode_project_path, "MapFileParser.sh"))

    __iconPath = os.path.join(IOS_TOOLS_PATH, "icon")
    if os.path.exists(__iconPath):
        __appiconset = os.path.join(__xcode_project_path, "Unity-iPhone/Images.xcassets/AppIcon.appiconset")
        util.console("copy icon to %s" % __appiconset)
        util.move(__iconPath, __appiconset)

    __xcode = util.init_xcode(__xcode_project_path)
    __xcode.Clean()

    modify_xcode_project(__xcode, __xcode_project_path)

    __archivePath = os.path.join(jenkins_params.WORKSPACE, "xcode_archive_{build_number}.xcarchive".format(build_number=jenkins_params.BUILD_NUMBER))
    if os.path.exists(__archivePath):
        shutil.rmtree(__archivePath)  # .xcarchive is a dir

    if xcode_params.automatic == "true":
        __xcode.ArchiveAutomatic(xcode_params.buildType, __archivePath)
    elif xcode_params.bundle_identifier != "":
        __xcode.SedBundleIdentifierAndArchive(xcode_params.bundle_identifier, xcode_params.buildType, __archivePath, xcode_params.CODE_SIGN_IDENTITY, xcode_params.PROVISIONING_PROFILE, xcode_params.DEVELOPMENT_TEAM, xcode_params.APP)
    else:
        __xcode.Archive(xcode_params.buildType, __archivePath, xcode_params.CODE_SIGN_IDENTITY, xcode_params.PROVISIONING_PROFILE, xcode_params.DEVELOPMENT_TEAM, xcode_params.APP)

    __exportPath = os.path.join(jenkins_params.WORKSPACE, "app-%s.ipa" % xcode_params.buildType)
    __export_options_plist = os.path.join(IOS_TOOLS_PATH, "exportOptionPlist/%s.plist" % xcode_params.export_options_plist_name)

    __xcode.Export(__archivePath, __exportPath, __export_options_plist)

    export_ipa_callback(__xcode, __xcode_project_path, __archivePath)
    util.console(" call xcode build end ".center(200, "#"))


def copy_outputs_to_share():
    """
    将导出的ipa拷贝到共享文件夹中
    """
    util.console(" copy ipa to output start ".center(200, "#"))
    # copy outputs to share dir
    __outputs = os.path.join(jenkins_params.WORKSPACE, "app-%s.ipa" % xcode_params.buildType)
    __copy_path = os.path.join(SHARE_PATH, "%s/%s" % (jenkins_params.JOB_NAME, jenkins_params.BUILD_NUMBER))
    util.move(__outputs, __copy_path)
    util.console(" copy ipa to output end ".center(200, "#"))


def main_function():
    """
    主函数
    """
    init_jenkins_params()
    if os.path.exists("/Users/lmd/Library/Developer/Xcode/DerivedData") and util.get_free_space_mb("/Users/lmd/Library/Developer/Xcode/DerivedData") < const.MAC_MAX_DISK:
        raise Exception("No space left /Users/lmd/Library/Developer/Xcode/DerivedData!")
    elif os.path.exists("/Users/yangxiaochun/Library/Developer/Xcode/DerivedData") and util.get_free_space_mb("/Users/yangxiaochun/Library/Developer/Xcode/DerivedData") < const.MAC_MAX_DISK:
        raise Exception("No space left /Users/yangxiaochun/Library/Developer/Xcode/DerivedData!")
    # IOS_Tools only as a local folder
    # update_ios_project()
    xcode_build()
    copy_outputs_to_share()


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
