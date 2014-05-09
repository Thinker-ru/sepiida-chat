from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('chatdemo.views',
	url(r'^$', 'index'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat/', include('sepiida_chat.urls', 'chat')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
