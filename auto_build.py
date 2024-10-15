# -*- coding: UTF-8 -*-

import os
import re
import shutil
import sys
import time
from enum import Enum

import const
import params
import util


# -buildTarget Android, Linux, Linux64, LinuxUniversal, N3DS, OSXUniversal, PS4, PSM, PSP2, Switch, Tizen, Web, WebGL, WebStreamed, WiiU, Win, Win64, WindowsStoreApps, XboxOne, iOS, tvOS
class Platform(Enum):
    Android = "Android",
    PC = "Win",
    IOS = "iOS",


localBuildTime = -1.0  # Use the file modification time to judge whether the export was successful
platform = []  # Platform.Android
jenkins_params = params.JenkinsClass
unity_params = params.UnityClass
build_params = params.BuildClass
path_params = params.PathClass
sys_params = params.SystemClass


def svn_clean_revert_update():
    """
    SVN清理、还原、更新操作
    """
    util.console(" svn clean revert update start ".center(200, "#"))
    if build_params.disableSvnUpdateCleanUnityProject == "true":
        util.console(">>> skip svn clean revert update.")
    else:
        __svn = util.init_svn(const.CONST_SVN_USERNAME, const.CONST_SVN_PASSWORD, path_params.PROJECT_PATH, path_params.CLEAN_PATH)
        __svn.clean_revert_update()
    util.console(" svn clean revert update end ".center(200, "#"))


def init_jenkins_params():
    """
    初始化自动化构建所需的各种参数
    """
    util.console(" call init jenkins params start ".center(200, "#"))

    global platform, jenkins_params, build_params, unity_params, path_params, sys_params
    jenkins_params = params.JenkinsClass()
    build_params = params.BuildClass()
    unity_params = params.UnityClass()
    sys_params = params.SystemClass(sys.argv)
    if not os.path.exists(sys_params.UNITY_EXE) or not os.path.exists(sys_params.UNITY_PROJECT):
        raise Exception("[%s] or [%s] path can not found!" % (sys_params.UNITY_EXE, sys_params.UNITY_PROJECT))
    __android_studio_path = "%s\\Android%s" % (sys_params.UNITY_PROJECT, ("_%s" % build_params.androidChannel) if build_params.androidChannel != "" else build_params.androidChannel)
    __build_gradle_path = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __build_gradle_path = os.path.join(__android_studio_path, "launcher\\build.gradle")
    else:
        __build_gradle_path = None if build_params.enableAndroidAppBundle == "true" else ("%s\\%s" % (__android_studio_path, "build.gradle"))
    util.console("[directory structure has changed] build_gradle_path:%s", __build_gradle_path)

    path_params = params.PathClass(sys_params.UNITY_EXE, sys_params.UNITY_PROJECT, __android_studio_path, __build_gradle_path)
    __platform_dic = {"PC": Platform.PC, "Android": Platform.Android, "IOS": Platform.IOS}
    platform = __platform_dic[build_params.buildTarget]

    util.console(" call init jenkins params end ".center(200, "#"))


def auto_build():
    """
    Unity构建逻辑
    """
    util.console(" unity auto build start ".center(200, "#"))
    _executeMethodName = "AutoBuild.AutoBuildPackage"

    _n_param_list = ["enableGM=" + unity_params.enableGM, "enableGuide=" + unity_params.enableGuide, "loginServer=" + unity_params.loginServer, "enableFPS=" + unity_params.enableFPS,
                     "enableConsole=" + unity_params.enableConsole, "enableLog=" + unity_params.enableLog, "enableBuildResources=" + unity_params.enableBuildResources]
    _o_param_list = None
    if platform == Platform.Android or platform == Platform.IOS:
        _o_param_list = ["enableSDK=" + unity_params.enableSDK, "enablePatching=" + unity_params.enablePatching, "enableQAServerCDN=" + unity_params.enableQAServerCDN]
    else:
        _o_param_list = ["isAuthenticationServer=" + unity_params.isAuthenticationServer]
    _n_param_list.extend(_o_param_list)

    # TW channel MyCard
    if build_params.channel == "tw":
        _n_param_list.extend(["androidChannel=" + build_params.androidChannel])

    _paramInfo = "+".join(_n_param_list)
    util.console("unity launcher params : %s", _paramInfo)

    __tail = util.init_tail(path_params.UNITY_LOG_PATH)
    __tail.start()

    __unity = util.init_unity(sys_params, path_params.UNITY_LOG_PATH, const.Build[build_params.buildTarget])
    # Self-Unity-Platform Switching
    # __unity.switch()

    global localBuildTime
    localBuildTime = time.time()

    __unity.execute(_executeMethodName, _paramInfo)

    __tail.stop()
    util.console(" unity auto build end ".center(200, "#"))


