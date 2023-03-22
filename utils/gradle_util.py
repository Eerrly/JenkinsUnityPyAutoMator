# -*- coding: UTF-8 -*-
import subprocess
import sys
from enum import Enum


class GRADLE(Enum):
    Clean = "{gradle_path} -info -p {android_project_path} clean"
    Bundle = "{gradle_path} -info -p {android_project_path} bundle{build_type}"
    Assemble = "{gradle_path} -info -p {android_project_path} assemble{build_type}"


class GradleHelper:
    """Gradle 工具类"""
    def __init__(self, _gradle_path, _android_project_path):
        self.gradle_path = _gradle_path
        self.android_project_path = _android_project_path

    def __str__(self):
        return "gradle information >\ngradle_path:%s\nandroid_project_path:%s" % (self.gradle_path, self.android_project_path)

    def __function(self, _enum, _build_type=None):
        _command = _enum.value.format(gradle_path=self.gradle_path, android_project_path=self.android_project_path, build_type=_build_type)
        sys.stdout.write(_command + "\n")
        sys.stdout.flush()
        _process = subprocess.Popen(_command, shell=True)
        _process.wait()
        if _process.returncode != 0:
            raise Exception(_process.returncode, _command)
        sys.stdout.write("{enum_type} successful !\n".format(enum_type=_enum))
        sys.stdout.flush()

    def Clean(self):
        """清除Android Project工程"""
        self.__function(GRADLE.Clean)

    def Bundle(self, _build_type):
        """构建
        构建Assets Bundle包

        Args:
            _build_type: 构建类型（Release/Debug）
        """
        self.__function(GRADLE.Bundle, _build_type=_build_type.capitalize())

    def Assemble(self, _build_type):
        """构建
        构建APK包

        Args:
            _build_type: 构建类型（Release/Debug）
        """
        self.__function(GRADLE.Assemble, _build_type=_build_type.capitalize())
