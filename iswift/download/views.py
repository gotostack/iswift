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


import os.path

from django.core.servers.basehttp import FileWrapper
from django.http import Http404
from django.http import HttpResponse


FILE_FOLDER = '/home/swift/webroot/iswift/userdownload/'


def tarball(request, release):
    file_name = 'dj-download-%s.tar.gz' % release
    file_path = os.path.join(FILE_FOLDER, file_name)
    try:
        tarball_file = open(file_path)
    except IOError:
        raise Http404
    wrapper = FileWrapper(tarball_file)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Encoding'] = 'utf-8'  # 设置该值gzip中间件就会直接返回而不进行后续操作
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    return response