def __copy_to_artifact_path(_zip_file):
    """
    拷贝压缩包到Jenkins存档文件夹中
    Args:
        _zip_file: 压缩文件路径
    """
    util.console("jenkins_target_path : " + jenkins_params.WORKSPACE + ", _zip_file : " + _zip_file)
    __copy_path = os.path.join(jenkins_params.WORKSPACE, os.path.basename(_zip_file))
    util.move(_zip_file, __copy_path)


def copy_main_zip_to_artifact():
    """
    拷贝主资源压缩包到Jenkins存档文件夹中
    """
    util.console(" copy main.zip to artifact start ".center(200, "#"))
    __copy_to_artifact_path(path_params.MAIN_ZIP_PATH)
    util.console(" copy main.zip to artifact end ".center(200, "#"))


def copy_windows_exe_to_share():
    """
    拷贝WindowExe程序到共享文件夹中
    """
    util.console(" copy windows exe to share start ".center(200, "#"))
    __desktop_Path = os.path.join(os.path.expanduser("~"), 'Desktop')
    __outputs_path = os.path.join(path_params.PROJECT_PATH, "output")
    __output_time = os.path.getmtime(__outputs_path)
    if localBuildTime < 0 or localBuildTime > __output_time:
        raise Exception("unity build or output error!")

    # sort by modify time
    __file_lists = os.listdir(__outputs_path)
    __file_lists.sort(key=lambda fn: os.path.getmtime(__outputs_path + "\\" + fn) if not os.path.isdir(__outputs_path + "\\" + fn) else 0)
    __zip_file = os.path.join(__outputs_path, __file_lists[-1])

    __share_path = os.path.join("ShareSoftware\\EXE_OutPut\\", "%s\\%s" % (jenkins_params.JOB_NAME, jenkins_params.BUILD_NUMBER))
    # share the zip for windows package to shared folder and jenkins workspace
    util.move(__zip_file, os.path.join(__desktop_Path, __share_path, __file_lists[-1]))
    util.move(__zip_file, os.path.join(jenkins_params.WORKSPACE, "PC.zip"))

    util.console(" copy windows exe to share end ".center(200, "#"))


def copy_android_apk_to_share():
    """
    拷贝AndroidApk到共享文件夹中
    """
    util.console(" copy android apk to share start ".center(200, "#"))
    # copy outputs to share dir
    __desktop_Path = os.path.join(os.path.expanduser("~"), 'Desktop')
    __copy_path = os.path.join("ShareSoftware\\APK_OutPut\\", "%s\\%s\\" % (jenkins_params.JOB_NAME, jenkins_params.BUILD_NUMBER))
    __android_outputs_path = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __android_outputs_path = os.path.join(path_params.ANDROID_LAUNCHER_PATH, "build\\outputs")
    else:
        __android_studio_root_path = path_params.ANDROID_APP_PATH if build_params.enableAndroidAppBundle == "true" else path_params.ANDROID_STUDIO_PATH
        __android_outputs_path = os.path.join(__android_studio_root_path, "build\\outputs")
    util.console("[directory structure has changed] android_outputs_path:%s", __android_outputs_path)
    util.move(__android_outputs_path, os.path.join(__desktop_Path, __copy_path))
    # share dir link
    __ip_address = "\\\\192.168.16.191\\" if build_params.channel == "cn" else "\\\\192.168.16.166\\"
    __output_file_address = (__ip_address + __copy_path).replace("\\", "/")
    util.console("open shared output folder >>>\nfile:%s", __output_file_address)
    util.console(" copy android apk to share end ".center(200, "#"))


