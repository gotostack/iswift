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

from django.shortcuts import render_to_response
from keystoneclient.v2_0 import client
from swiftclient import client as swiftclient


LOACL_AUTH_URL = 'http://127.0.0.1:5000/v2.0'


def get_connection(authurl, user, key, retries=5, preauthurl=None,
                   preauthtoken=None, snet=False, starting_backoff=1,
                   tenant_name=None, os_options={}, auth_version="2.0"):
    return swiftclient.Connection(authurl, user, key,
                                  retries, preauthurl, preauthtoken,
                                  snet, starting_backoff,
                                  tenant_name, os_options, auth_version)


def create_tenant(tenant_name, tenant_description,
                  user_name, user_password, user_email):
    keystone = client.Client(username='adminUser',
                             password='secretword',
                             tenant_name='openstackDemo',
                             auth_url=LOACL_AUTH_URL)
    tenant = keystone.tenants.create(tenant_name=tenant_name,
                                     description=tenant_description,
                                     enabled=True)
    newuser = keystone.users.create(name=user_name,
                                    password=user_password,
                                    email=user_email)
    role_list = keystone.roles.list()
    keystone.tenants.add_user(tenant=tenant, user=newuser, role=role_list[0])


class FakeFile(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.size = len(self.data)


def get_user_auth(user, key, tenant_name):
    connection = get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={}, auth_version="2.0")
    try:
        return connection.get_auth()
    except Exception:
        return 'FALSE'


def upload_object(user,
                  key,
                  tenant_name,
                  container_name,
                  object_name,
                  file_path):
    contents = open(file_path)
    get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0").put_object(container_name,
                                       object_name,
                                       contents)
    contents.close()
    return True


def get_object(user,
               key,
               tenant_name,
               container_name,
               object_name):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0").get_object(container_name, object_name)


def container_create(user, key, tenant_name, container_name):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0").put_container(container_name)


def update_container(user, key, tenant_name, container_name, headers):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0").post_container(container_name, headers)


def get_container_list(user, key, tenant_name):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0"). get_account()


def list_container_objects(user, key, tenant_name, container_name):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0"). get_container(container_name)


def list_container_detail(user, key, tenant_name, container_name):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0").head_container(container_name)


def list_object_detail(user, key, tenant_name, container_name, object_name):
    return get_connection(
        authurl=LOACL_AUTH_URL,
        user=user,
        key=key, retries=5, preauthurl=None,
        preauthtoken=None, snet=False, starting_backoff=1,
        tenant_name=tenant_name, os_options={},
        auth_version="2.0").head_object(container_name, object_name)


def home(request):
    username = ''
    password = ''
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        swift_user = username
        swift_key = password
        swift_tenant = 'swiftproject'
        if not swift_user:
            errors.append('Error: Please Enter a user name.')
        if not swift_key:
            errors.append('Error: Please Enter a password.')
        if not errors:
            try:
                get_user_auth(username, password, swift_tenant)
            except swiftclient.ClientException:
                errors.append('Error: Invalid user name or password.')
                c = {'errors': errors,
                     'logo_link': '/',
                     'username': swift_user,
                     'password': swift_key}
                return render_to_response('home.html', c)
    if request.method == 'GET':
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        swift_user = username
        swift_key = password
        swift_tenant = 'swiftproject'
        if not swift_user:
            errors.append('Error: Please Enter a user name.')
        if not swift_key:
            errors.append('Error: Please Enter a password.')
        if not errors:
            try:
                get_user_auth(username, password, swift_tenant)
            except swiftclient.ClientException:
                errors.append('Error: Invalid user name or password.')
                c = {'errors': errors,
                     'logo_link': '/',
                     'username': swift_user,
                     'password': swift_key}
                return render_to_response('home.html', c)
    return render_to_response('home.html', {
        'errors': errors,
        'logo_link': '/',
    })
