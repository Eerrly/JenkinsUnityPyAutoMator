# -*- coding: UTF-8 -*-
import os

import util


class JenkinsClass:
    """
    Jenkins参数类
    Attributes:
        WORKSPACE: Jenkins工作目录
        JENKINS_HOME: Jenkins主目录
        JOB_NAME: Jenkins任务名称
        BUILD_NUMBER: Jenkins构建编号
    """
    WORKSPACE = ""
    JENKINS_HOME = ""
    JOB_NAME = ""
    BUILD_NUMBER = ""

    def __init__(self):
        self.WORKSPACE = os.environ["WORKSPACE"]
        self.JENKINS_HOME = os.environ["JENKINS_HOME"]
        self.JOB_NAME = os.environ["JOB_NAME"]
        self.BUILD_NUMBER = os.environ["BUILD_NUMBER"]
        util.console(self)

    def __str__(self):
        return "WORKSPACE:%s\nJENKINS_HOME:%s\nJOB_NAME:%s\nBUILD_NUMBER:%s" % (self.WORKSPACE, self.JENKINS_HOME, self.JOB_NAME, self.BUILD_NUMBER)


class SystemClass:
    """
    系统参数类
    Attributes:
        UNITY_EXE: Unity.exe路径
        UNITY_PROJECT: Unity工程路径
        UNITY_USER_NAME: Unity用户名
        UNITY_USER_PASSWORD: Unity用户密码
        UNITY_USER_SERIAL: Unity用户序列号
        UNITY_VERSION: Unity版本号
    """
    UNITY_EXE = ""
    UNITY_PROJECT = ""
    UNITY_USER_NAME = ""
    UNITY_USER_PASSWORD = ""
    UNITY_USER_SERIAL = ""
    UNITY_VERSION = ""

    def __init__(self, sys_argv):
        self.UNITY_EXE = sys_argv[1]
        self.UNITY_PROJECT = sys_argv[2]
        self.UNITY_USER_NAME = sys_argv[3]
        self.UNITY_USER_PASSWORD = sys_argv[4]
        self.UNITY_USER_SERIAL = sys_argv[5]

        try:
            self.UNITY_VERSION = sys_argv[6]
        except IndexError:
            self.UNITY_VERSION = ""

        util.console(self)

    def __str__(self):
        return "UNITY_EXE:%s\nUNITY_PROJECT:%s\nUNITY_USER_NAME:%s\nUNITY_USER_PASSWORD:%s\nUNITY_USER_SERIAL:%s\nUNITY_VERSION:%s" % (
            self.UNITY_EXE, self.UNITY_PROJECT, self.UNITY_USER_NAME, self.UNITY_USER_PASSWORD, self.UNITY_USER_SERIAL, self.UNITY_VERSION)