def replace_android_studio_assets():
    """
    替换Android工程内的文件
    """
    util.console(" replace android studio assets start ".center(200, "#"))
    __output_path = os.path.join(path_params.PROJECT_PATH, "output")
    __output_time = os.path.getmtime(__output_path)
    if build_params.startBuildingDirectly == "true" and (localBuildTime < 0 or localBuildTime > __output_time):
        raise Exception("unity build or output error!")

    __unity_replace_files = ["assets", "jniLibs", "res"]
    __bundle_moveto_split_files = ["ABMain.s", "ABMainMD5.txt"]

    # '...\src\main\' or '...\unityLibrary\src\main\'
    __unity_android_main_dir = ""
    __unity_output_main_dir = ""
    # ...\launcher\src\main\res\
    __launcher_android_res_dir = ""
    __launcher_output_res_dir = ""

    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __unity_android_main_dir = os.path.join(path_params.ANDROID_UNITYLIBRARY_PATH, "src\\main")
        __unity_output_main_dir = os.path.join(path_params.PROJECT_PATH, "output\\unityLibrary\\src\\main")
        __launcher_android_res_dir = os.path.join(path_params.ANDROID_LAUNCHER_PATH, "src\\main\\res")
        __launcher_output_res_dir = os.path.join(path_params.PROJECT_PATH, "output\\launcher\\src\\main\\res")
    else:
        __android_studio_root_path = path_params.ANDROID_APP_PATH if build_params.enableAndroidAppBundle == "true" else path_params.ANDROID_STUDIO_PATH
        __unity_android_main_dir = os.path.join(__android_studio_root_path, "src\\main")
        __unity_output_main_dir = os.path.join(path_params.PROJECT_PATH, "output\\jielan2\\src\\main")
    util.console("[directory structure has changed] unity_android_main_dir:%s, unity_output_main_dir:%s", __unity_android_main_dir, __unity_output_main_dir)

    # '...\src\main\assets\Bundle'
    __unity_android_bundle_dir = os.path.join(__unity_android_main_dir, "assets\\Bundle")

    # Replace launcher res's assets
    if __launcher_android_res_dir != "" and __launcher_output_res_dir != "":
        util.move(__launcher_output_res_dir, __launcher_android_res_dir)

    # Replace unity main's assets
    for __file_name in __unity_replace_files:
        __src_path = os.path.join(__unity_output_main_dir, "{file_name}".format(file_name=__file_name))
        __dst_path = os.path.join(__unity_android_main_dir, "{file_name}".format(file_name=__file_name))
        util.move(__src_path, __dst_path)
    # Remove assets that need to be downloaded
    for __file_name in os.listdir(__unity_android_bundle_dir):
        if __file_name.endswith(".mp4") or __file_name == "HUMain.s" or __file_name == "HUMainMD5.txt":
            os.remove(os.path.join(__unity_android_bundle_dir, __file_name))
    # Only androidappbundle need to migrate assets
    if build_params.enableAndroidAppBundle == "true":
        for __file_name in __bundle_moveto_split_files:
            __src_path = os.path.join(__unity_android_bundle_dir, "{file_name}".format(file_name=__file_name))
            __dst_path = os.path.join(path_params.INSTALL_TIME_ASSET_PACK_PATH, "src\\main\\assets\\Bundle\\{file_name}".format(file_name=__file_name))
            if os.path.exists(__src_path):
                util.move(__src_path, __dst_path)
                os.remove(__src_path)

    special_treatment_for_each_channel_in_android()

    util.console(" replace android studio assets end ".center(200, "#"))


def __replace_android_icon(__launcher_main_path):
    """
    替换Android工程内的Icon
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
    """
    __android_res_path = os.path.join(__launcher_main_path, "res")
    __icon_path = os.path.join(path_params.PROJECT_PATH, "Android_Tools\\icon")
    __icon_channel_path = os.path.join(path_params.PROJECT_PATH, "Android_Tools\\icon_%s", build_params.androidChannel)
    if os.path.exists(__icon_path):
        util.move(__icon_path, __android_res_path, True)
    elif os.path.exists(__icon_channel_path):
        util.move(__icon_channel_path, __android_res_path, True)


