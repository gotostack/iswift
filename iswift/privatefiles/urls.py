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
    'privatefiles.views',
    url(r'^privatefiles/$',
        'privatefiles',
        name='privatefiles_home'),

    url(r'^privatefiles/(?P<containernames>.*)/download/(?P<objects>.*)/$',
        'download_file',
        name='privatefiles_download_file'),
    url(r'^privatefiles/folder/create/(?P<parent_folder>(.+/)+)?$',
        'sql_create_folder'),
    url(r'^privatefiles/file/create/(?P<parent_folder>(.+/)+)?$',
        'sql_create_file'),
    url(r'^privatefiles/folderfile/delete/(?P<parent_folder>(.+/)+)?$',
        'sql_delete_folderORfile'),
    url(r'^privatefiles/folderfile/update/(?P<parent_folder>(.+/)+)?$',
        'sql_update_folderORfile'),

    url(r'^privatefiles/(?P<parent_folder>(.+/)+)?$',
        'sub_folder',
        name='privatefiles_subfolder'),
)
