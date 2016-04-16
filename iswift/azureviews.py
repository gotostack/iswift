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

from django.contrib import auth
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context


from iswift.azureapi import azureapi


swift_user = ''
swift_key = ''
swift_tenant = 'swiftproject'

user_dashboard_templates = 'logined/userpanel/userdashboard.html'


def handle_uploaded_file(f):
    destination = open('/home/swift/webroot/userdownload/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255)
    file = forms.FileField()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('/')


def container_objects(request, container):
        container_name = '%s' % container
        username = request.GET.get('username')
        swift_user = username
        file_loaction = []
        file_loaction.append(container_name)
        objects_list = azureapi.list_container_objects(container_name)
        c = {'logo_link': '#',
             'username': swift_user,
             'container_root': 'javascript:history.go(-1)',
             'file_loaction': file_loaction,
             'file_pic': 'page_icon_page_white_word_32',
             'objects': objects_list,
             'object_create_path': container_name,
             'is_object_list': True,
             'is_container_list': False}
        return render_to_response(user_dashboard_templates, c)


def objects_stat(request, container, containername, objects):
    container_name = '%s' % container
    objects_name = '%s' % objects
    username = request.GET.get('username')
    swift_user = username
    file_loaction = []
    file_loaction.append(container_name)
    file_loaction.append(objects_name)
    objects_stat = azureapi.list_object_detail(container_name, objects_name)
    c = {'logo_link': '#',
         'username': swift_user,
         'container_root': 'javascript:history.go(-1)',
         'file_loaction': file_loaction,
         'file_pic': 'page_icon_page_white_code_32',
         'objects_detail': objects_stat}
    return render_to_response(user_dashboard_templates, c)


def download_object(request, containernames, objects):
    container_name = '%s' % containernames
    objects_name = '%s' % objects
    username = 'iswift'
    swift_user = username
    swift_key = '12345'
    swift_tenant = 'swiftproject'
    return azureapi.get_object(swift_user,
                               swift_key,
                               swift_tenant,
                               container_name,
                               objects_name)


def upload_a_object(request, container):
    errors = []
    if request.method == 'POST':
        container_name = '%s' % container
        object_name = request.POST.get('id_name')
        if not container_name:
            errors.append('Error: Please Enter a container name.')
        if not object_name:
            errors.append('Error: Please Enter a object_name name.')
        if not errors:
            swift_user = 'iswift'
            swift_key = '12345'
            swift_tenant = 'swiftproject'
            contents = request.FILES['id_object_file']
            if contents:
                    azureapi.upload_object(swift_user,
                                           swift_key,
                                           swift_tenant,
                                           container_name,
                                           object_name,
                                           contents)
            else:
                return render_to_response('/', {'errors': errors})
            objects_list = azureapi.list_container_objects(swift_user,
                                                           swift_key,
                                                           swift_tenant,
                                                           container_name)
            file_loaction = []
            file_loaction.append(container_name)
            return render_to_response(
                user_dashboard_templates,
                {'logo_link': '#',
                 'container_root': 'javascript:history.go(-1)',
                 'file_loaction': file_loaction,
                 'file_pic': 'page_icon_page_white_word_32',
                 'containers': objects_list[1]})
    return render_to_response(
        user_dashboard_templates,
        {'container_root': '#',
         'logo_link': '#',
         'file_pic': 'page_icon_page_white_word_32'})


def create_container(request):
    errors = []
    if request.method == 'POST':
        container_name = request.POST.get('id_name')
        if not container_name:
            errors.append('错误：请输入一个container名称')
        if not errors:
            swift_user = 'iswift'
            azureapi.container_create(container_name)
            container_list = azureapi.get_container_list()
            c = Context({'container_root': '#',
                         'username': swift_user,
                         'logo_link': '#',
                         'file_pic': 'page_icon_folder_32',
                         'containers': container_list[1],
                         'is_container_list': True})
            return render_to_response(user_dashboard_templates, c)
    if request.method == 'GET':
        container_name = request.GET.get('id_name')
        if not container_name:
            errors.append('错误：请输入一个container名称')
        if not errors:
            swift_user = 'iswift'
            azureapi.container_create(container_name)
            container_list = azureapi.get_container_list()
            contex = Context({'container_root': '#',
                              'username': swift_user,
                              'logo_link': '#',
                              'file_pic': 'page_icon_folder_32',
                              'is_container_list': True,
                              'containers': container_list[1]})
            return render_to_response(user_dashboard_templates, contex)
    contex = Context({'container_root': '#',
                      'username': swift_user,
                      'logo_link': '#',
                      'file_pic': 'page_icon_folder_32',
                      'is_container_list': True})
    return render_to_response(user_dashboard_templates, contex)


def usermain(request, username,
             tenant_name, password=None,
             errors=None, container_root=None,
             file_pic=None, containers=None,
             logo_link=None, is_container_list=None):
    username = username
    password = password
    errors = errors
    container_root = container_root
    file_pic = file_pic
    containers = containers
    logo_link = logo_link
    is_container_list = is_container_list
    c = {'errors': errors,
         'username': username,
         'password': password,
         'container_root': container_root,
         'containers': containers,
         'logo_link': logo_link,
         'file_pic': file_pic,
         'is_container_list': is_container_list}
    return render_to_response(user_dashboard_templates, c)


def index(request):
    return HttpResponseRedirect('/login')


def home(request):
    username = ''
    password = ''
    errors = []
    if request.method == 'POST':
        tenantname = request.POST.get('tenantname', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        swift_user = username
        swift_key = password
        swift_tenant = tenantname
        if not swift_tenant:
            errors.append('错误: 请输入存储项目。')
        if not swift_user:
            errors.append('错误: 请输入用户名。')
        if not swift_key:
            errors.append('错误: 请输入密码。')
        if not errors:
            container_list = azureapi.get_container_list()
            return usermain(request=request,
                            username=swift_user,
                            tenant_name=swift_tenant,
                            container_root='#',
                            logo_link='#',
                            file_pic='page_icon_folder_32',
                            containers=container_list,
                            is_container_list=True)
    return render_to_response('home.html',
                              {'errors': errors, 'logo_link': '/'})


def authlogin(request):
    username = ''
    password = ''
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if not username:
            errors.append('错误: 请输入用户名。')
        if not password:
            errors.append('错误: 请输入密码。')
        if not errors:
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                container_list = azureapi.get_container_list()
                # Redirect to a success page.
                return render_to_response(
                    user_dashboard_templates,
                    {'username': username,
                     'is_container_list': True,
                     'container_root': '#',
                     'logo_link': '#',
                     'file_pic': 'page_icon_folder_32',
                     'containers': container_list[1]})
            else:
                errors.append('错误: 不可用的用户名或者密码。')
                render_to_response(
                    'auth/login.html',
                    {'errors': errors,
                     'logo_link': '/',
                     'username': username,
                     'password': password})
    if request.method == 'GET':
        username = request.GET.get('username')
        user = auth.authenticate(username=username)
        if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                container_list = azureapi.get_container_list()
                # Redirect to a success page.
                return render_to_response(
                    user_dashboard_templates,
                    {'username': username,
                     'is_container_list': True,
                     'container_root': '/',
                     'logo_link': '#',
                     'file_pic': 'page_icon_folder_32',
                     'containers': container_list[1]})
        else:
            render_to_response(
                'auth/login.html',
                {'errors': errors,
                 'logo_link': '/'})
    return render_to_response(
        'auth/login.html',
        {'errors': errors,
         'logo_link': '/'})


def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')