def __modify_android_version():
    """
    修改Android工程里的AndroidVersion
    """
    if build_params.androidVersion != "" and len(build_params.androidVersion.split("*")) == 2:
        __version_code = build_params.androidVersion.split("*")[0]
        __version_name = build_params.androidVersion.split("*")[1]
        with open(path_params.BUILD_GRADLE_PATH, 'r+', encoding='utf-8') as rwf:
            __new_text = re.sub(r"versionCode (\d+)", "versionCode %s" % __version_code, rwf.read())
            __new_text = re.sub(r"versionName '(\d+.\d+.\d+)'", "versionName '%s'" % __version_name, __new_text)
            rwf.seek(0)
            rwf.write(__new_text)
        util.console("set android build.gradle versionCode: %s, versionName: %s", __version_code, __version_name)


def __replace_branch_kr(__launcher_main_path, __unitylibrary_main_path):
    """
    韩服渠道的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __replace_android_icon(__launcher_main_path)
    __unity_main_path = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __unity_main_path = __unitylibrary_main_path
    else:
        __unity_main_path = __launcher_main_path
    util.console("[directory structure has changed] unity_main_pat:%s", __unity_main_path)

    __android_assets_path = os.path.join(__unity_main_path, "assets")
    __android_res_path = os.path.join(__unity_main_path, "res")

    __cy_platform_json = "Android_Tools\\CYPlatform_%s.json" % build_params.androidChannel
    platformJsonPath = os.path.join(path_params.PROJECT_PATH, __cy_platform_json)
    androidStudioPlatformJsonPath = os.path.join(__android_assets_path, "CYPlatform.json")
    util.move(platformJsonPath, androidStudioPlatformJsonPath)

    stringXmlPath = os.path.join(path_params.PROJECT_PATH, "Android_Tools\\strings.xml")
    androidStudioStringXmlPath = os.path.join(__android_res_path, "values\\strings.xml")
    util.move(stringXmlPath, androidStudioStringXmlPath)

    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        util.move(stringXmlPath, os.path.join(__launcher_main_path, "res\\values\\strings.xml"))


def __replace_branch_cn(__launcher_main_path, __unitylibrary_main_path):
    """
    国服渠道的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __android_res_path = os.path.join(__launcher_main_path, "res")
    if build_params.enableOfficial == "true" or build_params.enableBlend == "true":
        __icon_path = os.path.join(path_params.PROJECT_PATH, "Android_Tools\\icon_official" if build_params.enableOfficial == "true" else "Android_Tools\\icon_blend")
        if os.path.exists(__icon_path):
            util.move(__icon_path, __android_res_path, True)
    if build_params.targetSdkVersion != "":
        with open(path_params.BUILD_GRADLE_PATH, 'r+', encoding='utf-8') as rwf:
            __new_text = re.sub(r"targetSdkVersion (\d+)", "targetSdkVersion %s" % build_params.targetSdkVersion, rwf.read())
            rwf.seek(0)
            rwf.write(__new_text)
        util.console("set android build.gradle targetSdkVersion: %s", build_params.targetSdkVersion)

    __unity_main_path = ""
    __replace_dir = os.path.join(path_params.PROJECT_PATH, "Android_Tools\\replace")
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __unity_main_path = __unitylibrary_main_path
    else:
        __unity_main_path = __launcher_main_path
    util.console("[directory structure has changed] unity_main_pat:%s", __unity_main_path)

    if os.path.exists(__replace_dir):
        util.move(__replace_dir, __unity_main_path, True)


def __replace_branch_jp(__launcher_main_path, __unitylibrary_main_path):
    """
    日服渠道的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __unity_main_path = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __unity_main_path = __unitylibrary_main_path
    else:
        __unity_main_path = __launcher_main_path
    os.remove(os.path.join(__launcher_main_path, "res\\values\\strings.xml"))
    __replace_android_icon(__unity_main_path)


def __replace_branch_tw(__launcher_main_path, __unitylibrary_main_path):
    """
    台服渠道的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __unity_main_path = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __unity_main_path = __unitylibrary_main_path
    else:
        __unity_main_path = __launcher_main_path
    os.remove(os.path.join(__launcher_main_path, "res\\values\\strings.xml"))
    __replace_android_icon(__unity_main_path)