class PathClass:
    """
    路径参数类
    Attributes:
        UNITY_EXE: Unity.exe路径
        PROJECT_PATH: Unity工程路径
        PATCH_PATH: 热更工程路径
        ANDROID_STUDIO_PATH: Android Studio工程路径
        ANDROID_APP_PATH: Android Studio App工程路径
        INSTALL_TIME_ASSET_PACK_PATH: Android Studio InstallTimeAssetPack工程路径
        GRADLE_PATH: Android Studio Gradle路径
        CLEAN_PATH: 清理路径
        UNITY_LOG_PATH: Unity日志路径
        SYMBOLS_ZIP_PATH: Symbols.zip路径
        LIB_IL2CPP_SO_PATH: libil2cpp.so路径
        UPLOAD_SYMBOLS_JAR_PATH: 上传Symbols.jar路径
        BUNDLE_TOOL_JAR_PATH: BundleTool.jar路径
        MAIN_ZIP_PATH: Main.zip路径
        KEYSTORE_PATH: KeyStore路径
        BUILD_GRADLE_PATH: Build.gradle路径
        ANDROID_LAUNCHER_PATH: Android Launcher路径
        ANDROID_UNITYLIBRARY_PATH: Android UnityLibrary路径
    """
    UNITY_EXE = ""
    PROJECT_PATH = ""
    PATCH_PATH = ""
    ANDROID_STUDIO_PATH = ""
    ANDROID_APP_PATH = ""
    INSTALL_TIME_ASSET_PACK_PATH = ""
    GRADLE_PATH = ""
    CLEAN_PATH = ""
    UNITY_LOG_PATH = ""
    SYMBOLS_ZIP_PATH = ""
    LIB_IL2CPP_SO_PATH = ""
    UPLOAD_SYMBOLS_JAR_PATH = ""
    BUNDLE_TOOL_JAR_PATH = ""
    MAIN_ZIP_PATH = ""
    KEYSTORE_PATH = ""
    BUILD_GRADLE_PATH = ""
    ANDROID_LAUNCHER_PATH = ""
    ANDROID_UNITYLIBRARY_PATH = ""

    def __init__(self, _unity_exe, _project_path, _android_studio_path=None, _build_gradle_path=None):
        self.UNITY_EXE = _unity_exe
        self.PROJECT_PATH = _project_path
        self.PATCH_PATH = "%s\\Client\\Patch" % self.PROJECT_PATH
        self.CLEAN_PATH = "%s\\Client\\Assets" % self.PROJECT_PATH
        self.UNITY_LOG_PATH = "%s\\build.log" % self.PROJECT_PATH

        if _android_studio_path is not None:
            self.ANDROID_STUDIO_PATH = _android_studio_path
            self.ANDROID_APP_PATH = "%s\\app" % self.ANDROID_STUDIO_PATH
            self.ANDROID_LAUNCHER_PATH = "%s\\launcher" % self.ANDROID_STUDIO_PATH
            self.ANDROID_UNITYLIBRARY_PATH = "%s\\unityLibrary" % self.ANDROID_STUDIO_PATH
            self.INSTALL_TIME_ASSET_PACK_PATH = "%s\\install_time_asset_pack" % self.ANDROID_STUDIO_PATH
            self.GRADLE_PATH = "%s\\gradlew.bat" % self.ANDROID_STUDIO_PATH
            self.BUILD_GRADLE_PATH = "%s\\build.gradle" % self.ANDROID_APP_PATH
        if _build_gradle_path is not None:
            self.BUILD_GRADLE_PATH = _build_gradle_path

        self.SYMBOLS_ZIP_PATH = "%s\\output-1.0-v1.symbols.zip" % self.PROJECT_PATH
        self.LIB_IL2CPP_SO_PATH = "%s\\libil2cpp.so" % self.PROJECT_PATH

        self.KEYSTORE_PATH = "%s\\Android_Tools\\key" % self.PROJECT_PATH
        self.UPLOAD_SYMBOLS_JAR_PATH = "%s\\Android_Tools\\buglyqq-upload-symbol.jar" % self.PROJECT_PATH
        self.BUNDLE_TOOL_JAR_PATH = "%s\\Android_Tools\\bundletool-all-1.6.1.jar" % self.PROJECT_PATH

        self.MAIN_ZIP_PATH = "%s\\Android_Tools\\Main.zip" % self.PROJECT_PATH
        util.console(self)

    def __str__(self):
        return "UNITY_EXE:%s\nPROJECT_PATH:%s\nANDROID_STUDIO_PATH:%s\nKEYSTORE_PATH:%s\nMAIN_ZIP_PATH:%s\n" % (
            self.UNITY_EXE, self.PROJECT_PATH, self.ANDROID_STUDIO_PATH, self.KEYSTORE_PATH, self.MAIN_ZIP_PATH)


