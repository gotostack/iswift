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

import random

import cStringIO
import Image
import ImageDraw
import ImageFont

import settings

from django.contrib import auth
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext

from iswift.folderlist.models import company_tree
from iswift.folderlist.models import folder_tree
from iswift.folderlist.models import user_storage
from iswift.swiftapi import messages
from iswift.swiftapi import views as iswift_views


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
        container_name = u'%s' % container
        username = request.GET.get('username')
        swift_user = username
        swift_key = '12345'
        file_loaction = []
        file_loaction.append(container_name)
        objects_list = iswift_views.list_container_objects(
            swift_user, swift_key,
            swift_tenant, container_name)
        c = {'logo_link': '#',
             'username': swift_user,
             'container_root': 'javascript:history.go(-1)',
             'file_loaction': file_loaction,
             'file_pic': 'page_icon_page_white_word_32',
             'objects': objects_list[1],
             'object_create_path': container_name,
             'is_object_list': True,
             'is_container_list': False}
        return render_to_response(user_dashboard_templates,
                                  c,
                                  context_instance=RequestContext(request))


def objects_stat(request, container, containername, objects):
    container_name = u'%s' % container
    objects_name = u'%s' % objects
    username = request.GET.get('username')
    swift_user = username
    swift_key = '12345'
    file_loaction = []
    file_loaction.append(container_name)
    file_loaction.append(objects_name)
    objects_stat = iswift_views.list_object_detail(
        swift_user,
        swift_key,
        swift_tenant,
        container_name,
        objects_name)
    c = {'logo_link': '#',
         'username': swift_user,
         'container_root': 'javascript:history.go(-1)',
         'file_loaction': file_loaction,
         'file_pic': 'page_icon_page_white_code_32',
         'objects_detail': objects_stat}
    return render_to_response(user_dashboard_templates,
                              c,
                              context_instance=RequestContext(request))


def download_object(request, containernames, objects):
    container_name = u'%s' % containernames
    objects_name = u'%s' % objects
    username = 'iswift'
    swift_user = username
    swift_key = '12345'
    swift_tenant = 'swiftproject'
    return iswift_views.get_object(
        swift_user,
        swift_key,
        swift_tenant,
        container_name,
        objects_name)