def __replace_branch_sa(__launcher_main_path, __unitylibrary_main_path):
    """
    东南亚服渠道的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __replace_branch_cn(__launcher_main_path, __unitylibrary_main_path)
    __replace_android_icon(__launcher_main_path)


def __replace_branch_na(__launcher_main_path, __unitylibrary_main_path):
    """
    美服渠道的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __replace_branch_cn(__launcher_main_path, __unitylibrary_main_path)
    __replace_android_icon(__launcher_main_path)


def __replace_branch_default(_launcher_main_path, __unitylibrary_main_path):
    """
    默认的替换逻辑
    Args:
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    __replace_branch_cn(_launcher_main_path, __unitylibrary_main_path)


def __replace_branch(_case, __launcher_main_path, __unitylibrary_main_path):
    """
    根据不同渠道进行Android工程文件替换
    Args:
        _case: 渠道
        __launcher_main_path: Android工程的主Module文件夹路径
        __unitylibrary_main_path: Android工程的UnityLibrary文件夹路径
    """
    functions = {
        "kr": __replace_branch_kr,
        "cn": __replace_branch_cn,
        "jp": __replace_branch_jp,
        "tw": __replace_branch_tw,
        "sa": __replace_branch_sa,
        "na": __replace_branch_na,
    }
    func = functions.get(_case, __replace_branch_default)
    func(__launcher_main_path, __unitylibrary_main_path)


def special_treatment_for_each_channel_in_android():
    """
    根据不同渠道进行Android工程文件替换
    """
    util.console(" special treatment for each channel start ".center(200, "#"))
    __launcher_main_path = ""
    __unitylibrary_main_path = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __launcher_main_path = os.path.join(path_params.ANDROID_LAUNCHER_PATH, "src\\main")
        __unitylibrary_main_path = os.path.join(path_params.ANDROID_UNITYLIBRARY_PATH, "src\\main")
    else:
        __android_studio_root_path = path_params.ANDROID_APP_PATH if build_params.enableAndroidAppBundle == "true" else path_params.ANDROID_STUDIO_PATH
        __launcher_main_path = os.path.join(__android_studio_root_path, "src\\main")
    util.console("[directory structure has changed] launcher_main_path:%s, unitylibrary_main_path:%s", __launcher_main_path, __unitylibrary_main_path)
    __replace_branch(build_params.channel, __launcher_main_path, __unitylibrary_main_path)
    __modify_android_version()

    util.console(" special treatment for each channel end ".center(200, "#"))


def start_android_studio_build():
    """
    开始进行AndroidStudio工程构建
    """
    util.console(" android studio build start ".center(200, "#"))
    __gradle = util.init_gradle(path_params.GRADLE_PATH, path_params.ANDROID_STUDIO_PATH)
    __gradle.Clean()
    __gradle.Bundle(build_params.buildType) if build_params.enableAndroidAppBundle == "true" else __gradle.Assemble(build_params.buildType)

    if build_params.enableAndroidAppBundle == "true" and build_params.enableUniversal == "true":
        build_appbundle_apk()
    util.console(" android studio build end ".center(200, "#"))


def build_appbundle_apk():
    """
    开始进行AndroidStudio工程构建AAB或者APK
    """
    util.console(" build android app bundle to apk start ".center(200, "#"))
    if path_params.KEYSTORE_PATH == "" or path_params.BUILD_GRADLE_PATH == "":
        return
    if not os.path.exists(path_params.KEYSTORE_PATH):
        raise Exception(path_params.KEYSTORE_PATH + " not exists!")
    if not os.path.exists(path_params.BUILD_GRADLE_PATH):
        raise Exception(path_params.BUILD_GRADLE_PATH + " not exists!")

    __keystore = ""
    for _file in os.listdir(path_params.KEYSTORE_PATH):
        if _file.endswith(".keystore") or _file.endswith(".jks"):
            __keystore = os.path.join(path_params.KEYSTORE_PATH, _file)
            break
    if __keystore == "":
        raise Exception(".keystore or .jks is empty!")
    else:
        util.console("keystore path:%s", __keystore)

    __storePassword = ""
    __keyAlias = ""
    __keyPassword = ""
    __text = ""
    with open(path_params.BUILD_GRADLE_PATH, 'r', encoding='utf-8') as rf:
        __text = rf.read()
    if __text != "":
        __storePasswords = re.findall(r"storePassword '(.+?)'", __text)
        __storePassword = __storePasswords[0] if len(__storePasswords) > 0 else ""
        __keyAliases = re.findall(r"keyAlias = '(.+?)'", __text)
        __keyAlias = __keyAliases[0] if len(__keyAliases) > 0 else ""
        __keyPasswords = re.findall(r"keyPassword '(.+?)'", __text)
        __keyPassword = __keyPasswords[0] if len(__keyPasswords) > 0 else ""
    util.console("storePassword:%s\nkeyAlias:%s\nkeyPassword:%s", __storePassword, __keyAlias, __keyPassword)

    if __storePassword == "" or __keyAlias == "" or __keyPassword == "":
        raise Exception("android keystore config is error !")

    __jar = util.init_jar(path_params.BUNDLE_TOOL_JAR_PATH, path_params.UPLOAD_SYMBOLS_JAR_PATH)
    if not os.path.exists(path_params.BUNDLE_TOOL_JAR_PATH):
        raise Exception("%s not found !" % path_params.BUNDLE_TOOL_JAR_PATH)

    __android_outputs_path = ""
    __build_model = ""
    # Unity2019 The directory structure has changed
    if sys_params.UNITY_VERSION and sys_params.UNITY_VERSION == "2019":
        __build_model = "launcher"
        __android_outputs_path = os.path.join(path_params.ANDROID_LAUNCHER_PATH, "build\\outputs")
    else:
        __build_model = "app"
        __android_outputs_path = os.path.join(path_params.ANDROID_APP_PATH, "build\\outputs")
    util.console("[directory structure has changed] android_outputs_path:%s, build_model:%s", __android_outputs_path, __build_model)

    __bundle = "{android_outputs_path}/bundle/{build_type}/{build_model}-{build_type}.aab".format(android_outputs_path=__android_outputs_path, build_type=build_params.buildType, build_model=__build_model)
    __output = "{android_outputs_path}/bundle/{build_type}/{build_type}.apks".format(android_outputs_path=__android_outputs_path, build_type=build_params.buildType)
    __mode = "--mode=universal" if build_params.enableUniversal == "true" else ""
    __jar.build_apks(__bundle, __output, __keystore, __storePassword, __keyAlias, __keyPassword, __mode)
    __unzip = util.unzip(__output)
    util.move(os.path.join(__unzip, "universal.apk"),
              "{android_outputs_path}/bundle/{build_type}/{build_type}.apk".format(android_outputs_path=__android_outputs_path, build_type=build_params.buildType))
    shutil.rmtree(__unzip)
    util.console(" build android app bundle to apk end ".center(200, "#"))


def zip_xcode_project_to_artifact():
    """
    压缩Unity导出的Xcode工程到Jenkins存档文件夹中
    """
    util.console(" zip xcode project to artifact start ".center(200, "#"))
    __ios_build = os.path.join(path_params.PROJECT_PATH, "IOSBuild")
    __output_time = os.path.getmtime(__ios_build)
    if localBuildTime < 0 or localBuildTime > __output_time:
        raise Exception("unity build or output error!")
    __zip = util.zip(__ios_build)
    __copy_to_artifact_path(__zip)
    util.console(" zip xcode project to artifact end ".center(200, "#"))


def start_build():
    """
    开始自动化构建
    """
    util.console(" build start ".center(200, "#"))
    if util.get_free_space_mb("C:\\") < const.WIN_MAX_DISK:
        raise Exception("No space left c: disk!")

    if build_params.startBuildingDirectly == "true":
        auto_build()

    if platform == Platform.Android:
        replace_android_studio_assets()
        start_android_studio_build()
        copy_android_apk_to_share()
        copy_main_zip_to_artifact()
    elif platform == Platform.IOS:
        zip_xcode_project_to_artifact()
    else:
        copy_windows_exe_to_share()

    util.console(" build end ".center(200, "#"))


def main_function():
    """
    主函数
    """
    init_jenkins_params()
    svn_clean_revert_update()
    start_build()


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
