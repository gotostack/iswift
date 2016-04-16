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

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


from iswift.folderlist.models import company_tree
from iswift.folderlist.models import user_storage
from iswift.privatefiles.models import users_folder_tree
from iswift.swiftapi import messages
from iswift.swiftapi import views as iswift_views


user_dashboard_templates = 'logined/privatefiles/userdashboard.html'


def privatefiles(request):
    if request.user.is_authenticated():
        username = request.user.username
        user_company_id = user_storage.objects.filter(name=username,
                                                      user_id=request.user.id)
        root_base_id = users_folder_tree.objects.filter(
            name='BASEROOT',
            level=1,
            companyid=user_company_id[0].companyid,
            user_id=request.user.id)

        books = users_folder_tree.objects.order_by('companyid').filter(
            parentID=root_base_id[0].id,
            companyid=user_company_id[0].companyid,
            user_id=request.user.id)
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
             'private_files_class': 'current'}
        return render_to_response(user_dashboard_templates,
                                  c,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, u'请先登录！')
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
            link = '/privatefiles/'
            temp = temp_vec[0:i + 1]
            path = '/'.join(temp)
            link += path
            abe = {'name': temp_vec[i], 'link': link}
            fast_file_link.append(abe)

        user_company_id = user_storage.objects.filter(
            name=username, user_id=request.user.id)
        item = users_folder_tree.objects.filter(
            name=folder_list[folder_list_length - 2],
            level=folder_list_length,
            user_id=request.user.id,
            companyid=user_company_id[0].companyid,
            isDeleted=0)
        if len(item) > 0:
            folders = users_folder_tree.objects.filter(
                parentID=item[0].id).filter(isDeleted=0)
            files = []
            for folder in folders:
                if folder.FileLink >= 0:
                    files.append(folder)
            container_root = folder_list[0:folder_list_length - 2]
            container_str = ''
            container_str = '/'.join(container_root)
            container_str = '/privatefiles/%s' % container_str
            c = {'username': username,
                 'container_root': container_str,
                 'logo_link': '#',
                 'file_pic': 'page_icon_folder_32',
                 'containers': files,
                 'file_loaction': fast_file_link,
                 'private_files_class': 'current'}
            return render_to_response(
                user_dashboard_templates,
                c,
                context_instance=RequestContext(request))
        else:
            messages.error(request, u'文件夹\'%s\'不存在！' % path_folder)
            return HttpResponseRedirect('/privatefiles')
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
            root_base_id = users_folder_tree.objects.filter(
                name='BASEROOT',
                level=1,
                companyid=userstorage[0].companyid,
                user_id=request.user.id)
            if len(folder_list) <= 1:
                is_folder_already_have = users_folder_tree.objects.filter(
                    name=folder_name,
                    parentID=root_base_id[0].id,
                    isFile=0,
                    level=2,
                    user_id=request.user.id,
                    companyid=userstorage[0].companyid,
                    isContainer=1)
                if len(is_folder_already_have) >= 1:
                    urls = u'%s%s' % ('/privatefiles/', folder_name)
                    messages.info(
                        request,
                        u'文件夹\'%s\'已经存在, 并已经进入该文件夹！' % folder_name)
                    return HttpResponseRedirect(urls)
                folder = users_folder_tree(
                    name=folder_name,
                    type=0,
                    parentID=root_base_id[0].id,
                    isFile=0,
                    level=2,
                    companyid=userstorage[0].companyid,
                    user_id=request.user.id,
                    isContainer=1,
                    sizebyte=0,
                    competence=10,
                    MD5string='',
                    SHA1string='',
                    CRC32string='',
                    FileLink=0,
                    isDeleted=0)
                folder.save()

                company_token = company_tree.objects.filter(
                    id=userstorage[0].companyid)
                swift_user = company_token[0].keystone_user_id
                swift_key = company_token[0].keystone_passwd
                swift_tenant = company_token[0].keystone_tenant
                container_name = u'%s-%d-%d-%d' % (folder_name,
                                                   userstorage[0].companyid,
                                                   request.user.id,
                                                   2)
                iswift_views.container_create(swift_user,
                                              swift_key,
                                              swift_tenant,
                                              container_name)

                messages.success(request, u'%s%s%s' % (u'文件夹\'',
                                                       folder_name,
                                                       u'\'创建成功！'))
                return HttpResponseRedirect('/privatefiles/')
            else:
                folder_list_length = len(folder_list)
                item = users_folder_tree.objects.filter(
                    name=folder_list[folder_list_length - 2]).filter(
                        level=folder_list_length)
                is_folder_already_have = users_folder_tree.objects.filter(
                    name=folder_name,
                    parentID=item[0].id,
                    isFile=0,
                    level=folder_list_length + 1,
                    companyid=userstorage[0].companyid,
                    user_id=request.user.id,
                    isContainer=1)
                if len(is_folder_already_have) >= 1:
                    urls = '%s%s%s' % ('/privatefiles/',
                                       parent_folder,
                                       folder_name)
                    messages.info(
                        request,
                        (u'Folder \'%s%s\' existed , access to it.') % (
                            folder_name,
                            folder_name))
                    return HttpResponseRedirect(urls)
                folder = users_folder_tree(
                    name=folder_name,
                    type=0,
                    parentID=item[0].id,
                    isFile=0,
                    level=folder_list_length + 1,
                    companyid=userstorage[0].companyid,
                    user_id=request.user.id,
                    isContainer=1,
                    sizebyte=0,
                    competence=10,
                    MD5string='',
                    SHA1string='',
                    CRC32string='',
                    FileLink=0,
                    isDeleted=0)
                folder.save()

                company_token = company_tree.objects.filter(
                    id=userstorage[0].companyid)

                swift_user = company_token[0].keystone_user_id
                swift_key = company_token[0].keystone_passwd
                swift_tenant = company_token[0].keystone_tenant
                container_name = u'%s-%d-%d-%d' % (
                    folder_name,
                    userstorage[0].companyid,
                    request.user.id,
                    folder_list_length + 1)
                iswift_views.container_create(swift_user,
                                              swift_key,
                                              swift_tenant,
                                              container_name)
                messages.success(request,
                                 u'文件夹\'%s\'创建成功！' % folder_name)
                urls = u'%s%s' % ('/privatefiles/',
                                  parent_folder)
                return HttpResponseRedirect(urls)
        if request.method == 'GET':
            messages.error(request, 'Only Post Method support!')
            return HttpResponseRedirect('/privatefiles')
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
            file_name = contents.name

            smd5 = iswift_views.GetFileMd5(contents)
            ssha1 = iswift_views.GetFileSHA1(contents)
            contents.seek(0)

            FileLink = 0
            is_file_already_store = users_folder_tree.objects.filter(
                MD5string=smd5,
                SHA1string=ssha1,
                companyid=userstorage[0].companyid)

            file_type = file_name.split('.')
            filetype = iswift_views.FindFileType(
                file_type[len(file_type) - 1])

            if len(is_file_already_store) <= 0:
                if len(folder_list) <= 1:
                    root_base_id = users_folder_tree.objects.filter(
                        name='BASEROOT',
                        level=1,
                        companyid=userstorage[0].companyid)
                    folder = users_folder_tree(
                        name=file_name,
                        type=filetype,
                        parentID=root_base_id[0].id,
                        isFile=1,
                        level=2,
                        companyid=userstorage[0].companyid,
                        user_id=request.user.id,
                        isContainer=0,
                        sizebyte=contents.size,
                        competence=10,
                        MD5string=smd5,
                        SHA1string=ssha1,
                        CRC32string='',
                        FileLink=FileLink,
                        isDeleted=0)
                    folder.save()

                    company_token = company_tree.objects.filter(
                        id=userstorage[0].companyid)
                    swift_user = company_token[0].keystone_user_id
                    swift_key = company_token[0].keystone_passwd
                    swift_tenant = company_token[0].keystone_tenant
                    container_name = '%s-%d' % ('BASEROOT',
                                                userstorage[0].companyid)
                    object_name = '%s-%d-%d' % (file_name,
                                                userstorage[0].companyid,
                                                2)
                    if contents:
                        iswift_views.upload_object(swift_user,
                                                   swift_key,
                                                   swift_tenant,
                                                   container_name,
                                                   object_name,
                                                   contents)
                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect('/privatefiles/')
                else:
                    folder_list_length = len(folder_list)
                    item = users_folder_tree.objects.filter(
                        name=folder_list[folder_list_length - 2]).filter(
                            level=folder_list_length).filter(
                                companyid=userstorage[0].companyid)
                    folder = users_folder_tree(
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

                    company_token = company_tree.objects.filter(
                        id=userstorage[0].companyid)
                    swift_user = company_token[0].keystone_user_id
                    swift_key = company_token[0].keystone_passwd
                    swift_tenant = company_token[0].keystone_tenant
                    container_name = '%s-%d-%d' % (item[0].name,
                                                   userstorage[0].companyid,
                                                   folder_list_length)
                    object_name = '%s-%d-%d' % (file_name,
                                                userstorage[0].companyid,
                                                folder_list_length + 1)

                    if contents:
                        iswift_views.upload_object(swift_user,
                                                   swift_key,
                                                   swift_tenant,
                                                   container_name,
                                                   object_name,
                                                   contents)
                    usls = '%s%s' % ('/privatefiles/', parent_folder)
                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect(usls)
            else:
                FileLink = is_file_already_store[0].id
                if len(folder_list) <= 1:
                    root_base_id = users_folder_tree.objects.filter(
                        name='BASEROOT',
                        level=1,
                        companyid=userstorage[0].companyid)
                    folder = users_folder_tree(
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
                    messages.success(request, u'文件\'%s\'上传成功!' % file_name)
                    return HttpResponseRedirect('/privatefiles/')
                else:
                    folder_list_length = len(folder_list)
                    item = users_folder_tree.objects.filter(
                        name=folder_list[folder_list_length - 2]).filter(
                            level=folder_list_length).filter(
                                companyid=userstorage[0].companyid)
                    folder = users_folder_tree(
                        name=file_name,
                        type=filetype,
                        parentID=item[0].id,
                        isFile=1,
                        level=folder_list_length + 1,
                        companyid=userstorage[0].companyid,
                        user_id=request.user.id,
                        isContainer=0,
                        sizebyte=contents.size,
                        competence=10,
                        MD5string=smd5,
                        SHA1string=ssha1,
                        CRC32string='',
                        FileLink=FileLink,
                        isDeleted=0)
                    folder.save()
                    usls = '%s%s' % ('/privatefiles/', parent_folder)
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

        company_root = users_folder_tree.objects.filter(
            level=1,
            name='BASEROOT',
            companyid=userstorage[0].companyid)

        if len(container_name) <= 1:
            current_file = users_folder_tree.objects.filter(
                level=2,
                name=objects_name,
                parentID=company_root[0].id)
            if current_file[0].FileLink == 0:
                container_name = '%s-%d' % ('BASEROOT',
                                            userstorage[0].companyid)
                object_name = '%s-%d-%d' % (objects_name,
                                            userstorage[0].companyid,
                                            2)
                return iswift_views.get_object(swift_user,
                                               swift_key,
                                               swift_tenant,
                                               container_name,
                                               object_name,
                                               objects_name)
            else:
                link_file = users_folder_tree.objects.filter(
                    id=current_file[0].FileLink)
                parent_file = users_folder_tree.objects.filter(
                    id=link_file[0].parentID)
                container_name = ''
                if parent_file[0].name == 'BASEROOT':
                    container_name = '%s-%d' % ('BASEROOT',
                                                userstorage[0].companyid)
                else:
                    container_name = '%s-%d-%d' % (parent_file[0].name,
                                                   userstorage[0].companyid,
                                                   parent_file[0].level)
                object_name = '%s-%d-%d' % (link_file[0].name,
                                            userstorage[0].companyid,
                                            link_file[0].level)
                return iswift_views.get_object(swift_user,
                                               swift_key,
                                               swift_tenant,
                                               container_name,
                                               object_name,
                                               objects_name)
        else:
            level = len(container_name) + 1
            current_file = users_folder_tree.objects.filter(
                level=level,
                name=objects_name,
                companyid=userstorage[0].companyid)
            if current_file[0].FileLink == 0:
                folder_name = '%s-%d-%d' % (
                    container_name[len(container_name) - 2],
                    userstorage[0].companyid,
                    len(container_name))
                object_name = '%s-%d-%d' % (
                    objects_name,
                    userstorage[0].companyid,
                    len(container_name) + 1)
                return iswift_views.get_object(swift_user,
                                               swift_key,
                                               swift_tenant,
                                               folder_name,
                                               object_name,
                                               objects_name)
            else:
                link_file = users_folder_tree.objects.filter(
                    id=current_file[0].FileLink)
                parent_file = users_folder_tree.objects.filter(
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
                object_name = '%s-%d-%d' % (link_file[0].name,
                                            userstorage[0].companyid,
                                            link_file[0].level)
                return iswift_views.get_object(swift_user,
                                               swift_key,
                                               swift_tenant,
                                               container_name,
                                               object_name,
                                               objects_name)
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')


def filesearch(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            userstorage = user_storage.objects.filter(
                name=request.user.username,
                user_id=request.user.id)
            if 'fileserarch' in request.POST:
                fileserarch = request.POST['fileserarch']
                books = users_folder_tree.objects.filter(
                    companyid=userstorage[0].companyid,
                    user_id=request.user.id)
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
            root_base_id = users_folder_tree.objects.filter(
                name='BASEROOT',
                level=1,
                companyid=userstorage[0].companyid)
            folder_list_length = len(folder_list)
            file_name = folder_list[folder_list_length - 2]

            if folder_list_length <= 2:
                delete_item = users_folder_tree.objects.get(
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
                messages.success(request, u'文件（夹）\'%s\'删除成功！' % file_name)
                return HttpResponseRedirect('/privatefiles')
            else:
                delete_item = users_folder_tree.objects.get(
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
                urls = '%s%s' % ('/privatefiles/', parent_folder)
                messages.success(request, u'文件（夹）\'%s\'删除成功！' % file_name)
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
            root_base_id = users_folder_tree.objects.filter(
                name='BASEROOT', level=1, companyid=userstorage[0].companyid)
            folder_list_length = len(folder_list)
            company_token = company_tree.objects.filter(
                id=userstorage[0].companyid)

            swift_user = company_token[0].keystone_user_id
            swift_key = company_token[0].keystone_passwd
            swift_tenant = company_token[0].keystone_tenant

            file_type = new_folder_name.split('.')
            filetype = iswift_views.FindFileType(
                file_type[len(file_type) - 1])

            if folder_list_length <= 2:
                folder = users_folder_tree.objects.get(
                    name=old_name,
                    parentID=root_base_id[0].id,
                    level=2,
                    companyid=userstorage[0].companyid,)
                if folder.isFile == 1:
                    folder.name = new_folder_name
                    folder.type = filetype
                    folder.save()
                    container_name = u'%s-%d' % ('BASEROOT',
                                                 userstorage[0].companyid)
                    # copy new obj
                    orig_object_name = u'%s-%d-%d' % (
                        old_name,
                        userstorage[0].companyid,
                        2)
                    new_object_name = u'%s-%d-%d' % (
                        new_folder_name,
                        userstorage[0].companyid,
                        2)
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
                        iswift_views.delete_an_objcte(swift_user,
                                                      swift_key,
                                                      swift_tenant,
                                                      container_name,
                                                      orig_object_name)
                    else:
                        messages.error(
                            request,
                            (u'from container: \'%s\' copy object: \'%s\''
                             'to container: \'%s\' as '
                             'new Object: \'%s\'failed') % (
                                 container_name,
                                 orig_object_name,
                                 container_name,
                                 new_object_name))
                if folder.isFile == 0:
                    # create new container
                    new_container_name = u'%s-%d-%d' % (
                        new_folder_name,
                        userstorage[0].companyid,
                        2)
                    iswift_views.container_create(swift_user,
                                                  swift_key,
                                                  swift_tenant,
                                                  new_container_name)
                    # list objects of old container
                    alter_base = users_folder_tree.objects.filter(
                        name=old_name,
                        companyid=userstorage[0].companyid,
                        isFile=0,
                        parentID=root_base_id[0].id,
                        level=2)
                    # find all child file
                    all_file_child = users_folder_tree.objects.filter(
                        companyid=userstorage[0].companyid,
                        isFile=1,
                        parentID=alter_base[0].id,
                        level=3)
                    folder.name = new_folder_name
                    folder.save()
                    # copy children file to new container
                    old_c_name = u'%s-%d-%d' % (
                        old_name, userstorage[0].companyid, 2)
                    for item in all_file_child:
                        if item.FileLink == 0:
                            orig_object_name = '%s-%d-%d' % (
                                item.name, userstorage[0].companyid, 3)
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
                                    '\'%s\'to container: \'%s\' '
                                    'as new Object: \'%s\'faile.' % (
                                        old_c_name,
                                        orig_object_name,
                                        new_container_name,
                                        orig_object_name))
                    iswift_views.delete_empty_container(
                        swift_user, swift_key, swift_tenant, old_c_name)
                messages.success(
                    request,
                    (u'original file (folder)\'%s\'was modified '
                     'to \'%s\' success!') % (old_name,
                                              new_folder_name))
                return HttpResponseRedirect('/privatefiles/')
            else:
                item = users_folder_tree.objects.filter(
                    name=folder_list[folder_list_length - 3]
                ).filter(level=folder_list_length - 1)
                folder = users_folder_tree.objects.get(
                    name=old_name,
                    parentID=item[0].id,
                    level=folder_list_length,
                    companyid=userstorage[0].companyid)
                parent_folder = folder_list[0:folder_list_length - 2]
                parent_folder = '/'.join(parent_folder)
                urls = u'%s%s' % ('/privatefiles/', parent_folder)
                if folder.isFile == 1:
                    folder.name = new_folder_name
                    folder.type = filetype
                    folder.save()
                    container_name = u'%s-%d-%d' % (
                        folder_list[folder_list_length - 3],
                        userstorage[0].companyid,
                        folder_list_length - 1)
                    # copy new obj
                    orig_object_name = u'%s-%d-%d' % (
                        old_name,
                        userstorage[0].companyid,
                        folder_list_length)
                    new_object_name = u'%s-%d-%d' % (
                        new_folder_name,
                        userstorage[0].companyid,
                        folder_list_length)
                    copy_success = iswift_views.copy_object(
                        swift_user, swift_key, swift_tenant,
                        container_name, orig_object_name,
                        container_name, new_object_name)
                    if copy_success:
                        # delete old obj
                        iswift_views.delete_an_objcte(swift_user,
                                                      swift_key,
                                                      swift_tenant,
                                                      container_name,
                                                      orig_object_name)
                    else:
                        messages.error(
                            request,
                            u'From container: '
                            '\'%s\' copy object: \'%s\'to container: \'%s\''
                            ' as new Object: \'%s\'faile.' % (
                                container_name,
                                orig_object_name,
                                container_name,
                                new_object_name))
                        return HttpResponseRedirect(urls)
                if folder.isFile == 0:
                    # create new container
                    new_container_name = u'%s-%d-%d' % (
                        new_folder_name,
                        userstorage[0].companyid,
                        folder_list_length)
                    iswift_views.container_create(swift_user,
                                                  swift_key,
                                                  swift_tenant,
                                                  new_container_name)
                    # list objects of old container
                    alter_base = users_folder_tree.objects.filter(
                        name=old_name,
                        companyid=userstorage[0].companyid,
                        isFile=0,
                        level=folder_list_length)
                    # find all child file
                    all_file_child = users_folder_tree.objects.filter(
                        companyid=userstorage[0].companyid,
                        isFile=1,
                        parentID=alter_base[0].id,
                        level=folder_list_length + 1)
                    folder.name = new_folder_name
                    folder.save()
                    # copy children file to new container
                    old_c_name = u'%s-%d-%d' % (
                        old_name,
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
                                    u'From container: \'%s\' copy object: '
                                    '\'%s\'to container: \'%s\' '
                                    'as new Object: \'%s\'faile.' % (
                                        old_c_name,
                                        orig_object_name,
                                        new_container_name,
                                        orig_object_name))
                                return HttpResponseRedirect(urls)
                    iswift_views.delete_empty_container(swift_user,
                                                        swift_key,
                                                        swift_tenant,
                                                        old_c_name)
                messages.success(
                    request,
                    (u'original file (folder)\'%s\'was modified '
                     'to \'%s\' success!') % (old_name,
                                              new_folder_name))
                return HttpResponseRedirect(urls)
        if request.method == 'GET':
            messages.error(request, 'Only Post Method support!')
            return HttpResponseRedirect('/privatefiles')
    else:
        messages.error(request, u'请先登录!')
        return HttpResponseRedirect('/')
