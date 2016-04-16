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

from django.core.urlresolvers import reverse
from django.core import validators
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django import http
from django.views import generic as generic

from iswift.swiftapi import jsonutils
from iswift.swiftapi import views

import logging


LOG = logging.getLogger(__name__)
FOLDER_DELIMITER = "/"
no_slash_validator = validators.RegexValidator(r'^(?u)[^/]+$',
                                               "Slash is not an allowed "
                                               "character.",
                                               code="noslash")


class SelfHandlingMixin(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        if not hasattr(self, "handle"):
            raise NotImplementedError("%s does not define a handle method."
                                      % self.__class__.__name__)
        super(SelfHandlingMixin, self).__init__(*args, **kwargs)


class SelfHandlingForm(SelfHandlingMixin, forms.Form):
    """SelfHandlingForm.

    A base :class:`Form <django:django.forms.Form>` class which includes
    processing logic in its subclasses.
    """
    def api_error(self, message):
        """api_error.

        Adds an error to the form's error dictionary after validation
        based on problems reported via the API. This is useful when you
        wish for API errors to appear as errors on the form rather than
        using the messages framework.
        """
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class ModalFormMixin(object):
    def get_template_names(self):
        if self.request.is_ajax():
            if not hasattr(self, "ajax_template_name"):
                # Transform standard template name to ajax name (leading "_")
                bits = list(os.path.split(self.template_name))
                bits[1] = "".join(("_", bits[1]))
                self.ajax_template_name = os.path.join(*bits)
            template = self.ajax_template_name
        else:
            template = self.template_name
        return template


class APIDictWrapper(object):
    """Simple wrapper for api dictionaries.

    Some api calls return dictionaries.  This class provides identical
    behavior as APIResourceWrapper, except that it will also behave as a
    dictionary, in addition to attribute accesses.

    Attribute access is the preferred method of access, to be
    consistent with api resource objects from novclient.
    """
    def __init__(self, apidict):
        self._apidict = apidict

    def __getattr__(self, attr):
        try:
            return self._apidict[attr]
        except KeyError:
            msg = 'Unknown attribute "%(attr)s" on APIResource object ' \
                  'of type "%(cls)s"' % {'attr': attr, 'cls': self.__class__}
            raise AttributeError(msg)

    def __getitem__(self, item):
        try:
            return self.__getattr__(item)
        except AttributeError as e:
            # caller is expecting a KeyError
            raise KeyError(e)

    def get(self, item, default=None):
        try:
            return self.__getattr__(item)
        except AttributeError:
            return default


class StorageObject(APIDictWrapper):
    def __init__(self, apidict, container_name, orig_name=None, data=None):
        super(StorageObject, self).__init__(apidict)
        self.container_name = container_name
        self.orig_name = orig_name
        self.data = data


class UploadObject(SelfHandlingForm):
    path = forms.CharField(max_length=255,
                           required=False,
                           widget=forms.HiddenInput)
    name = forms.CharField(max_length=255,
                           label="Object Name",
                           validators=[no_slash_validator])
    object_file = forms.FileField(label="File", allow_empty_file=True)
    container_name = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, authurl, user, key, retries=5, preauthurl=None,
                 preauthtoken=None, snet=False, starting_backoff=1,
                 tenant_name=None, os_options={}, auth_version="1"):
        self.authurl = authurl
        self.user = user
        self.key = key
        self.retries = retries
        self.http_conn = None
        self.url = preauthurl
        self.token = preauthtoken
        self.attempts = 0
        self.snet = snet
        self.starting_backoff = starting_backoff
        self.auth_version = auth_version
        if tenant_name:
            os_options['tenant_name'] = tenant_name
        self.os_options = os_options

    def handle(self, request, data, container_name, object_name, contents):
        object_file = self.files['object_file']
        if data['path']:
            object_path = "/".join([data['path'].rstrip("/"), data['name']])
        else:
            object_path = data['name']
        try:
            headers = {}
            headers['X-Object-Meta-Orig-Filename'] = object_file.name
            connection = views.get_connection(
                authurl=self.authurl,
                user=self.user,
                key=self.key,
                retries=5, preauthurl=None,
                preauthtoken=None, snet=False, starting_backoff=1,
                tenant_name=self.tenant_name, os_options={},
                auth_version="2.0")
            etag = connection.put_object(data['container_name'],
                                         object_path,
                                         object_file,
                                         headers)
            obj_info = {'name': object_name,
                        'bytes': object_file.size,
                        'etag': etag}
            return StorageObject(obj_info, container_name)
        except Exception:
            return None


ADD_TO_FIELD_HEADER = "HTTP_X_HORIZON_ADD_TO_FIELD"


class ModalFormView(ModalFormMixin, generic.FormView):
    def get_object_id(self, obj):
        return obj.id

    def get_object_display(self, obj):
        return obj.name

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception:
            handled = None
            # handle(self.request)

        if handled:
            if ADD_TO_FIELD_HEADER in self.request.META:
                field_id = self.request.META[ADD_TO_FIELD_HEADER]
                data = [self.get_object_id(handled),
                        self.get_object_display(handled)]
                response = http.HttpResponse(jsonutils.dumps(data))
                response["X-Horizon-Add-To-Field"] = field_id
            else:
                success_url = self.get_success_url()
                response = http.HttpResponseRedirect(success_url)
                # TODO(gabriel): This is not a long-term solution to how
                # AJAX should be handled, but it's an expedient solution
                # until the blueprint for AJAX handling is architected
                # and implemented.
                response['X-Horizon-Location'] = success_url
            return response
        else:
            # If handled didn't return, we can assume something went
            # wrong, and we should send back the form as-is.
            return self.form_invalid(form)


def wrap_delimiter(name):
    if not name.endswith(FOLDER_DELIMITER):
        return name + FOLDER_DELIMITER
    return name


class UploadView(ModalFormView):
    form_class = UploadObject
    template_name = 'nova/containers/upload.html'
    success_url = "horizon:nova:containers:index"

    def get_success_url(self):
        container_name = self.request.POST['container_name']
        return reverse(self.success_url,
                       args=(wrap_delimiter(container_name),
                             self.request.POST.get('path', '')))

    def get_initial(self):
        return {"container_name": self.kwargs["container_name"],
                "path": self.kwargs['subfolder_path']}

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        context['container_name'] = self.kwargs["container_name"]
        return context
