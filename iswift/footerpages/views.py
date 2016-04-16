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
from django import forms
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from iswift.folderlist.models import company_tree
from iswift.folderlist.models import folder_tree
from iswift.folderlist.models import user_storage
from iswift.footerpages.models import users_message
from iswift.privatefiles.models import users_folder_tree
from iswift.swiftapi import messages
from iswift.swiftapi import views as iswift_views
from iswift.swiftapi.views import StringMD5


def iscprght(request):
    return render_to_response('footerpages/footer_iscprght.html', {})


def install(request):
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': '下载与安装',
                               'infotitle': '下载与安装'})


def mobile(request):
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': '移动终端',
                               'infotitle': '移动终端'})


def pricing(request):
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': '价格',
                               'infotitle': '费用价格'})


def teams(request):
    return render_to_response('footerpages/footer_ourteam.html',
                              {'logo_link': '/',
                               'pagetitle': '小组',
                               'infotitle': '小组'})


def tour(request):
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': '体验',
                               'infotitle': '体验'})


def terms(request):
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': 'Privacy & Terms',
                               'infotitle': 'Privacy & Terms'})


def userhelp(request):
    return render_to_response('footerpages/footer_userhelp.html',
                              {'logo_link': '/',
                               'pagetitle': '帮助中心',
                               'infotitle': '帮助中心'})


def jobs(request):
    return render_to_response('footerpages/footer_jobs.html',
                              {'logo_link': '/',
                               'pagetitle': '加入我们',
                               'infotitle': '加入我们'})


def developers(request):
    return render_to_response('footerpages/footer_developer.html',
                              {'logo_link': '/',
                               'pagetitle': '开发人员',
                               'infotitle': '开发人员'})


def about(request):
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': '我们的队伍',
                               'infotitle': '我们的队伍'})


def news(request):
    return render_to_response('footerpages/footer_news.html',
                              {'logo_link': '/',
                               'pagetitle': '新闻',
                               'infotitle': '新闻'})


