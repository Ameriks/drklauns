# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views import defaults as default_views


admin.site.site_header = "Dr.Klauns IT"
admin.site.site_title = "Dr.Klauns IT"
admin.site.index_title = "Dr.Klauns IT"
admin.site.disable_action('delete_selected')

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/kadmin/"), name='home'),
    url(r'^kadmin/', include(admin.site.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
