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

from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url


urlpatterns = patterns(
    'footerpages.views',
    url(r'^iscprght/$', 'iscprght'),
    url(r'^install/$', 'install'),
    url(r'^mobile/$', 'mobile'),
    url(r'^pricing/$', 'pricing'),
    url(r'^teams/$', 'teams'),
    url(r'^tour/$', 'tour'),
    url(r'^terms/$', 'terms'),
    url(r'^userhelp/$', 'userhelp'),
    url(r'^jobs/$', 'jobs'),
    url(r'^developers/$', 'developers'),
    url(r'^about/$', 'about'),
    url(r'^news/$', 'news'),

    url(r'^display/$', 'display_meta'),
    url(r'^contact/$', 'contact'),

    url(r'^register/$', 'register_view'),
)
