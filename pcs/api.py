#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlencode
import os
import pdb
import json

import requests

api_template = 'https://pcs.baidu.com/rest/2.0/pcs/{0}'

class PCS(object):
    def __init__(self, access_token, api_template=api_template):
        self.access_token = access_token
        self.api_template = api_template

    def info(self, **kwargs):
        """获取当前用户空间配额信息.

        >>> access_token = '3.3f56524f9e796191ce5baa84239feb15.2592000'
        >>> access_token += '.1380728222.570579779-1274287'
        >>> pcs = PCS(access_token)
        >>> pcs.info()
        {u'used': 1694, u'quota': 5368709120L, u'request_id': 3892923453L}

        """
        api = self.api_template.format('quota')
        params = {
            'method': 'info',
            'access_token': self.access_token
        }
        response = requests.get(api, params=params, **kwargs)
        return response.json()

    def upload(self, remote_path, file_content, ondup='', **kwargs):
        """上传单个文件（<2G）.
        remote_path 必须以 /apps/ 开头

        >>> access_token = '3.3f56524f9e796191ce5baa84239feb15.2592000'
        >>> access_token += '.1380728222.570579779-1274287'
        >>> pcs = PCS(access_token)
        >>> pcs.upload('/apps/test_sdk/test.text', 'abc')
        {u'ctime': 1378289710, u'request_id': 3272051612L,
        u'fs_id': 1382134047, u'mtime': 1378289710,
        u'path': u'/apps/test_sdk/test.text',
        u'md5': u'900150983cd24fb0d6963f7d28e17f72', u'size': 3}
        >>> pcs.upload('/apps/test_sdk/test.text', 'abc')
        {u'error_code': 31061, u'error_msg': u'file already exists',
        u'request_id': 2836896020L}
        >>> pcs.upload('/apps/test_sdk/test.text', 'abc', ondup='overwrite')
        {u'ctime': 1378289935, u'request_id': 1863510702,
        u'fs_id': 290509500, u'mtime': 1378289935,
        u'path': u'/apps/test_sdk/test.text',
        u'md5': u'900150983cd24fb0d6963f7d28e17f72', u'size': 3}
        >>> pcs.upload('/apps/test_sdk/test.text', 'abc', ondup='newcopy')
        {u'ctime': 1378289935, u'request_id': 1963565646, u'fs_id': 1597681181,
        u'mtime': 1378289935,
        u'path': u'/apps/test_sdk/test_20130904181855.text',
        u'md5': u'900150983cd24fb0d6963f7d28e17f72', u'size': 3}

        """
        params = {
            'method': 'upload',
            'access_token': self.access_token,
            'path': remote_path,
            'ondup': ondup
        }
        api = '%s?%s' % (self.api_template.format('file'), urlencode(params))
        files = {'file': file_content}
        response = requests.post(api, files=files, **kwargs)
        return response.json()

    def upload_tmpfile(self, file_content, **kwargs):
        """.

        >>> access_token = '3.3f56524f9e796191ce5baa84239feb15.2592000'
        >>> access_token += '.1380728222.570579779-1274287'
        >>> pcs = PCS(access_token)
        >>> pcs.upload_tmpfile('abc')
        {u'request_id': 823641176, u'md5': u'900150983cd24fb0d6963f7d28e17f72'}
        >>> pcs.upload_tmpfile('efg')
        {u'request_id': 4011691380L, u'md5': u'7d09898e18511cf7c0c1815d07728d23'}

        """
        params = {
            'method': 'upload',
            'access_token': self.access_token,
            'type': 'tmpfile',
        }
        api = '%s?%s' % (self.api_template.format('file'), urlencode(params))
        files = {'file': file_content}
        response = requests.post(api, files=files, **kwargs)
        return response.json()

    def upload_superfile(self, remote_path, block_list, ondup='', **kwargs):
        """

        >>> access_token = '3.3f56524f9e796191ce5baa84239feb15.2592000'
        >>> access_token += '.1380728222.570579779-1274287'
        >>> pcs = PCS(access_token)
        >>> pcs.upload_tmpfile('abc')
        {u'request_id': 823641176, u'md5': u'900150983cd24fb0d6963f7d28e17f72'}
        >>> pcs.upload_tmpfile('efg')
        {u'request_id': 4011691380L, u'md5': u'7d09898e18511cf7c0c1815d07728d23'}
        >>> pcs.upload_superfile('/apps/test_sdk/superfile.txt',
        ... [u'900150983cd24fb0d6963f7d28e17f72',
        ... u'7d09898e18511cf7c0c1815d07728d23'])
        {u'ctime': 1378290352, u'request_id': 3271648239L, u'fs_id': 333508963,
        u'mtime': 1378290352, u'path': u'/apps/test_sdk/superfile.txt',
        u'md5': u'cf84dbd71b3742e0237589fcf4f8ed4e', u'size': 6}

        """
        # pdb.set_trace()
        params = {
            'method': 'createsuperfile',
            'access_token': self.access_token,
            'path': remote_path,
            'ondup': ondup
        }
        data = {
                'param': json.dumps({'block_list': block_list}),
        }
        api = '%s?%s' % (self.api_template.format('file'), urlencode(params))
        response = requests.post(api, data=data, **kwargs)
        return response.json()

    def download(self, remote_path, **kwargs):
        """

        >>> access_token = '3.3f56524f9e796191ce5baa84239feb15.2592000'
        >>> access_token += '.1380728222.570579779-1274287'
        >>> pcs = PCS(access_token)
        >>> pcs.download('/apps/test_sdk/superfile.txt')
        'abcefg'

        """
        params = {
            'method': 'download',
            'access_token': self.access_token,
            'path': remote_path,
        }
        api = self.api_template.format('file')
        response = requests.get(api, params=params, **kwargs)
        return response.content

if __name__ == '__main__':
    # pdb.set_trace()
    pass
