# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
from django.template import loader


__all__ = [
    'process_sms_notice',
]


def process_sms_notice(request):
    ''' Process SMS notice from sms paltform.'''

    if request.method == 'GET':
        context = {}
        get_data = request.GET.copy()
        if (get_data['do'] == 'notice') and ('success' in get_data):
            # Fail to send short message.
            if get_data['success'] == 0:
                context.update({
                    're': False,
                    'msg': get_data['desc']
                })
        elif (get_data['do'] == 'sms') and ('content' in get_data) and \
            ('mobile' in get_data):
            context.update({
                're': True,
                'mobile': get_data['mobile'],
                'content': get_data['content'],
            })
        if context:
            admin_mails = [ad[1] for ad in settings.ADMINS]
            subject = u'短信平台信息'
            content = loader.render_to_string('email/sms_notice.html', context)
            # send notice mail(subject, content, admin_mails)

        return HttpResponse('received')
