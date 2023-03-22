# -*- coding: UTF-8 -*-
import sys
from enum import Enum

import requests


class FlushType(Enum):
    Item = "item"
    All = "all"


class CDNFlushHelper:
    """ 刷新CDN 工具类 """
    def __init__(self, _url, _headers, _user, _pass, _pad, _path=None, _email=None):
        self.url = _url
        self.headers = _headers
        self.user = _user
        self.passwd = _pass
        self.pad = _pad
        self.path = _path
        self.email = _email

    def __str__(self):
        return "cdn flush information >\nurl:%s\nheaders:%s\nuser:%s\npassword:******\npad:%s\npath:%s\nemail:%s" % (self.url, self.headers, self.user, self.pad, self.path, self.email)

    def __request_post(self, _url, _headers, _data):
        response = requests.request("POST", _url, headers=_headers, data=_data)
        if "200" in response.text:
            sys.stdout.write("flush successful !")
            sys.stdout.flush()
        else:
            raise Exception(response.text)

    def flush(self):
        """ 刷新
        刷新CDN 通过requests的方式
        """
        __type = FlushType.All if self.path is None else FlushType.Item
        __data = ["user=" + self.user, "pass=" + self.passwd, "pad=" + self.pad, "type=" + __type.value]
        if self.path is not None:
            __data.append("path=" + self.path)
        if self.email is not None:
            __data.append("mailTo=" + self.email)
        payload = "&".join(__data)

        sys.stdout.write(payload)
        sys.stdout.flush()

        self.__request_post(self.url, self.headers, payload)
