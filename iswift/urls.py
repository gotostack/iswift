#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'iswift.views.home', name='index'),
    url(r'^VerifyCode/$', 'iswift.views.VerifyCode', name='VerifyCode'),
    url(r'^userdashboard/$', 'iswift.views.usermain', name='userdashboard'),

    url(r'^login/$', 'iswift.views.home'),
    url(r'^logout/', 'iswift.views.logout_view'),

    url(r'^mng', include('iswift.supermanager.urls')),
    url(r'^mng', include('iswift.companymanager.urls')),

    url(r'', include('iswift.footerpages.urls')),

    url(r'^auth/$', 'iswift.views.authlogin'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('iswift.privatefiles.urls')),
    url(r'^mysharedfiles/$', 'iswift.views.mysharedfiles'),
    url(r'^deletedfiles/$', 'iswift.views.deletedfiles'),
    url(r'^filesversion/$', 'iswift.views.filesversion'),

    url(r'^userdashboard/(?P<containernames>.*)/download/(?P<objects>.*)/$',
        'iswift.views.download_file',
        name='download_file'),

    url(r'^userdashboard/folder/create/(?P<parent_folder>(.+/)+)?$',
        'iswift.views.sql_create_folder'),

    url(r'^userdashboard/file/create/(?P<parent_folder>(.+/)+)?$',
        'iswift.views.sql_create_file'),

    url(r'^userdashboard/folderfile/delete/(?P<parent_folder>(.+/)+)?$',
        'iswift.views.sql_delete_folderORfile'),

    url(r'^userdashboard/folderfile/update/(?P<parent_folder>(.+/)+)?$',
        'iswift.views.sql_update_folderORfile'),

    url(r'^userdashboard/(?P<parent_folder>(.+/)+)?$',
        'iswift.views.sub_folder',
        name='sub_folder'),

    url(r'^filesystem/filesearch/$',
        'iswift.views.filesearch'),
)

# Development static app and project media serving using the staticfiles app.
# urlpatterns += static(settings.STATIC_URL,
#     document_root = settings.STATIC_ROOT )

# Convenience function for serving user-uploaded media during
# development. Only active if DEBUG==True and the URL prefix is a local
# path. Production media should NOT be served by Django.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
