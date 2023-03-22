import subprocess
import sys
from enum import Enum


class JAR(Enum):
    BuildApks = "java -jar {bt_jar} build-apks --bundle={bundle} --output={output} {mode} --ks={keystore} --ks-pass=pass:{k_pass} --ks-key-alias={key_alias} --key-pass=pass:{key_pass}"
    UploadSymbols = "java -jar {us_jar} -appid {appid} -appkey {appkey} -bundleid {bundleid} -version {version} -platform {platform} -inputSymbol {df_path}"


class JarHelper:
    """Jar 工具类"""
    def __init__(self, _bt_jar, _us_jar):
        self.bt_jar = _bt_jar
        self.us_jar = _us_jar

    def __str__(self):
        return "jar information >\nbt_jar:%s\nus_jar:%s" % (self.bt_jar, self.us_jar)

    def __function(self, _enum, _bundle=None, _output=None, _mode=None, _keystore=None, _k_pass=None, _key_alias=None, _key_pass=None,
                   _appid=None, _appkey=None, _bundleid=None, _version=None, _platform=None, _df_path=None):
        _command = _enum.value.format(bt_jar=self.bt_jar, us_jar=self.us_jar, bundle=_bundle, output=_output, mode=_mode, keystore=_keystore, k_pass=_k_pass, key_alias=_key_alias, key_pass=_key_pass,
                                      appid=_appid, appkey=_appkey, bundleid=_bundleid, version=_version, platform=_platform, df_path=_df_path)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True)
        _process.wait()
        if _process.stderr:
            sys.stdout.write("{enum_type} failed ! error : {error}\n".format(enum_type=_enum, error=_process.stderr))
        else:
            sys.stdout.write("{enum_type} successful !\n".format(enum_type=_enum))
        sys.stdout.flush()

    def build_apks(self, _bundle, _output, _keystore, _k_pass, _key_alias, _key_pass, _mode=None):
        """构建APKS
        通过Jar将 Android App Bundle 文件构建成 APKS 文件

        Args:
            _bundle: Android App Bundle 文件路径
            _output: APKS 的导出路径
            _keystore: Android KeyStore 路径
            _k_pass: k_pass
            _key_alias: key_alias
            _key_pass: key_pass
            _mode: 模式 (universal)
        """
        self.__function(JAR.BuildApks, _bundle=_bundle, _output=_output, _keystore=_keystore, _k_pass=_k_pass, _key_alias=_key_alias, _key_pass=_key_pass, _mode=_mode)

    def upload_symbols(self, _appid, _appkey, _bundleid, _version, _platform, _df_path):
        """上传Firebase符号表文件
        上传符号表文件到Firebase后台

        Args:
            _appid: appid
            _appkey: appkey
            _bundleid: bundleid
            _version: version
            _platform: platform
            df_path: 符号表文件路径
        """
        self.__function(JAR.UploadSymbols, _appid=_appid, _appkey=_appkey, _bundleid=_bundleid, _version=_version, _platform=_platform, _df_path=_df_path)
