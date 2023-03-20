from enum import Enum


# unity build target
class Build(Enum):
    PC = "-buildTarget Win"
    Android = "-buildTarget Android"
    IOS = "-buildTarget iOS"


class UploadType(Enum):
    Main = "Main"
    Patch = "Patch"
    Zip = "Zip"
    Merger = "Merger"
    Version = "Version"


class PatchType(Enum):
    All = "All"
    WithoutV = "WithOutV"
    V = "V"


# release ftp
CONST_FTP_BUF_SIZE = 1048576
# CONST_FTP_HOST = ""
# CONST_FTP_USERNAME = ""
# CONST_FTP_PASSWORD = ""

# # fake ftp
# CONST_FAKE_HOST = "192.168.10.231"
# CONST_FAKE_PORT = 22
# CONST_FAKE_USERNAME = "root"
# CONST_FAKE_PASSWORD = "123456"

# vpn
CONST_VPN_NAME = ""
CONST_VPN_USERNAME = ""
CONST_VPN_PASSWORD = ""
CONST_VPN_SECRET = ""

# svn (common)
CONST_SVN_USERNAME = ""
CONST_SVN_PASSWORD = ""

# keystore
# CONST_STORE_PASS = ""
# CONST_KEY_ALIAS = ""
# CONST_KEY_PASS = ""

# cdn flush (kr)
CDN_FLUSH_URL = ""
CDN_FLUSH_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
CDN_FLUSH_USER = ""
CDN_FLUSH_PASS = ""
CDN_FLUSH_PAD = ""
CDN_FLUSH_EMAIL = ""

WIN_MAX_DISK = 5
MAC_MAX_DISK = 3
