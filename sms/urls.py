from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sms.views',
	url(r'^notice/$', 'process_sms_notice'),
)
