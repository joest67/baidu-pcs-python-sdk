#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time


def get_new_access_token(refresh_token, client_id, client_secret,
                         scope=None, **kwargs):
    """使用 Refresh Token 刷新以获得新的 Access Token.

    :param refresh_token: 用于刷新 Access Token 用的 Refresh Token；
    :param client_id: 应用的 API Key；
    :param client_secret: 应用的 Secret Key;
    :param scope: 以空格分隔的权限列表，若不传递此参数，代表请求的数据访问
                  操作权限与上次获取 Access Token 时一致。通过 Refresh Token
                  刷新 Access Token 时所要求的 scope 权限范围必须小于等于上次
                  获取 Access Token 时授予的权限范围。 关于权限的具体信息请参考
                  “ `权限列表`__ ”。
    :return: Response 对象

    关于 ``response.json()`` 字典的内容所代表的含义，
    请参考 `相关的百度帮助文档`__ 。

     __ http://developer.baidu.com/wiki/index.php?title=docs/oauth/baiduoauth/list
     __ http://developer.baidu.com/wiki/index.php?title=docs/oauth/refresh
    """
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'netdisk',
    }
    if scope:
        data['scope'] = scope
    url = 'https://openapi.baidu.com/oauth/2.0/token'
    return requests.post(url, data=data)


def create_access_token(client_id, client_secret, scope=None):
    """
    1. call tools.create_access_token(`client_id`, `client_secret`)
    2. open website `http://openapi.baidu.com/device` in browser
    3. enter code `xxx`, click authorized
    """

    data = {
        'response_type': 'device_code',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    if scope:
        data['scope'] = scope
    url = 'https://openapi.baidu.com/oauth/2.0/device/code'
    enter_code_website = 'http://openapi.baidu.com/device'
    retries = 10
    res = requests.post(url, data=data)
    if res.status_code / 100 == 2:
        res = res.json()

    if res and res.get('user_code'):
        user_code = res.get('user_code')
        device_code = res.get('device_code')
        expires_in = res.get('expires_in')
        interval = res.get('interval')
        print '\nopen {}, enter the user_code {} in {}s\n'.format(
            enter_code_website, user_code, expires_in)
    else:
        raise Exception('Get user_code error {}, {}'.format(res['error'], res['error_description']))

    while retries > 0:
        res = check_authentication(device_code, client_id, client_secret)
        if 'access_token' in res:
            access_token = res['access_token']
            refresh_token = res['refresh_token']
            print 'success: access_token={}, refresh_token={}'.format(
                access_token, refresh_token)

            return access_token, refresh_token
        else:
            error_msg = 'Get access_token error {}, {}\n'.format(res['error'], res['error_description'])
            if retries > 1:
                retries -= 1
                print error_msg
            else:
                raise Exception(error_msg)
        time.sleep(interval + 5)


def check_authentication(device_code, client_id, client_secret):
    data = {
        'grant_type': 'device_token',
        'code': device_code,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    url = 'https://openapi.baidu.com/oauth/2.0/token'
    res = requests.post(url, data=data)
    return res.json()
