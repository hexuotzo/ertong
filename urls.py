# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ertong/', include('ertong.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'order.views.index'),   #主页
    (r'^project/(?P<pid>.*)/','order.views.to_project'),  #项目页
    (r'^project/','order.views.project'),  #项目分类展示
    (r'^order/','order.views.get_order'),   #提交订单
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': 'media','show_indexes':True}),
    (r'^img/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
)
