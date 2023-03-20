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


def console(_message, *_params):
    """ Console.

    Log Printing

    :param _message: Message
    :param _params: Params
    :return:
    """
    func.__console(_message, *_params)


def unzip(_src_path, _dst_path=None):
    """ Unpacking.

    UnPacking

    :param _src_path: Source Path
    :param _dst_path: Target Path
    :return:
    """
    return func.__unzip(_src_path, _dst_path)


def zip(_src_path, _dst_path=None):
    """ Packing.

    Packing

    :param _src_path: Source Path
    :param _dst_path: Target Path
    :return:
    """
    return func.__zip(_src_path, _dst_path)


def copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False):
    """ Copy Folder To.

    The original method will report an error if there is no target directory

    :param src:
    :param dst:
    :param symlinks:
    :param ignore:
    :param copy_function:
    :param ignore_dangling_symlinks:
    :return:
    """
    return func.__copytree(src, dst, symlinks, ignore, copy_function, ignore_dangling_symlinks)


def move(__src_path, __dst_path, __cover=False):
    """ Copy File or Folder To.

    Use [util copytree]
    The original method will report an error if there is no target directory

    :param __src_path: Source Path
    :param __dst_path: Target Path
    :param __cover: Use [util copytree] or Use [shutil copytree]
    :return:
    """
    return func.__move_to(__src_path, __dst_path, __cover)


def get_free_space_mb(_folder):
    """ Get Free Space Disk
    :param _folder: Folder
    :return: Return folder/drive free space (in bytes)
    """
    return func.__get_free_space_mb(_folder)


def get_file_size(_path):
    """ Get File Size
    :param _path: File Path
    """
    return func.__get_file_size(_path)


def init_vpn(_name, _user, _password, _secret):
    """ Init Vpn Class.

    Turn VPN on or off on Mac computers

    :param _name: VPN Name
    :param _user: VPN User
    :param _password: VPN Password
    :param _secret: VPN Secret
    :return: VPN Class
    """
    global vpn
    vpn = vpn or VPNHelper(_name, _user, _password, _secret)
    console(vpn)
    return vpn


def init_ftp(_host, _port, _user, _passwd, _debug_lv=0, _buf_size=1024 * 1024):
    """ Init FTP Class.

    Uploading with FTP

    :param _host: CDN HOST
    :param _port: CDN PORT
    :param _user: CDN User
    :param _passwd: CDN Password
    :param _debug_lv: Debug Log Level
    :param _buf_size: Uploading Max Buffer Size
    :return: FTP Class
    """
    global ftp
    ftp = ftp or FTPHelper(_host, _port, _user, _passwd, _debug_lv, _buf_size)
    console(ftp)
    return ftp


def init_ssh(_host, _port, _user, _passwd):
    """ Init SSH Class.

    Uploading with SFTP

    :param _host: CDN HOST
    :param _port: CDN PORT
    :param _user: CDN User
    :param _passwd: CDN Password
    :return: SSH Class
    """
    global ssh
    ssh = ssh or SSHHelper(_host, _port, _user, _passwd)
    console(ssh)
    return ssh


def init_cdn_flush(_url, _headers, _user, _pass, _pad, _path=None, _email=None):
    """ Init CDN Flush Class.

    Flush CDN (KR)

    :param _url: CDN Flush Url
    :param _headers: CDN Flush Url Headers
    :param _user: CDN Flush User
    :param _pass: CDN Flush Password
    :param _pad: CDN Flush PAD
    :param _path: CDN Flush Path (if want to flush item path)
    :param _email: Email for notification
    :return: CDN Flush Class
    """
    global flush
    flush = flush or CDNFlushHelper(_url, _headers, _user, _pass, _pad, _path, _email)
    console(flush)
    return flush


def init_svn(_user, _password, _path, _clean_path=None):
    """ Init SVN Class.

    Use SVN for cleanup, restore, update, and commit operations

    :param _user: SVN Account
    :param _password: SVN Password
    :param _path: SVN Project Path (Trunk_KR)
    :param _clean_path: SVN Project Clean Path (Trunk_KR/Client)
    :return: SVN Class
    """
    global svn
    svn = svn or SVNHelper(_user, _password, _path, _clean_path)
    console(svn)
    return svn


def init_unity(_sysparams, _log, _build_target):
    """ Init Unity Class.

    Use Unity for platforming, packaging, hot changes, variant collection

    :param _sysparams: Jenkins Parameter
    :param _log: Unity Project Log Path
    :param _build_target: Unity Platform Target
    :return: Unity Class
    """
    global unity
    unity = unity or UnityHelper(_sysparams, _log, _build_target)
    console(unity)
    return unity


def init_jar(_bt_jar, _us_jar):
    """ Init Jar Class.

    Mainly use jar for installation and export operation, you can also upload Bugly symbol

    :param _bt_jar: bundletool-all-1.6.1.jar Path
    :param _us_jar: buglyqq-upload-symbol.jar Path
    :return: Jar Class
    """
    global jar
    jar = jar or JarHelper(_bt_jar, _us_jar)
    console(jar)
    return jar


def init_tail(_log):
    """ Init Tail Class.

    Used to synchronize Unity's logs in real time

    :param _log: Unity Log File Path
    :return: Tail Class
    """
    global tail
    tail = tail or TailHelper(_log)
    console(tail)
    return tail


def init_xcode(_xcode_project):
    """ Init XCode Class.

    A series of operations used to build the IPA

    :param _xcode_project: XCode Project Path
    :return:
    """
    global xcode
    xcode = xcode or XCodeHelper(_xcode_project)
    console(xcode)
    return xcode


def init_gradle(_gradle_path, _android_project_path):
    """ Init Gradle Class

    Clean up and build android projects with Gradle

    :param _gradle_path: gradlew or gradlew.bat Path
    :param _android_project_path: Android Project Path
    :return: Gradle Class
    """
    global gradle
    gradle = gradle or GradleHelper(_gradle_path, _android_project_path)
    console(gradle)
    return gradle


def init_cos(_secretId, _secretKey, _bucket, _region):
    """ Init COScmd Class

    Use Tencent COS to upload resources to Tencent Cloud storage

    :param _secretId:secret id
    :param _secretKey:secret key
    :param _bucket:bucket
    :param _region:region
    """
    global cos
    cos = cos or COSHelper(_secretId, _secretKey, _bucket, _region)
    console(cos)
    return cos
