import subprocess
import sys
from enum import Enum


class UNITY(Enum):
    Switch = "\"{unity_exe}\" -quit -batchmode -projectPath {project_path}\Client -logFile {logPath} {build_target} -username {username} -password {password} -serial {serial}"
    ExecuteMethod = "\"{unity_exe}\" {no_safe_param} -quit -batchmode -projectPath {project_path}\Client -executeMethod {executeMethodName} -username {username} -password {password} -serial {serial} -logFile {logPath} -param {paramInfo}"
    ExecuteMethodForeWait = "start /wait \"{unity_exe}\" -projectPath {project_path}\Client -executeMethod {executeMethodName} -username {username} -password {password} -serial {serial} -logFile {logPath}"


class UnityHelper:

    def __init__(self, _sysparams, _log, _build_target):
        self.sysparams = _sysparams
        self.log = _log
        self.build_target = _build_target
        if self.sysparams.UNITY_USER_NAME == "" or self.sysparams.UNITY_USER_PASSWORD == "" or self.sysparams.UNITY_USER_SERIAL == "":
            raise Exception("Please set UNITY_USER_NAME, UNITY_USER_PASSWORD, UNITY_USER_SERIAL values !\n")

    def __str__(self):
        return "unity information >\nunity:%s\nproject:%s\nusername:%spassword:%s\nserial:%s\nlog:%s\nbuild_target:%s" % (
            self.sysparams.UNITY_EXE, self.sysparams.UNITY_PROJECT, self.sysparams.UNITY_USER_NAME, self.sysparams.UNITY_USER_PASSWORD, self.sysparams.UNITY_USER_SERIAL, self.log, self.build_target)

    def __function(self, _enum, _method_name=None, _param_info=None, _no_safe_param=None):
        _command = _enum.value.format(
            unity_exe=self.sysparams.UNITY_EXE, project_path=self.sysparams.UNITY_PROJECT, username=self.sysparams.UNITY_USER_NAME, password=self.sysparams.UNITY_USER_PASSWORD, serial=self.sysparams.UNITY_USER_SERIAL,
            logPath=self.log, build_target=self.build_target, executeMethodName=_method_name, paramInfo=_param_info, no_safe_param=_no_safe_param)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True)
        _process.wait()
        if _process.returncode != 0:
            sys.stdout.write("{enum_type} failed ! error : {error}\n".format(enum_type=_enum, error=_process.stderr))
        else:
            sys.stdout.write("{enum_type} successful !\n".format(enum_type=_enum))
        sys.stdout.flush()

    def switch(self):
        self.__function(UNITY.Switch)

    def execute(self, _method_name, _param_info, _no_safe_fast="false"):
        if _no_safe_fast == "true":
            self.__function(UNITY.ExecuteMethod, _method_name, _param_info, "-disable-assembly-updater")
        else:
            self.__function(UNITY.ExecuteMethod, _method_name, _param_info)

    # For shader variant collection
    def execute_fore_wait(self, _method_name):
        self.__function(UNITY.ExecuteMethodForeWait, _method_name)
