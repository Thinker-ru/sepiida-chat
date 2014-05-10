from django.conf.urls import patterns, include, url


urlpatterns = patterns('sepiida_chat.views',
    url('^send/$',      'send', name='send'),
    url('^widget\.js$', 'js',   name='js'),
)
