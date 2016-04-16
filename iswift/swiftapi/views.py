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

import hashlib
import os

from django.http import Http404
from django.http import HttpResponse
from swiftclient import client as swiftclient
from swiftclient import exceptions as swift_expceptions

from keystoneclient.v2_0 import client

FILE_FOLDER = '/home/swift/webroot/iswift/userdownload/'

LOACL_AUTH_URL = 'http://127.0.0.1:5000/v2.0'


def get_connection(authurl,
                   user,
                   key,
                   retries=5,
                   preauthurl=None,
                   preauthtoken=None,
                   snet=False,
                   starting_backoff=1,
                   tenant_name=None,
                   os_options={},
                   auth_version="2.0"):
    connection = swiftclient.Connection(authurl,
                                        user,
                                        key,
                                        retries,
                                        preauthurl,
                                        preauthtoken,
                                        snet,
                                        starting_backoff,
                                        tenant_name,
                                        os_options,
                                        auth_version)
    return connection


def get_user_auth(user, key, tenant_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    AUTH = connection.get_auth()
    return AUTH


def get_container_list(user, key, tenant_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    container_list = connection.get_account()
    return container_list


def list_container_objects(user, key, tenant_name, container_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    container_objects_list = connection.get_container(container_name)
    return container_objects_list


def list_container_detail(user, key, tenant_name, container_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    container_detail = connection.head_container(container_name)
    return container_detail


def list_object_detail(user, key, tenant_name, container_name, object_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    object_detail = connection.head_object(container_name, object_name)
    return object_detail


def container_create(user, key, tenant_name, container_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    try:
        connection.put_container(container_name)
    except Exception:
        return False
    return True


def upload_object(user,
                  key,
                  tenant_name,
                  container_name,
                  object_name,
                  orig_file_name,
                  object_file):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    try:
        connection.put_object(container=container_name,
                              obj=object_name,
                              contents=object_file)
    except swift_expceptions.ClientException:
        return False
    return True


def get_object(user,
               key,
               tenant_name,
               container_name,
               object_name,
               meta_filename,
               size):
    try:
        connection = get_connection(
            authurl=LOACL_AUTH_URL,
            user=user,
            key=key, retries=5, preauthurl=None,
            preauthtoken=None, snet=False, starting_backoff=1,
            tenant_name=tenant_name, os_options={}, auth_version="2.0")
    except Exception:
        raise Http404
    try:
        objectheaderanddata = connection.get_object(container_name,
                                                    object_name)
    except Exception:
        raise Http404
    filename = meta_filename
    response = HttpResponse()
    safe_name = filename.replace(",", "").encode('utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s' % safe_name
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Length'] = size
    response.write(objectheaderanddata[1])
    return response


def copy_object(user,
                key,
                tenant_name,
                orig_container_name,
                orig_object_name,
                new_container_name,
                new_object_name):
    headers = {}
    headers["X-Copy-From"] = "/".join([orig_container_name, orig_object_name])
    try:
        connection = get_connection(
            authurl=LOACL_AUTH_URL,
            user=user,
            key=key, retries=5, preauthurl=None,
            preauthtoken=None, snet=False, starting_backoff=1,
            tenant_name=tenant_name, os_options={}, auth_version="2.0")
    except Exception:
        return False
    try:
        connection.put_object(new_container_name,
                              new_object_name,
                              None,
                              headers=headers)
    except Exception:
        return False
    return True


def container_update(user,
                     key,
                     tenant_name,
                     container_name,
                     new_container_name):
    headers = {}
    headers['X-Containers-Meta-Orig-name'] = new_container_name
    try:
        connection = get_connection(
            authurl=LOACL_AUTH_URL,
            user=user,
            key=key, retries=5, preauthurl=None,
            preauthtoken=None, snet=False, starting_backoff=1,
            tenant_name=tenant_name, os_options={}, auth_version="2.0")
    except Exception:
        return False
    connection.post_container(container_name, headers)
    return True


def object_update(user, key, tenant_name, container_name, obj, new_objname):
    headers = {}
    headers['X-Object-Name'] = new_objname
    try:
        connection = get_connection(
            authurl=LOACL_AUTH_URL,
            user=user,
            key=key, retries=5, preauthurl=None,
            preauthtoken=None, snet=False, starting_backoff=1,
            tenant_name=tenant_name, os_options={}, auth_version="2.0")
    except Exception:
        return False
    connection.post_object(container_name, obj, headers)
    return True


def delete_empty_container(user, key, tenant_name, container_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    try:
        connection.delete_container(container_name)
    except Exception:
        return False
    return True


def delete_an_objcte(user,
                     key,
                     tenant_name,
                     container_name,
                     object_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    try:
        connection.delete_object(container_name, object_name)
    except Exception:
        return False
    return True


def create_container_subfolder(user,
                               key,
                               tenant_name,
                               container_name,
                               folder_name):
    pass


def create_tenant(tenant_name,
                  tenant_description,
                  user_name,
                  user_password,
                  user_email):
    try:
        keystone = client.Client(username='adminUser',
                                 password='secretword',
                                 tenant_name='openstackDemo',
                                 auth_url=LOACL_AUTH_URL)
    except Exception:
        return False
    try:
        tenant = keystone.tenants.create(tenant_name=tenant_name,
                                         description=tenant_description,
                                         enabled=True)
    except Exception:
        return False
    try:
        newuser = keystone.users.create(name=user_name,
                                        password=user_password,
                                        email=user_email)
    except Exception:
        return False
    try:
        role_list = keystone.roles.list()
    except Exception:
        return False
    try:
        keystone.tenants.add_user(tenant=tenant,
                                  user=newuser,
                                  role=role_list[0])
    except Exception:
        return False
    return True


def getEncodeStr(word, val='utf-8'):
    if os.name == 'nt':
        wtemp = u'wtemp'
        if type(word) == type(wtemp):
            disvalue = word
        else:
            disvalue = unicode(word, 'mbcs')
        if val.lower() != 'utf-8':
            try:
                tdv = disvalue.encode(val)
            except Exception:
                tdv = disvalue.encode('utf-8')
        else:
            tdv = disvalue.encode(val)
        return tdv
    else:
        return word


def StringMD5(string):
    return hashlib.md5(string).hexdigest().upper()


def StringSHA1(string):
    return hashlib.sha1(string).hexdigest().upper()


def GetFileMd5(filename):
    myhash = hashlib.md5()
    for chunk in filename.chunks(2097152):
        myhash.update(chunk)
    return myhash.hexdigest().upper()


def GetFileSHA1(filename):
    myhash = hashlib.sha1()
    for chunk in filename.chunks(2097152):
        myhash.update(chunk)
    return myhash.hexdigest().upper()


File_Type_Array_32 = {
    '.7z': 1, '.ace': 2, '.ai': 3, '.aif': 4,
    '.aiff': 5, '.amr': 6, '.asf': 7, '.asx': 8,
    '.bat': 9, '.bin': 10, '.bmp': 11, '.bup': 12,
    '.cab': 13, '.cbr': 14, '.cda': 15, '.cdl': 16,
    '.cdr': 17, '.chm': 18, '.dat': 19, '.divx': 20,
    '.dll': 21, '.dmg': 22, '.doc': 23, '.dss': 24,
    '.dvf': 25, '.dwg': 26, '.eml': 27, '.eps': 28,
    '.exe': 29, '.fla': 30, '.flv': 31, '.gif': 32,
    '.gz': 33, '.hqx': 34, '.htm': 35, '.html': 36,
    '.ifo': 37, '.indd': 38, '.iso': 39, '.jar': 40,
    '.jpeg': 41, '.jpg': 42, '.lnk': 43, '.log': 44,
    '.m4a': 45, '.m4b': 46, '.m4p': 47, '.m4v': 48,
    '.mcd': 49, '.mdb': 50, '.mid': 51, '.mov': 52,
    '.mp2': 53, '.mp4': 54, '.mpeg': 55, '.mpg': 56,
    '.msi': 57, '.mswmm': 58, '.ogg': 59, '.pdf': 60,
    '.png': 61, '.pps': 62, '.ps': 63, '.psd': 64,
    '.pst': 65, '.ptb': 66, '.pub': 67, '.qbb': 68,
    '.qbw': 69, '.qxd': 70, '.ram': 71, '.rar': 72,
    '.rm': 73, '.rmvb': 74, '.rtf': 75, '.sea': 76,
    '.ses': 77, '.sit': 78, '.sitx': 79, '.ss': 80,
    '.swf': 81, '.tgz': 82, '.thm': 83, '.tif': 84,
    '.tmp': 85, '.torrent': 86, '.ttf': 87, '.txt': 88,
    '.vcd': 89, '.vob': 90, '.wav': 91, '.wma': 92,
    '.wmv': 93, '.wps': 94, '.xls': 95, '.xpi': 96,
    '.zip': 97, '.mp3': 98, '.php': 99, '': 100,
    '.code': 101, '.cpp': 102, '.cs': 103, '.h': 104,
    '.vs': 105, '.as': 106, '.acrobat': 107, '.c': 108,
    '.ppt': 109, '.word': 110, '.3gp': 111}


def FindFileType(typename):
    typename = '%s%s' % ('.', typename)
    return File_Type_Array_32.get(typename.lower(), 100)
