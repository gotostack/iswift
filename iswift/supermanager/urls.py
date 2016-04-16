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
    'supermanager.views',
    url(r'/superlogin/$', 'superlogin', name='登录'),
    url(r'/superadmin/$', 'supermanage', name='super-admin'),
    url(r'/d/data/networkdata/', 'networkdata', name='networkdata'),
    url(r'/d/data/random/', 'fadecpudata', name='fade-cpu-data'),
    url(r'/d/data/cmpspaces/', 'cmpspaces', name='cmpspaces'),
    url(r'/superadmin/suptenants/', 'suptenants', name='suptenants'),
    url(r'/superadmin/spaces/', 'storate_spaces', name='storate_spaces'),
    url(r'/superadmin/storagenode/', 'storage_nodes', name='storage_nodes'),
    url(r'/superadmin/belance/', 'storage_balance', name='storage_balance'),
)
