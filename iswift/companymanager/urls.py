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
    'companymanager.views',
    url(r'/companylogin/$', 'companylogin', name='登录'),
    url(r'/d/data/cmpstorage/', 'storagedata', name='storagedata'),
    url(r'/companyadmin/$', 'companymanage', name='主界面'),
    url(r'/companyadmin/visitsnum/$', 'visitsnum', name='访问量'),
    url(r'/companyadmin/loginsnum/$', 'loginsnum', name='登录详情'),
    url(r'/companyadmin/publicfolder/$', 'publicfolder', name='公共文档'),
    url(r'/companyadmin/publicfile/$', 'publicfile', name='公共文件'),
    url(r'/companyadmin/allocate/$', 'allocate', name='分配空间'),
    url(r'/companyadmin/spaceadmin/$', 'spaceadmin', name='管理空间'),
    url(r'/companyadmin/orgs/$', 'orgs', name='组织机构'),
    url(r'/companyadmin/orgs/modify/$', 'orgsmodify', name='组织机构'),
    url(r'/companyadmin/rights/$', 'rights', name='权限'),
    url(r'/companyadmin/spaceapply/$', 'spaceapply', name='申请新空间'),
    url(r'/companyadmin/versionapply/$', 'versionapply', name='申请版本级别'),
)
