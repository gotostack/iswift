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
    url(r'^$', 'iswift.azureviews.home', name='index'),

    url(r'^usermain/$', 'iswift.azureviews.usermain'),

    url(r'^login/$', 'iswift.azureviews.home'),
    url(r'^logout/', 'iswift.azureviews.logout_view'),

    url(r'^mng', include('iswift.supermanager.urls')),
    url(r'^mng', include('iswift.companymanager.urls')),

    url(r'', include('iswift.footerpages.urls')),

    url(r'^auth/$', 'iswift.azureviews.authlogin'),
    url(r'^auth/', include('openstack_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<container>.*)/objectlist/$',
        'iswift.azureviews.container_objects',
        name='container_objectlist'),
    url(r'^(?P<container>.*)/objectlist/'
        '(?P<containername>.*)/(?P<objects>.*)/objectstat/$',
        'iswift.azureviews.objects_stat',
        name='objects_stat'),

    url(r'^download/(?P<containernames>.*)/(?P<objects>.*)/$',
        'iswift.azureviews.download_object',
        name='download_object'),

    url(r'^container/create/$',
        'iswift.azureviews.create_container'),
    url(r'^(?P<container>.*)/objectcreate/',
        'iswift.azureviews.upload_a_object'),
    url(r'^(?P<container_name>.+?)/(?P<subfolder_path>(.+/)+)?upload$',
        'iswift.azureviews.upload_a_object',
        name='object_upload'),
)

# Development static app and project media serving using the staticfiles app.
# urlpatterns += static(settings.STATIC_URL ,
#     document_root = settings.STATIC_ROOT )

# Convenience function for serving user-uploaded media during
# development. Only active if DEBUG==True and the URL prefix is a local
# path. Production media should NOT be served by Django.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