class UnityClass:
    """
    Unity参数类
    Attributes:
        enableGM: 是否开启GM
        enableGuide: 是否开启新手引导
        enableSDK: 是否开启SDK
        enableConsole: 是否开启Console
        enableLog: 是否开启Log
        enablePatching: 是否开启热更
        loginServer: 登录服务器
        enableQAServerCDN: 是否开启QA服务器CDN
        enableFPS: 是否开启FPS
        isAuthenticationServer: 是否是战斗校验服务器
        enableBuildResources: 是否开启资源打包
    """
    enableGM = ""
    enableGuide = ""
    enableSDK = ""
    enableConsole = ""
    enableLog = ""
    enablePatching = ""
    loginServer = ""
    enableQAServerCDN = ""
    enableFPS = ""
    isAuthenticationServer = ""
    enableBuildResources = ""

    def __init__(self):
        self.enableGM = "" if os.environ.get("enableGM") is None else os.environ["enableGM"]
        self.enableGuide = "" if os.environ.get("enableGuide") is None else os.environ["enableGuide"]
        self.enableSDK = "" if os.environ.get("enableSDK") is None else os.environ["enableSDK"]
        self.enableConsole = "" if os.environ.get("enableConsole") is None else os.environ["enableConsole"]
        self.enableLog = "" if os.environ.get("enableLog") is None else os.environ["enableLog"]
        self.enablePatching = "" if os.environ.get("enablePatching") is None else os.environ["enablePatching"]
        self.loginServer = "" if os.environ.get("loginServer") is None else os.environ["loginServer"]
        self.enableQAServerCDN = "" if os.environ.get("enableQAServerCDN") is None else os.environ["enableQAServerCDN"]
        self.enableFPS = "" if os.environ.get("enableFPS") is None else os.environ["enableFPS"]
        self.isAuthenticationServer = "" if os.environ.get("isAuthenticationServer") is None else os.environ["isAuthenticationServer"]
        self.enableBuildResources = "" if os.environ.get("enableBuildResources") is None else os.environ["enableBuildResources"]
        util.console(self)

    def __str__(self):
        return "enableGM:%s\nenableGuide:%s\nenableSDK:%s\nenableConsole:%s\nenableLog:%s\nenablePatching:%s\nloginServer:%s\nenableQAServerCDN:%s\nenableFPS:%s\nisAuthenticationServer:%s\nenableBuildResources:%s" % (
            self.enableGM, self.enableGuide, self.enableSDK, self.enableConsole, self.enableLog, self.enablePatching, self.loginServer, self.enableQAServerCDN, self.enableFPS,
            self.isAuthenticationServer, self.enableBuildResources)


class BuildClass:
    """
    构建参数类
    Attributes:
        channel: 渠道
        enableAndroidAppBundle: 是否开启AndroidAppBundle模式
        buildType: 构建类型
        buildTarget: 构建目标
        startBuildingDirectly: 是否直接开始构建
        enableUniversal: 是否开启Universal模式
        disableSvnUpdateCleanUnityProject: 是否跳过svn更新和清理Unity工程
        androidChannel: Android工程渠道
        androidVersion: Android工程版本号
        targetSdkVersion: Android工程targetSdkVersion
        enableOfficial: 是否开启官服
        enableBlend: 是否开启混服
    """
    channel = ""

    enableAndroidAppBundle = ""
    buildType = ""
    buildTarget = ""
    startBuildingDirectly = ""  # Skip unity and build directly from Android
    enableUniversal = ""
    disableSvnUpdateCleanUnityProject = ""  # Skip svn update and clean
    # Android Project Channel
    androidChannel = ""
    androidVersion = ""  # {versionCode*versionName}
    # CN
    targetSdkVersion = ""  # {targetSdkVersion}
    enableOfficial = ""
    enableBlend = ""

    def __init__(self):
        self.channel = os.environ["channel"]

        self.enableAndroidAppBundle = "" if os.environ.get("enableAndroidAppBundle") is None else os.environ["enableAndroidAppBundle"]
        self.buildType = "" if os.environ.get("buildType") is None else os.environ["buildType"]
        self.buildTarget = "" if os.environ.get("platform") is None else os.environ["platform"]
        self.startBuildingDirectly = "" if os.environ.get("startBuildingDirectly") is None else os.environ["startBuildingDirectly"]
        self.enableUniversal = "" if os.environ.get("enableUniversal") is None else os.environ["enableUniversal"]
        self.disableSvnUpdateCleanUnityProject = "" if os.environ.get("disableSvnUpdateCleanUnityProject") is None else os.environ["disableSvnUpdateCleanUnityProject"]
        self.androidChannel = "" if os.environ.get("androidChannel") is None else os.environ["androidChannel"]
        self.androidVersion = "" if os.environ.get("androidVersion") is None else os.environ["androidVersion"]

        # CN
        self.targetSdkVersion = "" if os.environ.get("targetSdkVersion") is None else os.environ["targetSdkVersion"]
        self.enableOfficial = "" if os.environ.get("enableOfficial") is None else os.environ["enableOfficial"]
        self.enableBlend = "" if os.environ.get("enableBlend") is None else os.environ["enableBlend"]
        util.console(self)

    def __str__(self):
        return "channel:%s\nenableAndroidAppBundle:%s\nbuildType:%s\nbuildTarget:%s\nstartBuildingDirectly:%s\nenableUniversal:%s\n" \
               "androidChannel:%s\ntargetSdkVersion:%s\nenableOfficial:%s\nenableBlend:%s\ndisableSvnUpdateCleanUnityProject:%s" % (
                   self.channel, self.enableAndroidAppBundle, self.buildType, self.buildTarget, self.startBuildingDirectly, self.enableUniversal, self.androidChannel,
                   self.targetSdkVersion, self.enableOfficial, self.enableBlend, self.disableSvnUpdateCleanUnityProject)


