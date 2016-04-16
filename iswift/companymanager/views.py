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
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from iswift.folderlist.models import company_tree
from iswift.folderlist.models import user_storage
from iswift.privatefiles.models import users_folder_tree
from iswift.swiftapi import messages


def companylogin(request):
    username = ''
    password = ''
    isFromOK = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if not username:
            messages.error(request, 'please enter username')
            isFromOK = False
        if not password:
            messages.error(request, 'please enter password')
            isFromOK = False
        if isFromOK:
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/mng/companyadmin/')
            else:
                messages.error(request, u'错误的用户名或者密码！')
    return render_to_response(
        'logined/admintemplates/company/companylogin.html',
        {'logo_link': '/'},
        context_instance=RequestContext(request))


def companymanage(request):
    if request.user.is_authenticated():
        username = request.user.username
        current_user = user_storage.objects.filter(user_id=request.user.id,
                                                   name=username)
        user_company = company_tree.objects.filter(
            id=current_user[0].companyid)
        spaceall = user_company[0].storage_size
        spacerem = user_company[0].storage_size - user_company[0].used_size
        spaceinused = user_company[0].used_size
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'spaceall': spaceall,
             'spaceinused': spaceinused,
             'spacerem': spacerem,
             'cmpmain_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/companydashboard.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def storagedata(request):
    username = request.user.username
    current_user = user_storage.objects.filter(user_id=request.user.id,
                                               name=username)
    user_company = company_tree.objects.filter(id=current_user[0].companyid)
    empty_sp = user_company[0].storage_size - user_company[0].used_size
    empty_sp = int(empty_sp / (1024 * 1024))
    empty_used = int(user_company[0].used_size / (1024 * 1024))
    js1 = '%s%d%s%d%s' % ("[{country: \"已经使用\",value:",
                          empty_used,
                          "}, {country: \"可用空间\",value: ",
                          empty_sp,
                          "}]")
    return HttpResponse(js1)


def visitsnum(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmpvisit_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/visitsnum.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def loginsnum(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmplogin_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/loginsnum.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def publicfolder(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmppf_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/publicfolder.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def publicfile(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmppfile_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/publicfile.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def allocate(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmpalloc_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/allocate.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def spaceadmin(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmpapadmin_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/spaceadmin.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def orgs(request):
    if request.user.is_authenticated():
        username = request.user.username
        current_user = user_storage.objects.filter(user_id=request.user.id,
                                                   name=username)
        companyusers = user_storage.objects.filter(
            companyid=current_user[0].companyid)
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'companyusers': companyusers,
             'cmporgs_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/orgs.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def orgsmodify(request):
    if request.user.is_authenticated():
        optselect = 0
        newusername = ''
        useremail = ''
        telephone = ''
        competence = 0
        storagespace = 0
        userpassword = ''
        passwordconfirm = ''
        isFromOK = True
        if request.method == 'POST':
            username = request.user.username
            current_user = user_storage.objects.filter(
                user_id=request.user.id, name=username)
            optselect = int(request.POST.get('optselect', ''))
            newusername = request.POST.get('newusername', '')
            useremail = request.POST.get('useremail', '')
            telephone = request.POST.get('telephone', '')
            competence = int(request.POST.get('competence', ''))
            storagespace = int(request.POST.get('storagespace', ''))
            userpassword = request.POST.get('userpassword', '')
            passwordconfirm = request.POST.get('passwordconfirm', '')
            if not optselect:
                isFromOK = False
                messages.error(request, u'Please Enter a optselect.')
            if not newusername:
                isFromOK = False
                messages.error(request, u'Please Enter a newusername.')
            if not useremail:
                isFromOK = False
                messages.error(request, u'Please Enter a useremail.')
            if not competence:
                isFromOK = False
                messages.error(request, u'Please confirm competence.')
            if not storagespace:
                isFromOK = False
                messages.error(request, u'Please confirm storagespace.')
            if userpassword != passwordconfirm:
                isFromOK = False
                messages.error(request, u'Please password is not same.')
            if isFromOK:
                if optselect == 1:
                    user = auth.models.User.objects.filter(
                        username=newusername)
                    if len(user) > 0:
                        messages.error(request, u'User already exists.')
                        return HttpResponseRedirect('/mng/companyadmin/orgs/')
                    user = auth.models.User(
                        username=useremail,
                        email=useremail,
                        password=make_password(userpassword))
                    user.save()
                    user = auth.models.User.objects.filter(username=useremail)

                    userstorage = user_storage(
                        user_id=user[0].id,
                        name=useremail,
                        telephone=telephone,
                        storage_size=storagespace,
                        used_size=0,
                        companyid=current_user[0].companyid,
                        competence=competence)
                    userstorage.save()

                    user_base_foler = users_folder_tree(
                        name='BASEROOT',
                        type=0,
                        parentID=0,
                        isFile=0,
                        level=1,
                        companyid=current_user[0].companyid,
                        user_id=user[0].id,
                        isContainer=1,
                        sizebyte=0,
                        competence=competence,
                        MD5string='',
                        SHA1string='',
                        CRC32string='',
                        FileLink=0,
                        isDeleted=0)
                    user_base_foler.save()
                    messages.success(request, u'操作成功！')
                    return HttpResponseRedirect('/mng/companyadmin/orgs/')
                if optselect == 2:
                    messages.success(request, u'操作成功！')
                    return HttpResponseRedirect('/mng/companyadmin/orgs/')
                if optselect == 3:
                    messages.success(request, u'操作成功！')
                    return HttpResponseRedirect('/mng/companyadmin/orgs/')
                if optselect == 4:
                    messages.success(request, u'操作成功！')
                    return HttpResponseRedirect('/mng/companyadmin/orgs/')
                messages.error(request, u'未知操作类型！')
                return HttpResponseRedirect('/mng/companyadmin/orgs/')
        else:
            messages.error(request, u'Only POST Method Supported!')
            return HttpResponseRedirect('/mng/companyadmin/orgs/')
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def rights(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmprights_current': 'current'}
        return render_to_response('logined/admintemplates/company/rights.html',
                                  c,
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def spaceapply(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'cmpapply_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/spaceapply.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')


def versionapply(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'versionapply_current': 'current'}
        return render_to_response(
            'logined/admintemplates/company/versionapply.html',
            c,
            context_instance=RequestContext(request))
    else:
        messages.error(request, u'请登录先！')
        return HttpResponseRedirect('/mng/companylogin/')
