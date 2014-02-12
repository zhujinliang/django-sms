# -*- coding: utf-8 -*-

from django.conf import settings

# Tui3.com platform
SMS_PLATFORM_TUI3 = {
    'name': 'Tui3',
    'api_key': 'YOUR API KEY HERER',
    'sms_send_url': 'http://www.tui3.com/api/send/',
    'site_url': 'http://tui3.com',
}
SMS_PRODUCT_TYPE_TUI3= {
    'tuixin': 1,
    'tuixin_diy': 2
}

ERR_CODE = {
    0: u'正常',
    1: u'服务未开通',
    2: u'非法KEY',
    3: u'IP地址非法',
    4: u'无合法接收手机号码',
    5: u'有违禁内容，拒绝发送',
    6: u'短信格式未备案（实时短信）',
    7: u'发送短信内容不符合备案格式(实时短信)',
    8: u'余额不足',
    9: u'批量处理超过限额',
    10: u'参数不正确',
    11: u'发送过于频繁，超过频率限制'
}

SMS_PLATFORM = getattr(settings, 'SMS_PLATFORM', SMS_PLATFORM_TUI3)
SMS_PRODUCT_TYPE = getattr(settings, 'SMS_PRODUCT_TYPE', SMS_PRODUCT_TYPE_TUI3)

SMS_REMAIN_COUNT = getattr(settings, 'SMS_REMAIN_COUNT', 100)
SMS_CONTENT_PREFIX = getattr(settings, 'SMS_CONTENT_PREFIX', u'')
ID_CODE_CONTENT = u'您的验证码为：'
