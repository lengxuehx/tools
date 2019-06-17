# -*- coding: utf-8 -*-

import requests
import logging
import time
from urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter

from conf import settings

logger = logging.getLogger('utils.rest')


def try_request(
        method, url, try_count=None, timeout=None, data=None, status_forcelist=None, json=None,
        backoff_factor=None, **kwargs
):
    """
    尝试多次发送请求

    :param method: http方法
    :param url: http请求地址
    :param try_count: 尝试次数
    :param timeout: 每次尝试的超时时间
    :param data: 提交的数据
    :param json: 提交的数据
    :param backoff_factor: 重试时，等待时间按此参数递增
    :param status_forcelist: 当返回请求的http状态在该列表中时，才认为出错并进行下一次尝试
    :return:
    """
    def get_backoff_time(backoff_factor, total_retry_count):
        backoff_value = backoff_factor * (2 ** (total_retry_count - 1))
        return min(120, backoff_value)

    backoff_factor = backoff_factor or 0.1
    status_forcelist = status_forcelist or [500, 502, 503, 504]
    try_count = try_count or 2
    timeout = timeout or 3
    s = requests.Session()
    ret = None
    for i in range(try_count):
        try:
            ret = s.request(method=method, url=url, timeout=timeout, data=data, json=json, **kwargs)
            if ret.status_code in status_forcelist:
                if i < try_count-1:
                    logger.warning(
                        'remote server error, try again, url: %s, status: %s, reason: %s,  ...' % (
                           url,  ret.status_code, ret.text)
                    )
                    time.sleep(
                        get_backoff_time(backoff_factor=backoff_factor, total_retry_count=i+1)
                    )
                continue
            else:
                break
        except requests.exceptions.ConnectTimeout as e:
            if i < try_count - 1:
                logger.warning('failed to connect to server, url: %s,  fail reason: connection timeout, try again ...' % url)
                time.sleep(
                    get_backoff_time(backoff_factor=backoff_factor, total_retry_count=i + 1)
                )
                continue
            else:
                raise

    return ret


def try_get(url, try_count=None, timeout=None, status_forcelist=None, backoff_factor=None, **kwargs):
    return try_request(
        'GET', url=url, try_count=try_count, timeout=timeout, status_forcelist=status_forcelist,
        backoff_factor=backoff_factor, **kwargs
    )


def try_post(
        url, try_count=None, timeout=None, data=None, json=None, status_forcelist=None, backoff_factor=None, **kwargs
):
    """
    务必保证操作是幂等的
    """
    return try_request(
        'POST', url=url, try_count=try_count, timeout=timeout, data=data,
        status_forcelist=status_forcelist, json=json, backoff_factor=backoff_factor, **kwargs
    )