def upload_a_object(request, container):
    errors = []
    if request.method == 'POST':
        container_name = u'%s' % container
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
                iswift_views.upload_object(
                    swift_user,
                    swift_key,
                    swift_tenant,
                    container_name,
                    object_name,
                    object_name,
                    contents)
            else:
                return render_to_response('/', {'errors': errors})
            objects_list = iswift_views.list_container_objects(
                swift_user,
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
            errors.append('错误: 请输入一个container名称')
        if not errors:
            swift_user = 'iswift'
            swift_key = '12345'
            swift_tenant = 'swiftproject'
            iswift_views.container_create(
                swift_user,
                swift_key,
                swift_tenant,
                container_name)
            container_list = iswift_views.get_container_list(
                swift_user,
                swift_key,
                swift_tenant)
            c = Context({'container_root': '#',
                         'username': swift_user,
                         'logo_link': '#',
                         'file_pic': 'page_icon_folder_32',
                         'containers': container_list[1],
                         'is_container_list': True})
            return render_to_response(
                user_dashboard_templates,
                c,
                context_instance=RequestContext(request))
    if request.method == 'GET':
        container_name = request.GET.get('id_name')
        if not container_name:
            errors.append(u'错误: 请输入一个container名称')
        if not errors:
            swift_user = 'iswift'
            swift_key = '12345'
            swift_tenant = 'swiftproject'
            iswift_views.container_create(
                swift_user,
                swift_key,
                swift_tenant,
                container_name)
            container_list = iswift_views.get_container_list(
                swift_user,
                swift_key,
                swift_tenant)
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


def index(request):
    return HttpResponseRedirect('/login')


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
                auth.login(request, user)
                container_list = iswift_views.get_container_list(
                    'adminUser',
                    'secretword',
                    'openstackDemo')
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
                auth.login(request, user)
                container_list = iswift_views.get_container_list(
                    'adminUser',
                    'secretword',
                    'openstackDemo')
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
    return render_to_response('auth/login.html', {
        'errors': errors,
        'logo_link': '/',
    })


def file_tree_create_folder(request):
    if request.user.is_authenticated():
        errors = []
        if request.method == 'POST':
            container_name = request.POST.get('id_name')
            if not container_name:
                errors.append('Please input a folder name!')
                messages.error(request, 'Please input a folder name!')
            if not errors:
                iswift_views.container_create(container_name)
                messages.success(request, u'创建成功！')
                return HttpResponseRedirect('/userdashboard')
        if request.method == 'GET':
            container_name = request.GET.get('id_name')
            if not container_name:
                errors.append('Please input a folder name!')
                messages.error(request, 'Please input a folder name!')
            if not errors:
                iswift_views.container_create(container_name)
                messages.success(request, '创建成功！')
                return HttpResponseRedirect('/userdashboard')
        contex = Context({'container_root': '#',
                          'username': swift_user,
                          'logo_link': '#',
                          'file_pic': 'page_icon_folder_32',
                          'is_container_list': True})
        return render_to_response(user_dashboard_templates,
                                  contex,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, '请登录！')
        return HttpResponseRedirect('/')


class HomeForm(forms.Form):
    username = forms.EmailField()
    password = forms.PasswordInput()


def home(request):
    username = ''
    password = ''
    isFromOK = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not username:
            messages.error(request, u'please enter username')
            isFromOK = False
        if not password:
            messages.error(request, u'please enter userpassword')
            isFromOK = False
        if isFromOK:
            request.session.clear()
            if request.user.is_authenticated():
                auth.logout(request)
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                messages.success(request, u'登录成功！')
                return HttpResponseRedirect('/userdashboard')
            else:
                messages.error(request, u'Invaild username or password.')
                return HttpResponseRedirect('/')
    return render_to_response(
        'auth/login.html',
        {'logo_link': '/',
         's_username': username,
         's_password': password},
        context_instance=RequestContext(request))


def VerifyCode(request):
    """VerifyCode.

    background  #随机背景颜色
    line_color #随机干扰线颜色
    img_width = #画布宽度
    img_height = #画布高度
    font_color = #验证码字体颜色
    font_size = #验证码字体尺寸
    font = I#验证码字体
    """

    string = {'number': '12345679',
              'litter': 'ACEFGHKMNPRTUVWXY'}
    background = (random.randrange(230, 255),
                  random.randrange(230, 255),
                  random.randrange(230, 255))
    img_width = 58
    img_height = 30
    font_color = ['black', 'darkblue', 'darkred',
                  'green', 'purple', 'brown',
                  'darkmagenta', 'maroon', 'teal']
    font_size = 14
    font = ImageFont.truetype('%s/font/timesbi.ttf' % settings.STATIC_ROOT,
                              font_size)
    request.session['verify'] = ''

    im = Image.new('RGB', (img_width, img_height), background)
    char_choice = ['litter', 'number']
    code = random.sample(
        string[random.choice(char_choice)],
        1) + random.sample(
        string[random.choice(char_choice)],
        1) + random.sample(
        string[random.choice(char_choice)],
        1) + random.sample(string[random.choice(char_choice)], 1)

    draw = ImageDraw.Draw(im)

    for i in range(random.randrange(3, 13)):
        xy = (random.randrange(0, img_width),
              random.randrange(0, img_height),
              random.randrange(0, img_width),
              random.randrange(0, img_height))
        line_color = (random.randrange(0, 255),
                      random.randrange(0, 255),
                      random.randrange(0, 255))
        draw.line(xy, fill=line_color, width=1)

    x = 2
    for i in code:
        y = random.randrange(0, 10)
        draw.text((x, y), i, font=font, fill=random.choice(font_color))
        x += 14
        request.session['verify'] += i
    del x
    del draw
    buf = cStringIO.StringIO()
    im.save(buf, 'gif')
    buf.seek(0)
    return HttpResponse(buf.getvalue(), 'image/gif')


def usermain(request):
    if request.user.is_authenticated():
        username = request.user.username
        user_company_id = user_storage.objects.filter(name=username,
                                                      user_id=request.user.id)
        root_base_id = folder_tree.objects.filter(
            name='BASEROOT',
            level=1,
            companyid=user_company_id[0].companyid)
        books = folder_tree.objects.order_by('companyid').filter(
            parentID=root_base_id[0].id,
            companyid=user_company_id[0].companyid)
        retlist = []
        for first in books:
            if (user_company_id[0].competence >= first.competence
                    and first.isDeleted == 0):
                retlist.append(first)
        c = {'username': username,
             'is_container_list': True,
             'container_root': '#',
             'logo_link': '#',
             'file_pic': 'page_icon_folder_32',
             'containers': retlist,
             'company_files_class': 'current'}
        return render_to_response(user_dashboard_templates,
                                  c,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, u'请先登录！')
        return HttpResponseRedirect('/')


def logout_view(request):
    messages.success(request, u'下线成功！ 再见!')
    auth.logout(request)
    return HttpResponseRedirect('/')


def sub_folder(request, parent_folder):
    if request.user.is_authenticated():
        username = request.user.username
        path_folder = u'%s' % parent_folder
        folder_list = path_folder.split('/')
        folder_list_length = len(folder_list)

        fast_file_link = []
        temp_vec = folder_list[0:folder_list_length - 1]
        for i in range(0, len(temp_vec)):
            link = '/userdashboard/'
            temp = temp_vec[0:i + 1]
            path = '/'.join(temp)
            link += path
            abe = {'name': temp_vec[i], 'link': link}
            fast_file_link.append(abe)

        user_company_id = user_storage.objects.filter(
            name=username,
            user_id=request.user.id)
        item = folder_tree.objects.filter(
            name=folder_list[folder_list_length - 2],
            level=folder_list_length,
            companyid=user_company_id[0].companyid).filter(isDeleted=0)
        if len(item) > 0:
            folders = folder_tree.objects.filter(
                parentID=item[0].id).filter(isDeleted=0)
            files = []
            for folder in folders:
                if folder.FileLink >= 0:
                    files.append(folder)
            container_root = folder_list[0:folder_list_length - 2]
            container_str = ''
            container_str = '/'.join(container_root)
            container_str = '/userdashboard/%s' % container_str
            c = {'username': username,
                 'container_root': container_str,
                 'logo_link': '#',
                 'file_pic': 'page_icon_folder_32',
                 'containers': files,
                 'file_loaction': fast_file_link,
                 'company_files_class': 'current'}
            return render_to_response(
                user_dashboard_templates,
                c,
                context_instance=RequestContext(request))
        else:
            messages.error(request, u'文件夹\'%s\'不存在！' % path_folder)
            return HttpResponseRedirect('/userdashboard')
    else:
        messages.error(request, u'请先登录！')
        return HttpResponseRedirect('/')


def sql_create_folder(request, parent_folder):
    if request.user.is_authenticated():
        if request.method == 'POST':
            folder_name = request.POST.get('id_name')
            folder_list = '%s' % parent_folder
            folder_list = folder_list.split('/')
            userstorage = user_storage.objects.filter(
                name=request.user.username)
            root_base_id = folder_tree.objects.filter(
                name='BASEROOT',
                level=1,
                companyid=userstorage[0].companyid)
            if len(folder_list) <= 1:
                is_folder_already_have = folder_tree.objects.filter(
                    name=folder_name,
                    parentID=root_base_id[0].id,
                    isFile=0,
                    level=2,
                    companyid=userstorage[0].companyid,
                    isContainer=1)
                if len(is_folder_already_have) >= 1:
                    urls = '%s%s' % ('/userdashboard/', folder_name)
                    messages.info(
                        request,
                        u'文件夹\'%s\'已经存在, 并已经进入该文件夹！' % folder_name)
                    return HttpResponseRedirect(urls)
                company_token = company_tree.objects.filter(
                    id=userstorage[0].companyid)
                swift_user = company_token[0].keystone_user_id
                swift_key = company_token[0].keystone_passwd
                swift_tenant = company_token[0].keystone_tenant
                container_name = '%s-%d-%d' % (
                    folder_name, userstorage[0].companyid, 2)
                create_success = iswift_views.container_create(
                    swift_user,
                    swift_key,
                    swift_tenant,
                    container_name)
                if not create_success:
                    messages.error(
                        request,
                        ('Folder\'%s\' create failed, reason: '
                         'swift container\'%s\' create failed.') % (
                             folder_name,
                             container_name))
                    return HttpResponseRedirect('/userdashboard/')
                folder = folder_tree(
                    name=folder_name,
                    type=0,
                    parentID=root_base_id[0].id,
                    isFile=0,
                    level=2,
                    companyid=userstorage[0].companyid,
                    isContainer=1,
                    sizebyte=0,
                    competence=10,
                    MD5string='',
                    SHA1string='',
                    CRC32string='',
                    FileLink=0,
                    isDeleted=0)
                folder.save()

                messages.success(request,
                                 u'%s%s%s' % (u'文件夹\'',
                                              folder_name,
                                              u'\'创建成功！'))
                return HttpResponseRedirect('/userdashboard/')
            else:
                urls = u'%s%s' % ('/userdashboard/', parent_folder)
                folder_list_length = len(folder_list)
                item = folder_tree.objects.filter(
                    name=folder_list[folder_list_length - 2]).filter(
                        level=folder_list_length)
                is_folder_already_have = folder_tree.objects.filter(
                    name=folder_name,
                    parentID=item[0].id,
                    isFile=0,
                    level=folder_list_length + 1,
                    companyid=userstorage[0].companyid,
                    isContainer=1)
                if len(is_folder_already_have) >= 1:
                    messages.info(request,
                                  u'文件夹\'%s\'已经存在, 并已进入该文件夹！' % (
                                      folder_name))
                    return HttpResponseRedirect(urls)
                company_token = company_tree.objects.filter(
                    id=userstorage[0].companyid)
                swift_user = company_token[0].keystone_user_id
                swift_key = company_token[0].keystone_passwd
                swift_tenant = company_token[0].keystone_tenant
                container_name = '%s-%d-%d' % (
                    folder_name,
                    userstorage[0].companyid,
                    folder_list_length + 1)
                if not iswift_views.container_create(
                        swift_user,
                        swift_key,
                        swift_tenant,
                        container_name):
                    messages.error(
                        request,
                        u'Folder \'%s\' create failed, reason: '
                        'container \'%s\' create failed.' % (
                            folder_name,
                            container_name))
                    return HttpResponseRedirect(urls)
                folder = folder_tree(
                    name=folder_name,
                    type=0,
                    parentID=item[0].id,
                    isFile=0,
                    level=folder_list_length + 1,
                    companyid=userstorage[0].companyid,
                    isContainer=1,
                    sizebyte=0,
                    competence=10,
                    MD5string='',
                    SHA1string='',
                    CRC32string='',
                    FileLink=0,
                    isDeleted=0)
                folder.save()
                messages.success(request, u'文件夹\'%s\'创建成功！' % folder_name)
                return HttpResponseRedirect(urls)
        if request.method == 'GET':
            messages.error(request, 'Only Post Method support!')
            return HttpResponseRedirect('/userdashboard')
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def sql_create_file(request, parent_folder):
    if request.user.is_authenticated():
        if request.method == 'POST':
            folder_list = '%s' % parent_folder
            folder_list = folder_list.split('/')
            userstorage = user_storage.objects.filter(
                name=request.user.username)
            contents = request.FILES['id_object_file']
            file_name = '%s' % (contents.name)

            smd5 = request.POST.get('id_file_md5')
            ssha1 = iswift_views.GetFileSHA1(contents)
            contents.seek(0)

            FileLink = 0
            is_file_already_store = folder_tree.objects.filter(
                MD5string=smd5,
                SHA1string=ssha1,
                companyid=userstorage[0].companyid)

            file_type = file_name.split('.')
            filetype = iswift_views.FindFileType(file_type[len(file_type) - 1])

            cmp_storage_add = company_tree.objects.get(
                id=userstorage[0].companyid)
            cmp_storage_add.used_size = \
                contents.size + cmp_storage_add.used_size
            cmp_storage_add.save()

            if len(is_file_already_store) <= 0:
                if len(folder_list) <= 1:
                    root_base_id = folder_tree.objects.filter(
                        name='BASEROOT',
                        level=1,
                        companyid=userstorage[0].companyid)
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=file_name,
                        parentID=root_base_id[0].id,
                        isFile=1,
                        level=2,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            u'这一级目录下已经存在一个名为\'%s\'的文件!' % (file_name))
                        return HttpResponseRedirect('/userdashboard/')
                    company_token = company_tree.objects.filter(
                        id=userstorage[0].companyid)
                    swift_user = company_token[0].keystone_user_id
                    swift_key = company_token[0].keystone_passwd
                    swift_tenant = company_token[0].keystone_tenant
                    container_name = '%s-%d' % (
                        'BASEROOT', userstorage[0].companyid)
                    object_name = '%s-%d-%d' % (
                        file_name,
                        userstorage[0].companyid,
                        2)
                    if contents:
                        if not iswift_views.upload_object(
                                swift_user,
                                swift_key,
                                swift_tenant,
                                container_name,
                                object_name,
                                file_name,
                                contents):
                            messages.error(
                                request,
                                u'upload file \'%s\'failed, reason: create'
                                'Container-\'%s\' Oject-'
                                '\'%s\'failed.' % (file_name,
                                                   container_name,
                                                   object_name))
                            return HttpResponseRedirect('/userdashboard/')
                    folder = folder_tree(
                        name=file_name,
                        type=filetype,
                        parentID=root_base_id[0].id,
                        isFile=1,
                        level=2,
                        companyid=userstorage[0].companyid,
                        isContainer=0,
                        sizebyte=contents.size,
                        competence=10,
                        MD5string=smd5,
                        SHA1string=ssha1,
                        CRC32string='',
                        FileLink=FileLink,
                        isDeleted=0)
                    folder.save()

                    baseroot = folder_tree.objects.get(id=root_base_id[0].id)
                    baseroot.sizebyte = contents.size + baseroot.sizebyte
                    baseroot.save()

                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect('/userdashboard/')
                else:
                    usls = '%s%s' % ('/userdashboard/', parent_folder)
                    folder_list_length = len(folder_list)
                    item = folder_tree.objects.filter(
                        name=folder_list[folder_list_length - 2]).filter(
                            level=folder_list_length).filter(
                                companyid=userstorage[0].companyid)
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=file_name,
                        parentID=item[0].id,
                        isFile=1,
                        level=folder_list_length + 1,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            u'这一级目录下已经存在一个名为\'%s\'的文件!' % (file_name))
                        return HttpResponseRedirect(usls)
                    company_token = company_tree.objects.filter(
                        id=userstorage[0].companyid)
                    swift_user = company_token[0].keystone_user_id
                    swift_key = company_token[0].keystone_passwd
                    swift_tenant = company_token[0].keystone_tenant
                    container_name = '%s-%d-%d' % (
                        item[0].name,
                        userstorage[0].companyid,
                        folder_list_length)
                    object_name = '%s-%d-%d' % (
                        file_name,
                        userstorage[0].companyid,
                        folder_list_length + 1)
                    if contents:
                        upload_success = iswift_views.upload_object(
                            swift_user,
                            swift_key,
                            swift_tenant,
                            container_name,
                            object_name,
                            file_name,
                            contents)
                        if not upload_success:
                            messages.error(
                                request,
                                u'Upload file \'%s\' failed, reason: create'
                                'Container-\'%s\' Oject-\'%s\' failed.' % (
                                    file_name,
                                    container_name,
                                    object_name))
                            return HttpResponseRedirect(usls)
                    folder = folder_tree(
                        name=file_name,
                        type=filetype,
                        parentID=item[0].id,
                        isFile=1,
                        level=folder_list_length + 1,
                        companyid=userstorage[0].companyid,
                        isContainer=0,
                        sizebyte=contents.size,
                        competence=10,
                        MD5string=smd5,
                        SHA1string=ssha1,
                        CRC32string='',
                        FileLink=FileLink,
                        isDeleted=0)
                    folder.save()
                    findid = item[0].id
                    while 1:
                        baseroot = folder_tree.objects.get(id=findid)
                        baseroot.sizebyte = contents.size + baseroot.sizebyte
                        baseroot.save()
                        if baseroot.level == 1:
                            break
                        findid = baseroot.parentID
                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect(usls)
            else:
                FileLink = is_file_already_store[0].id
                if len(folder_list) <= 1:
                    root_base_id = folder_tree.objects.filter(
                        name='BASEROOT',
                        level=1,
                        companyid=userstorage[0].companyid)
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=file_name,
                        parentID=root_base_id[0].id,
                        isFile=1,
                        level=2,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            u'这一级目录下已经存在一个名为\'%s\'的文件!' % (file_name))
                        return HttpResponseRedirect('/userdashboard/')
                    folder = folder_tree(
                        name=file_name,
                        type=filetype,
                        parentID=root_base_id[0].id,
                        isFile=1,
                        level=2,
                        companyid=userstorage[0].companyid,
                        isContainer=0,
                        sizebyte=contents.size,
                        competence=10,
                        MD5string=smd5,
                        SHA1string=ssha1,
                        CRC32string='',
                        FileLink=FileLink,
                        isDeleted=0)
                    folder.save()

                    baseroot = folder_tree.objects.get(id=root_base_id[0].id)
                    baseroot.sizebyte = contents.size + baseroot.sizebyte
                    baseroot.save()

                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect('/userdashboard/')
                else:
                    usls = '%s%s' % ('/userdashboard/', parent_folder)
                    folder_list_length = len(folder_list)
                    item = folder_tree.objects.filter(
                        name=folder_list[folder_list_length - 2]).filter(
                            level=folder_list_length).filter(
                                companyid=userstorage[0].companyid)
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=file_name,
                        parentID=item[0].id,
                        isFile=1,
                        level=folder_list_length + 1,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            u'这一级目录下已经存在一个名为\'%s\'的文件!' % (file_name))
                        return HttpResponseRedirect(usls)
                    folder = folder_tree(
                        name=file_name,
                        type=filetype,
                        parentID=item[0].id,
                        isFile=1,
                        level=folder_list_length + 1,
                        companyid=userstorage[0].companyid,
                        isContainer=0,
                        sizebyte=contents.size,
                        competence=10,
                        MD5string=smd5,
                        SHA1string=ssha1,
                        CRC32string='',
                        FileLink=FileLink,
                        isDeleted=0)
                    folder.save()
                    findid = item[0].id
                    while True:
                        baseroot = folder_tree.objects.get(id=findid)
                        baseroot.sizebyte = contents.size + baseroot.sizebyte
                        baseroot.save()
                        if baseroot.level == 1:
                            break
                        findid = baseroot.parentID

                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect(usls)
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def download_file(request, containernames, objects):
    if request.user.is_authenticated():
        container_name = '%s' % containernames
        objects_name = '%s' % objects
        container_name = container_name.split('/')
        userstorage = user_storage.objects.filter(name=request.user.username)
        company_token = company_tree.objects.filter(
            id=userstorage[0].companyid)
        swift_user = company_token[0].keystone_user_id
        swift_key = company_token[0].keystone_passwd
        swift_tenant = company_token[0].keystone_tenant

        company_root = folder_tree.objects.filter(
            level=1,
            name='BASEROOT',
            companyid=userstorage[0].companyid)

        if len(container_name) <= 1:
            current_file = folder_tree.objects.filter(
                level=2,
                name=objects_name,
                parentID=company_root[0].id)
            file_size = current_file[0].sizebyte
            if current_file[0].FileLink == 0:
                container_name = '%s-%d' % ('BASEROOT',
                                            userstorage[0].companyid)
                object_name = '%s-%d-%d' % (
                    objects_name,
                    userstorage[0].companyid,
                    2)
                return iswift_views.get_object(
                    swift_user,
                    swift_key,
                    swift_tenant,
                    container_name,
                    object_name,
                    objects_name,
                    file_size)
            else:
                link_file = folder_tree.objects.filter(
                    id=current_file[0].FileLink)
                parent_file = folder_tree.objects.filter(
                    id=link_file[0].parentID)
                container_name = ''
                if parent_file[0].name == 'BASEROOT':
                    container_name = '%s-%d' % (
                        'BASEROOT', userstorage[0].companyid)
                else:
                    container_name = '%s-%d-%d' % (
                        parent_file[0].name,
                        userstorage[0].companyid,
                        parent_file[0].level)
                object_name = '%s-%d-%d' % (
                    link_file[0].name,
                    userstorage[0].companyid,
                    link_file[0].level)
                return iswift_views.get_object(
                    swift_user,
                    swift_key,
                    swift_tenant,
                    container_name,
                    object_name,
                    objects_name,
                    file_size)
        else:
            level = len(container_name) + 1
            current_file = folder_tree.objects.filter(
                level=level,
                name=objects_name,
                companyid=userstorage[0].companyid)
            file_size = current_file[0].sizebyte
            if current_file[0].FileLink == 0:
                folder_name = '%s-%d-%d' % (
                    container_name[len(container_name) - 2],
                    userstorage[0].companyid,
                    len(container_name))
                object_name = '%s-%d-%d' % (
                    objects_name,
                    userstorage[0].companyid,
                    len(container_name) + 1)
                return iswift_views.get_object(
                    swift_user,
                    swift_key,
                    swift_tenant,
                    folder_name,
                    object_name,
                    objects_name,
                    file_size)
            else:
                link_file = folder_tree.objects.filter(
                    id=current_file[0].FileLink)
                parent_file = folder_tree.objects.filter(
                    id=link_file[0].parentID)
                container_name = ''
                if parent_file[0].name == 'BASEROOT':
                    container_name = '%s-%d' % ('BASEROOT',
                                                userstorage[0].companyid)
                else:
                    container_name = '%s-%d-%d' % (
                        parent_file[0].name,
                        userstorage[0].companyid,
                        parent_file[0].level)
                object_name = '%s-%d-%d' % (
                    link_file[0].name,
                    userstorage[0].companyid,
                    link_file[0].level)
                return iswift_views.get_object(
                    swift_user,
                    swift_key,
                    swift_tenant,
                    container_name,
                    object_name,
                    objects_name,
                    file_size)
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def filesearch(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            userstorage = user_storage.objects.filter(
                name=request.user.username)
            if 'fileserarch' in request.POST:
                fileserarch = request.POST['fileserarch']
                books = folder_tree.objects.filter(
                    companyid=userstorage[0].companyid)
                retlist = books.filter(name__icontains=fileserarch)
                c = {'username': request.user.username,
                     'is_container_list': True,
                     'container_root': 'javascript:history.go(-1)',
                     'logo_link': '#',
                     'file_pic': 'page_icon_folder_32',
                     'containers': retlist}
                return render_to_response(
                    user_dashboard_templates,
                    c,
                    context_instance=RequestContext(request))
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def sql_delete_folderORfile(request, parent_folder):
    if request.user.is_authenticated():
        if request.method == 'POST':
            folder_list = '%s' % parent_folder
            folder_list = folder_list.split('/')
            userstorage = user_storage.objects.filter(
                name=request.user.username)
            root_base_id = folder_tree.objects.filter(
                name='BASEROOT',
                level=1,
                companyid=userstorage[0].companyid)
            folder_list_length = len(folder_list)
            file_name = folder_list[folder_list_length - 2]

            if folder_list_length <= 2:
                delete_item = folder_tree.objects.get(
                    name=file_name,
                    parentID=root_base_id[0].id,
                    level=folder_list_length,
                    companyid=userstorage[0].companyid)
                if delete_item.isFile == 1:
                    delete_item.isDeleted = 1
                    delete_item.save()
                else:
                    delete_item.isDeleted = 1
                    delete_item.save()
                messages.success(request, u'文件(夹)\'%s\'删除成功！' % file_name)
                return HttpResponseRedirect('/userdashboard')
            else:
                delete_item = folder_tree.objects.get(
                    name=file_name,
                    level=folder_list_length,
                    companyid=userstorage[0].companyid)
                if delete_item.isFile == 1:
                    delete_item.isDeleted = 1
                    delete_item.save()
                else:
                    delete_item.isDeleted = 1
                    delete_item.save()
                parent_folder = folder_list[0:folder_list_length - 2]
                parent_folder = '/'.join(parent_folder)
                urls = '%s%s' % ('/userdashboard/', parent_folder)
                messages.success(request, u'文件(夹)\'%s\'删除成功！' % file_name)
                return HttpResponseRedirect(urls)
        else:
            messages.error(request, 'Only Post Method support!')
            return HttpResponseRedirect('/')
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def sql_update_folderORfile(request, parent_folder):
    if request.user.is_authenticated():
        if request.method == 'POST':
            new_folder_name = request.POST.get('id_name')
            old_name = request.POST.get('old_name')
            folder_list = u'%s' % parent_folder
            folder_list = folder_list.split('/')
            userstorage = user_storage.objects.filter(
                name=request.user.username)
            root_base_id = folder_tree.objects.filter(
                name='BASEROOT',
                level=1,
                companyid=userstorage[0].companyid)
            folder_list_length = len(folder_list)
            company_token = company_tree.objects.filter(
                id=userstorage[0].companyid)

            swift_user = company_token[0].keystone_user_id
            swift_key = company_token[0].keystone_passwd
            swift_tenant = company_token[0].keystone_tenant

            file_type = new_folder_name.split('.')
            filetype = iswift_views.FindFileType(file_type[len(file_type) - 1])

            if folder_list_length <= 2:
                folder = folder_tree.objects.get(
                    name=old_name,
                    parentID=root_base_id[0].id,
                    level=2,
                    companyid=userstorage[0].companyid)
                if folder.isFile == 1:
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=new_folder_name,
                        parentID=root_base_id[0].id,
                        isFile=1,
                        level=2,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            'Failed existed: %s' % new_folder_name)
                        return HttpResponseRedirect('/userdashboard/')
                    if folder.FileLink == 0:
                        container_name = u'%s-%d' % ('BASEROOT',
                                                     userstorage[0].companyid)
                        # copy new obj
                        orig_object_name = u'%s-%d-%d' % (
                            old_name, userstorage[0].companyid, 2)
                        new_object_name = u'%s-%d-%d' % (
                            new_folder_name, userstorage[0].companyid, 2)
                        copy_success = iswift_views.copy_object(
                            swift_user,
                            swift_key,
                            swift_tenant,
                            container_name,
                            orig_object_name,
                            container_name,
                            new_object_name)
                        if copy_success:
                            # delete old obj
                            iswift_views.delete_an_objcte(
                                swift_user, swift_key,
                                swift_tenant, container_name,
                                orig_object_name)
                        else:
                            messages.error(
                                request,
                                u'From container: \'%s\' copy '
                                'object: \'%s\'to container: \'%s\' '
                                'as new Object: \'%s\'failed.' % (
                                    container_name,
                                    orig_object_name,
                                    container_name,
                                    new_object_name))
                            return HttpResponseRedirect('/userdashboard/')
                    folder.name = new_folder_name
                    folder.type = filetype
                    folder.save()
                if folder.isFile == 0:
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=new_folder_name,
                        parentID=root_base_id[0].id,
                        isFile=0,
                        level=2,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            u'这一级目录下已经存在一个名为\'%s\'的文件夹!' % (
                                new_folder_name))
                        return HttpResponseRedirect('/userdashboard/')
                    # create new container
                    new_container_name = u'%s-%d-%d' % (
                        new_folder_name,
                        userstorage[0].companyid, 2)
                    iswift_views.container_create(
                        swift_user,
                        swift_key,
                        swift_tenant,
                        new_container_name)
                    # list objects of old container
                    alter_base = folder_tree.objects.filter(
                        name=old_name,
                        companyid=userstorage[0].companyid,
                        isFile=0,
                        parentID=root_base_id[0].id,
                        level=2)
                    # find all child file
                    all_file_child = folder_tree.objects.filter(
                        companyid=userstorage[0].companyid,
                        isFile=1,
                        parentID=alter_base[0].id,
                        level=3)
                    # copy children file to new container
                    old_c_name = u'%s-%d-%d' % (
                        old_name,
                        userstorage[0].companyid,
                        2)
                    for item in all_file_child:
                        if item.FileLink == 0:
                            orig_object_name = u'%s-%d-%d' % (
                                item.name,
                                userstorage[0].companyid,
                                3)
                            copy_success = iswift_views.copy_object(
                                swift_user,
                                swift_key,
                                swift_tenant,
                                old_c_name,
                                orig_object_name,
                                new_container_name,
                                orig_object_name)
                            if copy_success:
                                iswift_views.delete_an_objcte(
                                    swift_user,
                                    swift_key,
                                    swift_tenant,
                                    old_c_name,
                                    orig_object_name)
                            else:
                                messages.error(
                                    request,
                                    u'From container: \'%s\' copy object: '
                                    '\'%s\'to container: \'%s\' as new '
                                    'Object: \'%s\'failed.' % (
                                        old_c_name,
                                        orig_object_name,
                                        new_container_name,
                                        orig_object_name))
                                return HttpResponseRedirect('/userdashboard/')
                    iswift_views.delete_empty_container(swift_user,
                                                        swift_key,
                                                        swift_tenant,
                                                        old_c_name)
                    folder.name = new_folder_name
                    folder.save()
                messages.success(request,
                                 u'原文件(夹)\'%s\'修改为\'%s\'成功!' % (
                                     old_name,
                                     new_folder_name))
                return HttpResponseRedirect('/userdashboard/')
            else:
                item = folder_tree.objects.filter(
                    name=folder_list[folder_list_length - 3]).filter(
                        level=folder_list_length - 1)
                folder = folder_tree.objects.get(
                    name=old_name,
                    parentID=item[0].id,
                    level=folder_list_length,
                    companyid=userstorage[0].companyid)
                parent_folder = folder_list[0:folder_list_length - 2]
                parent_folder = '/'.join(parent_folder)
                urls = u'%s%s' % ('/userdashboard/', parent_folder)
                if folder.isFile == 1:
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=new_folder_name,
                        parentID=item[0].id,
                        isFile=1,
                        level=folder_list_length,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            'File existed: %s' % new_folder_name)
                        return HttpResponseRedirect(urls)
                    if folder.FileLink == 0:
                        container_name = u'%s-%d-%d' % (
                            folder_list[folder_list_length - 3],
                            userstorage[0].companyid,
                            folder_list_length - 1)
                        orig_object_name = u'%s-%d-%d' % (
                            old_name,
                            userstorage[0].companyid,
                            folder_list_length)
                        new_object_name = u'%s-%d-%d' % (
                            new_folder_name,
                            userstorage[0].companyid,
                            folder_list_length)
                        copy_success = iswift_views.copy_object(
                            swift_user, swift_key,
                            swift_tenant,
                            container_name, orig_object_name,
                            container_name, new_object_name)
                        if copy_success:
                            iswift_views.delete_an_objcte(
                                swift_user, swift_key,
                                swift_tenant, container_name,
                                orig_object_name)
                        else:
                            messages.error(
                                request,
                                u'From container: \'%s\' copy object: '
                                '\'%s\'to container: \'%s\' as new Object: '
                                '\'%s\'failed.' % (
                                    container_name,
                                    orig_object_name,
                                    container_name,
                                    new_object_name))
                            return HttpResponseRedirect(urls)
                    folder.name = new_folder_name
                    folder.type = filetype
                    folder.save()
                if folder.isFile == 0:
                    isNewNameAlreadyIN = folder_tree.objects.filter(
                        name=new_folder_name,
                        parentID=item[0].id,
                        isFile=0,
                        level=folder_list_length,
                        companyid=userstorage[0].companyid)
                    if len(isNewNameAlreadyIN) > 0:
                        messages.warning(
                            request,
                            u'这一级目录下已经存在一个名为\'%s\'的文件夹!' % (
                                new_folder_name))
                        return HttpResponseRedirect(urls)
                    # create new container
                    new_container_name = u'%s-%d-%d' % (
                        new_folder_name,
                        userstorage[0].companyid,
                        folder_list_length)
                    iswift_views.container_create(
                        swift_user,
                        swift_key,
                        swift_tenant,
                        new_container_name)
                    # list objects of old container
                    alter_base = folder_tree.objects.filter(
                        name=old_name,
                        companyid=userstorage[0].companyid,
                        isFile=0,
                        level=folder_list_length)
                    # find all child file
                    all_file_child = folder_tree.objects.filter(
                        companyid=userstorage[0].companyid,
                        isFile=1,
                        parentID=alter_base[0].id,
                        level=folder_list_length + 1)
                    # copy children file to new container
                    old_c_name = u'%s-%d-%d' % (old_name,
                                                userstorage[0].companyid,
                                                folder_list_length)
                    for item in all_file_child:
                        if item.FileLink == 0:
                            orig_object_name = '%s-%d-%d' % (
                                item.name,
                                userstorage[0].companyid,
                                folder_list_length + 1)
                            copy_success = iswift_views.copy_object(
                                swift_user,
                                swift_key,
                                swift_tenant,
                                old_c_name,
                                orig_object_name,
                                new_container_name,
                                orig_object_name)
                            if copy_success:
                                iswift_views.delete_an_objcte(
                                    swift_user,
                                    swift_key,
                                    swift_tenant,
                                    old_c_name,
                                    orig_object_name)
                            else:
                                messages.error(
                                    request,
                                    u'From container: \'%s\' copy object: \'%s'
                                    '\'to container: \'%s\' as new Object: '
                                    '\'%s\'failed.' % (
                                        old_c_name,
                                        orig_object_name,
                                        new_container_name,
                                        orig_object_name))
                                return HttpResponseRedirect(urls)
                    iswift_views.delete_empty_container(
                        swift_user,
                        swift_key,
                        swift_tenant,
                        old_c_name)
                    folder.name = new_folder_name
                    folder.save()
                messages.success(request,
                                 u'原文件(夹)\'%s\'修改为\'%s\'成功!' % (
                                     old_name,
                                     new_folder_name))
                return HttpResponseRedirect(urls)
        if request.method == 'GET':
            messages.error(request, 'Only Post Method support!')
            return HttpResponseRedirect('/userdashboard')
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def mysharedfiles(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'logo_link': '#',
             'file_pic': 'page_icon_folder_32',
             'share_files_class': 'current'}
        return render_to_response(user_dashboard_templates,
                                  c,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def deletedfiles(request):
    if request.user.is_authenticated():
        username = request.user.username
        user_company_id = user_storage.objects.filter(
            name=username,
            user_id=request.user.id)
        root_base_id = folder_tree.objects.filter(
            name='BASEROOT',
            level=1,
            companyid=user_company_id[0].companyid)

        books = folder_tree.objects.order_by('companyid').filter(
            parentID=root_base_id[0].id,
            companyid=user_company_id[0].companyid)
        retlist = []
        for first in books:
            if (user_company_id[0].competence >= first.competence
                    and first.isDeleted > 0):
                retlist.append(first)
        c = {'username': username,
             'is_container_list': True,
             'container_root': '#',
             'logo_link': '#',
             'file_pic': 'page_icon_folder_32',
             'containers': retlist,
             'recycle_files_class': 'current'}
        return render_to_response(user_dashboard_templates,
                                  c,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def filesversion(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'logo_link': '#',
             'file_pic': 'page_icon_folder_32',
             'version_files_class': 'current'}
        return render_to_response(user_dashboard_templates,
                                  c,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')
