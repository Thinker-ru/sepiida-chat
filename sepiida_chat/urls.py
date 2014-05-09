from django.conf.urls import patterns, include, url

urlpatterns = patterns('sepiida_chat.views',
    url('^$', 'index', name='index'),
)
