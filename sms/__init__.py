# -*- coding: utf-8 -*-

import urllib2
import json
from urllib import urlencode

from django.conf import settings
from django.template import loader

from sms.sms_settings import SMS_PLATFORM, SMS_PRODUCT_TYPE, SMS_REMAIN_COUNT
from sms.sms_settings import ERR_CODE, SMS_CONTENT_PREFIX, ID_CODE_CONTENT


__all__ = [
    'SMS',
]

HTTP_TIMEOUT = 10

class SMS(object):
    ''' SMS class to send short message.
    send short message method:
        send_id_code()
        send_realtime_sms()
        send_sms()
    Parameters are: phone number(can be number or string or a list of number) 
                    and message content(must be *unicode* string).
    Example:
    s = SMS()
    s.send_sms(13888888888, 'Hi there!')
    '''

    def __init__(self):
        self.name = SMS_PLATFORM['name']
        self.api_key = SMS_PLATFORM['api_key']
        self.send_url = SMS_PLATFORM['sms_send_url']


    def _http_get(self, url, data, parse=True):
        req = urllib2.Request('%s?%s' % (url, urlencode(data)))
        self.http_add_header(req)
        res = urllib2.urlopen(req, timeout=HTTP_TIMEOUT).read()
        if parse:
            return json.loads(res)
        return res

    def _http_post(self, url, data, parse=True):
        req = urllib2.Request(url, data=urlencode(data))
        self.http_add_header(req)
        res = urllib2.urlopen(req, timeout=HTTP_TIMEOUT).read()
        if parse:
            return json.loads(res)
        return res

    def http_add_header(self, req):
        ''' Add http headers.'''

        pass

    def _send_sms(self, product_type, phone_list, content):
        phone_list = phone_list if isinstance(phone_list, list) else [phone_list, ]
        phone_len = len(phone_list)
        cnt = phone_len / 100 + 1
        for i in xrange(cnt):
            phone = phone_list[i*100:(i+1)*100]
            phone_len = len(phone)

            if phone_len < 20:
                send = self._http_get
            elif phone_len < 100:
                send = self._http_post
            phone_num = ','.join(map(str, phone))
            data = {
                'k': self.api_key,
                'r': 'json',
                'p': product_type,
                't': phone_num,
                'c': content.encode('utf-8'),
            }
            res = send(self.send_url, data)
            self._check_response(product_type, res)
        return res

    def _check_response(self, product_type, res):
        ''' Check the response of SMS platform.'''
        err = False
        if product_type == SMS_PRODUCT_TYPE['tuixin']:
            t = u'实时短信'
        elif product_type == SMS_PRODUCT_TYPE['tuixin_diy']:
            t = u'普通短信'
        if isinstance(res, dict):
            remain_count = res.get('remain_count', None)
            if (remain_count is not None) and (remain_count < SMS_REMAIN_COUNT):
                err = True
            if res['err_code'] != 0:
                err = True
        if err:
            admin_mails = [ad[1] for ad in settings.ADMINS]
            subject = u'短信平台信息'
            context = {
                'sms_type': t,
                'sms_remain_count': res.get('remain_count', None),
                'err_msg': ERR_CODE[res['err_code']],
                'message': res['err_msg'],
            }
            content = loader.render_to_string('email/sms_status.html', context)
            # send notice mail(subject, content, admin_mails)


    def send_id_code(self, phone, content):
        ''' Send identifying code to identify.'''

        content = SMS_CONTENT_PREFIX + ID_CODE_CONTENT  + content
        self._send_sms(SMS_PRODUCT_TYPE['tuixin'], phone, content)

    def send_rt_sms(self, phone, content):
        ''' Send realtime short message to phone user.'''

        content = SMS_CONTENT_PREFIX + content
        self._send_sms(SMS_PRODUCT_TYPE['tuixin'], phone, content)

    def send_sms(self, phone, content):
        ''' Send simple short message to phone user. '''

        content = SMS_CONTENT_PREFIX + content
        self._send_sms(SMS_PRODUCT_TYPE['tuixin_diy'], phone, content)

