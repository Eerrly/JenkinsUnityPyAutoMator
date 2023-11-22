import subprocess
import sys
from enum import Enum


class XCODE(Enum):
    """
    XCODE枚举
    Attributes:
        PlistBuddyShortVersion: 修改短版本号
        PlistBuddyVersion: 修改版本号
        PlistBuddyAddAppleSignKey: 添加苹果登录Key
        PlistBuddyAddAppleSignValue: 添加苹果登录Value
        PlistBuddyDelAppleSign: 删除苹果登录
        Clean: 清理
        Archive: 归档
        ArchiveAutomatic: 自动归档
        ModifyBundleIdentifierAndArchive: 修改BundleIdentifier并归档
        Export: 导出
        UploadDsym: 上传Dsym
    """
    PlistBuddyShortVersion = "/usr/libexec/PlistBuddy -c 'Set :CFBundleShortVersionString {short_version}' {xcode_project}/Info.plist"
    PlistBuddyVersion = "/usr/libexec/PlistBuddy -c 'Set :CFBundleVersion {version}' {xcode_project}/Info.plist"
    SedBundleIdentifier = "/usr/libexec/PlistBuddy -c 'Set :CFBundleIdentifier {bundle_identifier}' {xcode_project}/Info.plist"
    PlistBuddyAddAppleSignKey = "/usr/libexec/PlistBuddy -c 'Add :com.apple.developer.applesignin array' {entitlements}"
    PlistBuddyAddAppleSignValue = "/usr/libexec/PlistBuddy -c 'Add :com.apple.developer.applesignin: string Default' {entitlements}"
    PlistBuddyDelAppleSign = "/usr/libexec/PlistBuddy -c 'Delete :com.apple.developer.applesignin' {entitlements}"
    Clean = "xcodebuild clean -project {xcode_project}/Unity-iPhone.xcodeproj -alltargets -UseModernBuildSystem=YES"
    Archive = "xcodebuild archive -project {xcode_project}/Unity-iPhone.xcodeproj -scheme 'Unity-iPhone' -configuration '{build_type}' -archivePath {archive_path} CODE_SIGN_IDENTITY='{CODE_SIGN_IDENTITY}' PROVISIONING_PROFILE{APP}='{PROVISIONING_PROFILE}' DEVELOPMENT_TEAM='{DEVELOPMENT_TEAM}' PRODUCT_BUNDLE_IDENTIFIER={bundle_identifier} CODE_SIGN_STYLE='Manual' -UseModernBuildSystem=YES"
    ArchiveAutomatic = "xcodebuild archive -project {xcode_project}/Unity-iPhone.xcodeproj -scheme 'Unity-iPhone' -configuration '{build_type}' -archivePath {archive_path} -allowProvisioningUpdates"
    ModifyBundleIdentifierAndArchive = "xcodebuild archive -project {xcode_project}/Unity-iPhone.xcodeproj -scheme 'Unity-iPhone' -configuration '{build_type}' -archivePath {archive_path} CODE_SIGN_IDENTITY='{CODE_SIGN_IDENTITY}' PROVISIONING_PROFILE{APP}='{PROVISIONING_PROFILE}' DEVELOPMENT_TEAM='{DEVELOPMENT_TEAM}' PRODUCT_BUNDLE_IDENTIFIER='{bundle_identifier}' CODE_SIGN_STYLE='Manual' -UseModernBuildSystem=YES"
    Export = "xcodebuild -exportArchive -archivePath {archive_path} -exportPath {export_path} -exportOptionsPlist {export_Options_plist} -UseModernBuildSystem=YES"
    UploadDsym = "{upload_symbols} -gsp {google_plist} -p ios {dsym_file}"