class PatchClass:
    """
    热更参数类
    Attributes:
        empty_patch: 是否空热更
        clean_update_project: 是否清理更新工程
        channel: 渠道
        platform: 平台
        patch_version: 热更版本号
        start_svn_version: 开始svn版本号
        end_svn_version: 结束svn版本号
        version: 版本号
        no_safe_fast: 是否跳过安全检查
    """
    empty_patch = ""
    clean_update_project = ""
    channel = ""
    platform = ""
    patch_version = ""
    start_svn_version = ""
    end_svn_version = ""
    version = ""
    no_safe_fast = ""

    def __init__(self):
        self.empty_patch = "" if os.environ.get("empty_patch") is None else os.environ["empty_patch"]
        self.clean_update_project = "" if os.environ.get("clean_update_project") is None else os.environ["clean_update_project"]
        self.channel = "" if os.environ.get("channel") is None else os.environ["channel"]
        self.platform = "" if os.environ.get("Platform") is None else os.environ["Platform"]
        self.patch_version = "" if os.environ.get("Patch_Version") is None else os.environ["Patch_Version"]
        self.start_svn_version = "" if os.environ.get("Start_Svn_Version") is None else os.environ["Start_Svn_Version"]
        self.end_svn_version = "" if os.environ.get("End_Svn_Version") is None else os.environ["End_Svn_Version"]
        self.version = "" if os.environ.get("Version") is None else os.environ["Version"]
        self.no_safe_fast = "" if os.environ.get("no_safe_fast") is None else os.environ["no_safe_fast"]
        util.console(self)

    def __str__(self):
        return "empty_patch:%s\nclean_update_project:%s\nchannel:%s\nplatform:%s\npatch_version:%s\nstart_svn_version:%s\nend_svn_version:%s\nversion:%s\nno_safe_fast:%s\n" % (
            self.empty_patch, self.clean_update_project, self.channel, self.platform, self.patch_version, self.start_svn_version, self.end_svn_version, self.version, self.no_safe_fast)


class CDNClass:
    """
    CDN参数类
    Attributes:
        version: 版本号
        channel: 渠道
        upload_type: 上传类型
        patch_type: 热更类型
        delete_other: 是否删除其他版本
        cdn_address: CDN地址
        account_information: 账号信息
        remote_path: 远程路径
        upload_channel_list: 上传渠道列表
    """
    version = ""
    channel = ""
    upload_type = ""
    patch_type = ""
    delete_other = False
    cdn_address = ""
    account_information = ""
    remote_path = ""
    upload_channel_list = ""

    def __init__(self):
        self.version = "" if os.environ.get("version") is None else os.environ["version"]
        self.channel = "" if os.environ.get("channel") is None else os.environ["channel"]
        self.upload_type = "" if os.environ.get("upload_type") is None else os.environ["upload_type"]
        self.patch_type = "" if os.environ.get("patch_type") is None else os.environ["patch_type"]
        self.delete_other = ("" if os.environ.get("delete_other") is None else os.environ["delete_other"]) == "true"
        self.cdn_address = "" if os.environ.get("cdn_address") is None else os.environ["cdn_address"]
        if self.cdn_address == "" or len(self.cdn_address.split("*")) < 2:
            raise Exception("the param cdn url is error!")
        self.account_information = "" if os.environ.get("account_information") is None else os.environ["account_information"]
        if self.account_information == "" or len(self.account_information.split("*")) < 3:
            raise Exception("the param account infomation is error!")
        self.remote_path = "" if os.environ.get("remote_path") is None else os.environ["remote_path"]
        self.upload_channel_list = "" if os.environ.get("upload_channel_list") is None else os.environ["upload_channel_list"]
        util.console(self)

    def __str__(self):
        return "version:%s\nchannel:%s\npatch_type:%s\nupload_type:%s\ndelete_other:%s\ncdn_address:%s\nremote_path:%s\nupload_channel_list:%s" % (
            self.version, self.channel, self.patch_type, self.upload_type, self.delete_other, self.cdn_address, self.remote_path, self.upload_channel_list)


