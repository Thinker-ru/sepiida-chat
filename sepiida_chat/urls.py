from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url('', name="")
)

urlpatterns += sepiida_chat.urls.urlpatterns
