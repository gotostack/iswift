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

import os
from random import randint

from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from iswift.folderlist.models import company_tree
from iswift.folderlist.models import user_storage
from iswift.swiftapi import messages


def superlogin(request):
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
                return HttpResponseRedirect('/mng/superadmin/')
            else:
                messages.error(request, 'Invaild username or password.')
    return render_to_response(
        'logined/admintemplates/superadmin/superlogin.html',
        {'logo_link': '/'}, context_instance=RequestContext(request))


def supermanage(request):
    if request.user.is_authenticated():
        username = request.user.username
        pam = []
        request.session['networkdata'] = pam
        request.session['maxnum'] = 0
        user_company_id = user_storage.objects.filter(
            name=username).filter(user_id=request.user.id)
        user_company = company_tree.objects.filter(
            id=user_company_id[0].companyid)
        ret = u"%s%s的%s" % (u'来自:', user_company[0].name, username)
        c = {'username': ret,
             'container_root': '#',
             'logo_link': '#',
             'supamin_current': 'current'}
        return render_to_response(
            'logined/admintemplates/superadmin/superdashboard.html',
            c,
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/mng/superlogin/')


def networkdata(request):
    js1 = ''
    pam = request.session['networkdata']
    max = request.session['maxnum']
    i = 0
    while len(pam) != 40:
            value1 = randint(40, 50)
            value2 = randint(30, 60)
            value3 = randint(50, 60)
            item = '%s%d%s%d%s%d%s%d%s' % (
                "{'date':'", i + 1,
                "' ,'value':'", value1,
                "','value2':'", value2,
                "','value3':'", value3, "'},")
            pam.append(item)
            i = i + 1
    value1 = randint(40, 50)
    value2 = randint(30, 60)
    value3 = randint(50, 60)
    newdata = '%s%d%s%d%s%d%s%d%s' % (
        "{date:", max + 1,
        " ,value:", value1,
        ",value2:", value2,
        ",value3:", value3, "},")
    pam = pam[1:40]
    pam.append(newdata)
    request.session['networkdata'] = pam
    request.session['maxnum'] = max + 1
    for item in pam:
        js1 = js1 + item
    return HttpResponse('[' + js1 + ']')


def suptenants(request):
    if request.user.is_authenticated():
        username = request.user.username
        companys = company_tree.objects.order_by('id')
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'suptenants_current': 'current',
             'companys': companys}
        return render_to_response(
            'logined/admintemplates/superadmin/super_suptenants.html',
            c,
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/mng/superlogin/')


def storate_spaces(request):
    if request.user.is_authenticated():
        username = request.user.username
        companys = company_tree.objects.order_by('id')
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'supspace_current': 'current',
             'companys': companys}
        return render_to_response(
            'logined/admintemplates/superadmin/super_spaces.html',
            c,
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/mng/superlogin/')


def cmpspaces(request):
    user_company = company_tree.objects.order_by('id')
    js1 = '['
    for item in user_company:
        space = int(item.storage_size / (1024 * 1024 * 1024))
        name = item.name
        js1 += '%s%s%s%d%s' % ("{country: \"",
                               name,
                               "\",value:",
                               space,
                               "},")
    js1 += ']'
    return HttpResponse(js1)


def storage_nodes(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'supnode_current': 'current'}
        return render_to_response(
            'logined/admintemplates/superadmin/super_nodes.html',
            c,
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/mng/superlogin/')


def storage_balance(request):
    if request.user.is_authenticated():
        username = request.user.username
        c = {'username': username,
             'container_root': '#',
             'logo_link': '#',
             'supblnc_current': 'current'}
        return render_to_response(
            'logined/admintemplates/superadmin/super_belance.html',
            c,
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/mng/superlogin/')


def fadecpudata(request):
    r = os.popen(
        'top -bi -n 2 -d 0.02').read().split(
        '\n\n\n')[1].split('\n')[2].split(':')[1].split(',')[0].split('%')[0]
    return HttpResponse(r)