class VersionClass:
    """
    版本号相关参数类
    Attributes:
        version: 版本号
        modify_type: 修改类型
        cdn_address: CDN地址
        account_information: 账号信息
        modify_path: 修改路径
        platform: 平台
        all_platform_modify_field: 所有平台修改字段
        all_platform_modify_value: 所有平台修改目标值
        platform_modify_info: 平台修改信息
        is_check: 是否是check文件
        check_value: check文件值
    """
    version = ""
    modify_type = ""
    cdn_address = ""
    account_information = ""
    modify_path = ""
    platform = ""
    all_platform_modify_field = ""  # 所有的修改字段
    all_platform_modify_value = ""  # 修改目标值
    platform_modify_info = ""  # 针对平台修改的info 实例：version*10*1*2&url*http:1.2.3*http:1.4.5
    is_check = False  # 是不是check文件
    check_value = ""

    def __init__(self):
        self.version = "" if os.environ.get("version") is None else os.environ["version"]
        self.modify_type = "" if os.environ.get("modify_type") is None else os.environ["modify_type"]
        self.cdn_address = "" if os.environ.get("cdn_address") is None else os.environ["cdn_address"]
        if self.cdn_address == "" or len(self.cdn_address.split("*")) < 2:
            raise Exception("the param cdn url is error!")
        self.account_information = "" if os.environ.get("account_information") is None else os.environ["account_information"]
        if self.account_information == "" or len(self.account_information.split("*")) < 3:
            raise Exception("the param account infomation is error!")
        self.modify_path = "" if os.environ.get("modify_path") is None else os.environ["modify_path"]
        if self.modify_path == "":
            raise Exception("the param modify_path is None")
        self.platform = "" if os.environ.get("platform") is None else os.environ["platform"]
        self.all_platform_modify_field = "" if os.environ.get("all_platform_modify_field") is None else os.environ["all_platform_modify_field"]
        self.all_platform_modify_value = "" if os.environ.get("all_platform_modify_value") is None else os.environ["all_platform_modify_value"]
        self.is_check = ("" if os.environ.get("is_check") is None else os.environ["is_check"]) == "true"
        self.check_value = "" if os.environ.get("check_value") is None else os.environ["check_value"]
        self.platform_modify_info = "" if os.environ.get("platform_modify_info") is None else os.environ["platform_modify_info"]

    def __str__(self):
        return "version:%s\modify_type:%s\ncdn_address:%s\naccount_information:%s\nmodify_path:%s\nplatform:%s\nall_platform_modify_field:%s" \
               "\nall_platform_modify_value:%s\nis_check:%s\ncheck_value:%s\nplatform_modify_info:%s" % (
                   self.version, self.modify_type, self.cdn_address, self.account_information, self.modify_path, self.platform, self.all_platform_modify_field,
                   self.all_platform_modify_value, self.is_check, self.check_value, self.platform_modify_info)