class ContactForm(forms.Form):
    subject = forms.CharField(required=True,
                              max_length=100,
                              label='姓名')
    email = forms.EmailField(required=True,
                             label='email')
    message = forms.CharField(required=True,
                              widget=forms.Textarea,
                              label='消息')
    VerifyCode = forms.CharField(required=True,
                                 max_length=4,
                                 label='验证码')

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError(u"您输入的消息太短!")
        return message


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            clientcode = cd['VerifyCode']
            servercode = request.session['verify']
            if servercode != clientcode:
                messages.error(request, u"验证码不正确！")
            else:
                messages.success(request, u"提交成功！")
                message = users_message(subject=cd['subject'],
                                        email=cd['email'],
                                        message=cd['message'])
                message.save()
            return http.HttpResponseRedirect('/contact/')
    else:
        form = ContactForm()
    return render_to_response('footerpages/contact_form.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return http.HttpResponse('<table>%s</table>' % '\n'.join(html))


def register_view(request):
    username = ''
    telephone = ''
    password = ''
    cfpassword = ''
    companyname = ''
    companytenant = ''
    companyaddress = ''
    companysize = 0
    companyusers = 0
    isFromOK = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        telephone = request.POST.get('telephone', '')
        password = request.POST.get('password', '')
        cfpassword = request.POST.get('confirm', '')
        companyname = request.POST.get('companyname', '')
        companytenant = request.POST.get('companytenant', '')
        companyaddress = request.POST.get('companyaddress', '')
        companysize = int(request.POST.get('companysize', ''))
        companyusers = int(request.POST.get('companyusers', ''))
        if not username:
            isFromOK = False
            messages.error(request, u'Please Enter a username.')
        if not telephone:
            isFromOK = False
            messages.error(request, u'Please Enter a telephone number.')
        if not password:
            isFromOK = False
            messages.error(request, u'Please Enter a password.')
        if not cfpassword:
            isFromOK = False
            messages.error(request, u'Please confirm password.')
        if password != cfpassword:
            isFromOK = False
            messages.error(request, u'Please password is not same.')
        if not companyname:
            isFromOK = False
            messages.error(request, u'Please Enter a companyname.')
        if not companytenant:
            isFromOK = False
            messages.error(request, u'Please Enter a companytenant.')
        if not companyaddress:
            isFromOK = False
            messages.error(request, u'Please Enter a companyaddress.')
        if 0 == companysize:
            isFromOK = False
            messages.error(request, u'Please select a companysize.')
        if 0 == companyusers:
            isFromOK = False
            messages.error(request, u'Please select a employee quantity.')
        if isFromOK:
            companysize = companysize * 1024 * 1024 * 1024

            user = auth.models.User.objects.filter(username=username)
            if len(user) > 0:
                messages.error(request, u'User already exists.')
                return http.HttpResponseRedirect('/register/')

            user_company = company_tree.objects.filter(name=companyname)
            if len(user_company) > 0:
                messages.error(request, u'Company already exists.')
                return http.HttpResponseRedirect('/register/')

            user = auth.models.User(username=username,
                                    email=username,
                                    password=make_password(password))
            user.save()
            user = auth.authenticate(username=username,
                                     password=password)

            if iswift_views.create_tenant(
                    tenant_name=companytenant,
                    tenant_description=companyname,
                    user_name=companytenant,
                    user_password=StringMD5(password),
                    user_email=username):
                user_company = company_tree(
                    name=companyname,
                    address=companyaddress,
                    storage_size=companysize,
                    used_size=0,
                    employee_quantity=companyusers,
                    keystone_tenant=companytenant,
                    keystone_user_id=companytenant,
                    keystone_passwd=StringMD5(password))
                user_company.save()
                user_company = company_tree.objects.filter(name=companyname)

                user_base_foler = folder_tree(
                    name='BASEROOT',
                    type=0,
                    parentID=0,
                    isFile=0,
                    level=1,
                    companyid=user_company[0].id,
                    isContainer=1,
                    sizebyte=0,
                    competence=10,
                    MD5string='',
                    SHA1string='',
                    CRC32string='',
                    FileLink=0,
                    isDeleted=0)
                user_base_foler.save()

                container_name = '%s-%d' % ('BASEROOT',
                                            user_company[0].id)
                iswift_views.container_create(
                    user=user_company[0].keystone_user_id,
                    key=user_company[0].keystone_passwd,
                    tenant_name=user_company[0].keystone_tenant,
                    container_name=container_name)

                user_base_foler = users_folder_tree(
                    name='BASEROOT',
                    type=0,
                    parentID=0,
                    isFile=0,
                    level=1,
                    companyid=user_company[0].id,
                    user_id=user.id,
                    isContainer=1,
                    sizebyte=0,
                    competence=10,
                    MD5string='',
                    SHA1string='',
                    CRC32string='',
                    FileLink=0,
                    isDeleted=0)
                user_base_foler.save()

                container_name = '%s-%d-%d' % ('BASEROOT',
                                               user_company[0].id, user.id)
                iswift_views.container_create(
                    user=user_company[0].keystone_user_id,
                    key=user_company[0].keystone_passwd,
                    tenant_name=user_company[0].keystone_tenant,
                    container_name=container_name)

                userstorage = user_storage(
                    user_id=user.id,
                    name=user.username,
                    telephone=telephone,
                    storage_size=0,
                    used_size=0,
                    companyid=user_company[0].id,
                    competence=10)
                userstorage.save()
                messages.success(request, u'注册成功！ 请登录')
                return http.HttpResponseRedirect('/')
            else:
                messages.error(request, u'Create Tenant ERROR!')
                return http.HttpResponseRedirect('/register/')
    return render_to_response('footerpages/footer_pages_template.html',
                              {'logo_link': '/',
                               'pagetitle': 'Sign In',
                               'register_form': 'register_form',
                               'username': username,
                               'telephone': telephone,
                               'password': password,
                               'confirm': cfpassword,
                               'companyname': companyname,
                               'companyaddress': companyaddress,
                               'companysize': companysize,
                               'companyusers': companyusers},
                              context_instance=RequestContext(request))
