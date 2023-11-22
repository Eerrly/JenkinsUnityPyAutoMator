import os
import shutil
import sys
import zipfile
import ctypes
import platform


def __console(_message, *_params):
    """
    控制台输出
    Args:
        _message: 输出信息
        *_params: 输出参数
    """
    print((_message % _params) if len(_params) > 0 else _message)
    sys.stdout.flush()


def __unzip(_src_path, _dst_path=None):
    """
    解压文件
    Args:
        _src_path: 源文件路径
        _dst_path: 目标文件路径
    Returns:
        解压后的文件路径
    """
    if not _src_path.endswith(".apks") and not _src_path.endswith(".zip"):
        raise Exception("%s not an extractable file!" % _src_path)
    _dst_path = ".".join(_src_path.split(".")[0:-1]) if _dst_path is None else _dst_path
    if os.path.exists(_dst_path):
        shutil.rmtree(_dst_path)
    with zipfile.ZipFile(_src_path, "r", zipfile.ZIP_DEFLATED) as z_file:
        z_file.extractall(_dst_path)
    return _dst_path


def __zip(_src_path, _dst_path=None):
    """
    压缩文件
    Args:
        _src_path: 源文件路径
        _dst_path: 目标文件路径
    Returns:
        压缩后的文件路径
    """
    _dst_path = _dst_path if (_dst_path is not None and _dst_path.endswith(".zip")) else (_src_path + ".zip")
    if os.path.exists(_dst_path):
        os.remove(_dst_path)
    with zipfile.ZipFile(_dst_path, "w", zipfile.ZIP_DEFLATED) as z_file:
        for path, dir_names, file_names in os.walk(_src_path):
            f_path = path.replace(_src_path, "")
            for file_name in file_names:
                z_file.write(os.path.join(path, file_name), os.path.join(f_path, file_name))
    return _dst_path


def __copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False):
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
        目标文件夹
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.islink(srcname):
                linkto = os.readlink(srcname)
                if symlinks:
                    os.symlink(linkto, dstname)
                    shutil.copystat(srcname, dstname, follow_symlinks=not symlinks)
                else:
                    if not os.path.exists(linkto) and ignore_dangling_symlinks:
                        continue
                    if os.path.isdir(srcname):
                        __copytree(srcname, dstname, symlinks, ignore,
                                   copy_function)
                    else:
                        copy_function(srcname, dstname)
            elif os.path.isdir(srcname):
                __copytree(srcname, dstname, symlinks, ignore, copy_function)
            else:
                copy_function(srcname, dstname)
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))
    return dst


def __move_to(__src_path, __dst_path, __cover=False):
    """
    移动文件
    Args:
        __src_path: 源文件路径
        __dst_path: 目标文件路径
        __cover: 是否覆盖
    Returns:
        目标文件路径
    """
    __src_path = __src_path.replace("\\", "/")
    __dst_path = __dst_path.replace("\\", "/")
    if os.path.exists(__src_path):
        __dst_dir = os.path.dirname(__dst_path)
        if not os.path.exists(__dst_dir):
            os.makedirs(__dst_dir)
        if os.path.isdir(__src_path):
            if __cover:
                __copytree(__src_path, __dst_path)
            else:
                if os.path.exists(__dst_path):
                    shutil.rmtree(__dst_path)
                shutil.copytree(__src_path, __dst_path)
        elif os.path.isfile(__src_path):
            if os.path.exists(__dst_path):
                os.remove(__dst_path)
            shutil.copyfile(__src_path, __dst_path)
        else:
            raise Exception("cannot copy %s!" % __src_path)
    else:
        __console("cannot find %s!" % __src_path)
    __console("copy '%s' to '%s' ", __src_path, __dst_path)
    return __dst_path


def __get_free_space_mb(folder):
    """
    获取磁盘剩余空间
    Args:
        folder: 文件夹
    Returns:
        磁盘剩余空间
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 1024 / 1024


def __format_size(bytes):
    """
    格式化文件大小
    Args:
        bytes: 文件大小
    Returns:
        格式化后的文件大小
    """
    bytes = float(bytes)
    KB = bytes / 1024

    if KB >= 1024:
        M = KB / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % G
        else:
            return "%fM" % M
    else:
        return "%fKB" % KB


def __get_file_size(path):
    """
    获取文件大小
    Args:
        path: 文件路径
    Returns:
        文件大小
    """
    try:
        size = os.path.getsize(path)
        return __format_size(size)
    except Exception as err:
        __console(err)
        return float(-1)