class XCodeClass:
    """
    Xcode参数类
    Attributes:
        channel: 渠道
        buildType: 构建类型
        export_options_plist_name: 导出选项名称
        xcode_version_build: Xcode版本号
        CODE_SIGN_IDENTITY: 证书
        PROVISIONING_PROFILE: 描述文件
        PROVISIONING_PROFILE_SPECIFIER: 描述文件名称
        DEVELOPMENT_TEAM: 开发团队
        APP: APP名称
        enable_apple_sign: 是否开启苹果签名
        upload_symbols: 是否上传符号表
        bundle_identifier: 包名
        automatic: 是否自动化
    """
    channel = ""
    buildType = ""
    export_options_plist_name = ""
    xcode_version_build = ""
    CODE_SIGN_IDENTITY = ""
    PROVISIONING_PROFILE = ""
    PROVISIONING_PROFILE_SPECIFIER = ""
    DEVELOPMENT_TEAM = "",
    APP = "",
    enable_apple_sign = ""
    upload_symbols = ""
    bundle_identifier = ""
    automatic = ""

    def __init__(self):
        self.channel = "" if os.environ.get("channel") is None else os.environ["channel"]
        self.buildType = "" if os.environ.get("buildType") is None else os.environ["buildType"]
        self.export_options_plist_name = "" if os.environ.get("export_options_plist_name") is None else os.environ["export_options_plist_name"]
        self.xcode_version_build = "" if os.environ.get("xcode_version_build") is None else os.environ["xcode_version_build"]
        if self.xcode_version_build != "" and len(self.xcode_version_build.split("*")) != 2:
            raise Exception("IOS version number parameter error!")
        
        self.CODE_SIGN_IDENTITY = "" if os.environ.get("CODE_SIGN_IDENTITY") is None else os.environ["CODE_SIGN_IDENTITY"]
        self.PROVISIONING_PROFILE = "" if os.environ.get("PROVISIONING_PROFILE") is None else os.environ["PROVISIONING_PROFILE"]
        self.PROVISIONING_PROFILE_SPECIFIER = "" if os.environ.get("PROVISIONING_PROFILE_SPECIFIER") is None else os.environ["PROVISIONING_PROFILE_SPECIFIER"]
        self.DEVELOPMENT_TEAM = "" if os.environ.get("DEVELOPMENT_TEAM") is None else os.environ["DEVELOPMENT_TEAM"]
        self.APP = "" if os.environ.get("APP") is None else os.environ["APP"]
        self.bundle_identifier = "" if os.environ.get("bundle_identifier") is None else os.environ["bundle_identifier"]

        self.enable_apple_sign = "" if os.environ.get("enable_apple_sign") is None else os.environ["enable_apple_sign"]
        self.upload_symbols = "" if os.environ.get("upload_symbols") is None else os.environ["upload_symbols"]

        self.automatic = "" if os.environ.get("automatic") is None else os.environ["automatic"]

        util.console(self)

    def __str__(self):
        return "channel:%s\nbuildType:%s\nxcode_version_build:%s\nCODE_SIGN_IDENTITY:%s\nPROVISIONING_PROFILE:%s\nPROVISIONING_PROFILE_SPECIFIER:%s\nDEVELOPMENT_TEAM:%s\nAPP:%s\nenable_apple_sign:%s\nupload_symbols:%s" \
               "\nexport_options_plist_name:%s\nbundle_identifier:%s" % (
                   self.channel, self.buildType, self.xcode_version_build, self.CODE_SIGN_IDENTITY, self.PROVISIONING_PROFILE, self.PROVISIONING_PROFILE_SPECIFIER, self.DEVELOPMENT_TEAM, self.APP, self.enable_apple_sign, self.upload_symbols,
                   self.export_options_plist_name, self.bundle_identifier)


class COSClass:
    """
    Cos参数类
    Attributes:
        version: 版本号
        secretId: secretId
        secretKey: secretKey
        bucket: 桶
        region: 地区
        remote_path: 远程路径
    """
    version = ""
    secretId = ""
    secretKey = ""
    bucket = ""
    region = ""
    remote_path = ""

    def __init__(self):
        self.version = "" if os.environ.get("version") is None else os.environ["version"]
        self.secretId = "" if os.environ.get("secretId") is None else os.environ["secretId"]
        self.secretKey = "" if os.environ.get("secretKey") is None else os.environ["secretKey"]
        self.bucket = "" if os.environ.get("bucket") is None else os.environ["bucket"]
        self.region = "" if os.environ.get("region") is None else os.environ["region"]
        self.remote_path = "" if os.environ.get("remote_path") is None else os.environ["remote_path"]

    def __str__(self):
        return "version:%s\nsecretId:%s\nsecretKey:******\nbucket:%s\nregion:%s\nremote_path:%s" % (
            self.version, self.secretId, self.bucket, self.region, self.remote_path
        )
