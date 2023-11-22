# -*- coding: UTF-8 -*-
import shutil

import func
from utils.cdn_flush_util import CDNFlushHelper
from utils.cos_util import COSHelper
from utils.ftp_util import FTPHelper
from utils.gradle_util import GradleHelper
from utils.jar_util import JarHelper
from utils.ssh_util import SSHHelper
from utils.svn_util import SVNHelper
from utils.tail_util import TailHelper
from utils.unity_util import UnityHelper
from utils.vpn_util import VPNHelper
from utils.xcode_util import XCodeHelper
from utils.aws_util import AWSHelper

svn = None
vpn = None
ftp = None
unity = None
jar = None
tail = None
ssh = None
xcode = None
flush = None
gradle = None
cos = None
aws = None


def console(_message, *_params):
    """
    控制台输出
    Args:
        _message: 输出信息
        *_params: 输出参数
    """
    func.__console(_message, *_params)


def unzip(_src_path, _dst_path=None):
    """
    解压缩
    Args:
        _src_path: 源文件路径
        _dst_path: 目标文件路径
    Returns:
        解压后的文件路径
    """
    return func.__unzip(_src_path, _dst_path)


def zip(_src_path, _dst_path=None):
    """
    压缩
    Args:
        _src_path: 源文件路径
        _dst_path: 目标文件路径
    Returns:
        压缩后的文件路径
    """
    return func.__zip(_src_path, _dst_path)


def copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False):
    """
    复制文件夹
    Args:
        src: 源文件夹
        dst: 目标文件夹
        symlinks: 是否复制链接
        ignore: 忽略文件
        copy_function: 复制方法
        ignore_dangling_symlinks: 忽略链接
    Returns:
        复制后的文件夹
    """
    return func.__copytree(src, dst, symlinks, ignore, copy_function, ignore_dangling_symlinks)


def move(__src_path, __dst_path, __cover=False):
    """
    移动文件
    Args:
        __src_path: 源文件路径
        __dst_path: 目标文件路径
        __cover: 是否覆盖
    Returns:
        移动后的文件路径
    """
    return func.__move_to(__src_path, __dst_path, __cover)


def get_free_space_mb(_folder):
    """
    获取磁盘剩余空间
    Args:
        _folder: 文件夹路径
    Returns:
        磁盘剩余空间
    """
    return func.__get_free_space_mb(_folder)


def get_file_size(_path):
    """
    获取文件大小
    Args:
        _path: 文件路径
    Returns:
        文件大小
    """
    return func.__get_file_size(_path)


def init_vpn(_name, _user, _password, _secret):
    """
    初始化VPN工具类
    Args:
        _name: VPN名称
        _user: 用户名
        _password: 密码
        _secret: 密钥
    Returns:
        VPN工具类
    """
    global vpn
    vpn = vpn or VPNHelper(_name, _user, _password, _secret)
    console(vpn)
    return vpn


def init_ftp(_host, _port, _user, _passwd, _debug_lv=0, _buf_size=1024 * 1024):
    """
    初始化FTP工具类
    Args:
        _host: 主机
        _port: 端口
        _user: 用户名
        _passwd: 密码
        _debug_lv: 调试等级
        _buf_size: 缓冲区大小
    Returns:
        FTP工具类
    """
    global ftp
    ftp = ftp or FTPHelper(_host, _port, _user, _passwd, _debug_lv, _buf_size)
    console(ftp)
    return ftp


def init_ssh(_host, _port, _user, _passwd):
    """
    初始化SSH工具类
    Args:
        _host: 主机
        _port: 端口
        _user: 用户名
        _passwd: 密码
    Returns:
        SSH工具类
    """
    global ssh
    ssh = ssh or SSHHelper(_host, _port, _user, _passwd)
    console(ssh)
    return ssh


def init_cdn_flush(_url, _headers, _user, _pass, _pad, _path=None, _email=None):
    """
    初始化CDN刷新工具类
    Args:
        _url: 刷新地址
        _headers: 请求头
        _user: 用户名
        _pass: 密码
        _pad: 填充
        _path: 路径
        _email: 邮箱
    Returns:
        CDN刷新工具类
    """
    global flush
    flush = flush or CDNFlushHelper(_url, _headers, _user, _pass, _pad, _path, _email)
    console(flush)
    return flush


def init_svn(_user, _password, _path, _clean_path=None):
    """
    初始化SVN工具类
    Args:
        _user: 用户名
        _password: 密码
        _path: SVN路径
        _clean_path: 清理路径
    Returns:
        SVN工具类
    """
    global svn
    svn = svn or SVNHelper(_user, _password, _path, _clean_path)
    console(svn)
    return svn


def init_unity(_sysparams, _log, _build_target):
    """
    初始化Unity工具类
    Args:
        _sysparams: 系统参数
        _log: 日志路径
        _build_target: 构建目标
    Returns:
        Unity工具类
    """
    global unity
    unity = unity or UnityHelper(_sysparams, _log, _build_target)
    console(unity)
    return unity


def init_jar(_bt_jar, _us_jar):
    """
    初始化Jar工具类
    Args:
        _bt_jar: BundleTool Jar 路径
        _us_jar: UploadSymbols Jar 路径
    Returns:
        Jar工具类
    """
    global jar
    jar = jar or JarHelper(_bt_jar, _us_jar)
    console(jar)
    return jar


def init_tail(_log):
    """
    初始化Tail工具类
    Args:
        _log: 日志路径
    Returns:
        Tail工具类
    """
    global tail
    tail = tail or TailHelper(_log)
    console(tail)
    return tail


def init_xcode(_xcode_project):
    """
    初始化XCode工具类
    Args:
        _xcode_project: XCode工程路径
    Returns:
        XCode工具类
    """
    global xcode
    xcode = xcode or XCodeHelper(_xcode_project)
    console(xcode)
    return xcode


def init_gradle(_gradle_path, _android_project_path):
    """
    初始化Gradle工具类
    Args:
        _gradle_path: Gradle路径
        _android_project_path: Android工程路径
    Returns:
        Gradle工具类
    """
    global gradle
    gradle = gradle or GradleHelper(_gradle_path, _android_project_path)
    console(gradle)
    return gradle


def init_cos(_secretId, _secretKey, _bucket, _region):
    """
    初始化COS工具类
    Args:
        _secretId: secretId
        _secretKey: secretKey
        _bucket: bucket
        _region: region
    Returns:
        COS工具类
    """
    global cos
    cos = cos or COSHelper(_secretId, _secretKey, _bucket, _region)
    console(cos)
    return cos


def init_aws():
    """
    初始化AWS工具类
    Returns:
        AWS工具类
    """
    global aws
    aws = aws or AWSHelper()
    console(aws)
    return aws
