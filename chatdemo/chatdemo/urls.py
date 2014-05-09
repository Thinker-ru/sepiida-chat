from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import sepiida_chat

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chatdemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += sepiida_chat.urls.urlpatterns