class XCodeHelper:
    """
    XCode 工具类
    """
    def __init__(self, _xcode_project):
        """
        初始化XCode工具类
        Args:
            _xcode_project: XCode工程路径
        """
        self.xcode_project = _xcode_project

    def __str__(self):
        return "xcode information >\nxcode_project:%s" % self.xcode_project

    def __function(self, _enum, _build_type=None, _archive_path=None, _CODE_SIGN_IDENTITY=None, _PROVISIONING_PROFILE=None, _DEVELOPMENT_TEAM=None, _APP=None, _export_path=None, _export_Options_plist=None, _upload_symbols=None,
                   _google_plist=None, _dsym_file=None, _entitlements=None, _short_version=None, _version=None, _bundle_identifier=None,):
        """
        执行方法
        Args:
            _enum: 枚举类型
            _build_type: 构建类型（Release/Debug）
            _archive_path: 归档路径
            _CODE_SIGN_IDENTITY: 证书
            _PROVISIONING_PROFILE: 描述文件
            _DEVELOPMENT_TEAM: 开发团队
            _APP: APP
            _export_path: 导出路径
            _google_plist: GoogleService-Info.plist路径
            _dsym_file: DSYM文件路径
            _entitlements: entitlements文件路径
            _short_version: 短版本号
            _version: 版本号
            _bundle_identifier: 包名
        """
        _command = _enum.value.format(xcode_project=self.xcode_project, short_version=_short_version, version=_version, build_type=_build_type, archive_path=_archive_path,
                                      bundle_identifier=_bundle_identifier, CODE_SIGN_IDENTITY=_CODE_SIGN_IDENTITY, PROVISIONING_PROFILE=_PROVISIONING_PROFILE, DEVELOPMENT_TEAM=_DEVELOPMENT_TEAM, APP=_APP,
                                      export_path=_export_path, export_Options_plist=_export_Options_plist,
                                      upload_symbols=_upload_symbols, google_plist=_google_plist, dsym_file=_dsym_file, entitlements=_entitlements)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True)
        _process.wait()
        if _process.returncode != 0:
            raise Exception(_process.returncode, _command)
        sys.stdout.write("{enum_type} successful !\n".format(enum_type=_enum))
        sys.stdout.flush()

    def PlistBuddyShortVersion(self, _short_version):
        """
        修改短版本号
        Args:
            _short_version: 短版本号
        """
        self.__function(XCODE.PlistBuddyShortVersion, _short_version=_short_version)

    def PlistBuddyVersion(self, _version):
        """
        修改版本号
        Args:
            _version: 版本号
        """
        self.__function(XCODE.PlistBuddyVersion, _version=_version)

    def PlistBuddyAddAppleSign(self, _entitlements):
        """
        添加苹果登录
        Args:
            _entitlements: entitlements文件路径
        """
        self.__function(XCODE.PlistBuddyAddAppleSignKey, _entitlements=_entitlements)
        self.__function(XCODE.PlistBuddyAddAppleSignValue, _entitlements=_entitlements)

    def PlistBuddyDelAppleSign(self, _entitlements):
        """
        删除苹果登录
        Args:
            _entitlements: entitlements文件路径
        """
        self.__function(XCODE.PlistBuddyDelAppleSign, _entitlements=_entitlements)

    def SedBundleIdentifierAndArchive(self, _bundle_identifier, _build_type, _archive_path, _CODE_SIGN_IDENTITY, _PROVISIONING_PROFILE, _DEVELOPMENT_TEAM, _APP):
        """
        修改BundleIdentifier并归档
        Args:
            _bundle_identifier: 包名
            _build_type: 构建类型（Release/Debug）
            _archive_path: 归档路径
            _CODE_SIGN_IDENTITY: 证书
            _PROVISIONING_PROFILE: 描述文件
            _DEVELOPMENT_TEAM: 开发团队
            _APP: APP
        """
        # self.__function(XCODE.SedBundleIdentifier, _bundle_identifier=_bundle_identifier)
        self.__function(XCODE.ModifyBundleIdentifierAndArchive, _bundle_identifier=_bundle_identifier, _build_type=_build_type, _archive_path=_archive_path, _CODE_SIGN_IDENTITY=_CODE_SIGN_IDENTITY, _PROVISIONING_PROFILE=_PROVISIONING_PROFILE, _DEVELOPMENT_TEAM=_DEVELOPMENT_TEAM, _APP=_APP)

    def Clean(self):
        """
        清理
        """
        self.__function(XCODE.Clean)

    # security cms -D -i
    def Archive(self, _build_type, _archive_path, _CODE_SIGN_IDENTITY, _PROVISIONING_PROFILE, _DEVELOPMENT_TEAM, _APP):
        """
        归档
        Args:
            _build_type: 构建类型（Release/Debug）
            _archive_path: 归档路径
            _CODE_SIGN_IDENTITY: 证书
            _PROVISIONING_PROFILE: 描述文件
            _DEVELOPMENT_TEAM: 开发团队
            _APP: APP
        """
        self.__function(XCODE.Archive, _build_type=_build_type, _archive_path=_archive_path, _CODE_SIGN_IDENTITY=_CODE_SIGN_IDENTITY, _PROVISIONING_PROFILE=_PROVISIONING_PROFILE, _DEVELOPMENT_TEAM=_DEVELOPMENT_TEAM, _APP=_APP)

    def ArchiveAutomatic(self, _build_type, _archive_path):
        """
        自动归档
        Args:
            _build_type: 构建类型（Release/Debug）
            _archive_path: 归档路径
        """
        self.__function(XCODE.ArchiveAutomatic, _build_type=_build_type, _archive_path=_archive_path)

    def Export(self, _archive_path,  _export_path, _export_Options_plist):
        """
        导出
        Args:
            _archive_path: 归档路径
            _export_path: 导出路径
            _export_Options_plist: 导出配置文件
        """
        self.__function(XCODE.Export, _archive_path=_archive_path, _export_path=_export_path, _export_Options_plist=_export_Options_plist)

    def UploadDsym(self, _upload_symbols, _google_plist, _dsym_file):
        """
        上传Dsym
        Args:
            _upload_symbols: 上传符号表文件路径
            _google_plist: GoogleService-Info.plist路径
            _dsym_file: DSYM文件路径
        """
        self.__function(XCODE.UploadDsym, _upload_symbols=_upload_symbols, _google_plist=_google_plist, _dsym_file=_dsym_file)
