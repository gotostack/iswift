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

from azure import storage
from django.http import Http404
from django.http import HttpResponse


def get_blob_service(account_name=None, account_key=None):
    blob_service = storage.BlobService(
        account_name='portalvhds566klfftsqsr7',
        account_key='xFwS67H28IWJUseqG5I9ZFSBcxNzBkdXgLFIALM9+0PVmB'
        'lw+GeO0dVo8j7rmfhasXyZtiPux5EYIu5mUnbuhg==.')
    return blob_service


def get_user_auth(account_name=None, account_key=None):
    blob_service = storage.BlobService(account_name=account_name,
                                       account_key=account_key)
    return blob_service


def get_container_list():
    blob_service = get_blob_service()
    container_list = blob_service. list_containers()
    return container_list


def list_container_objects(container_name):
    blob_service = get_blob_service()
    blobs = blob_service.list_blobs(container_name)
    return blobs


def list_container_detail(container_name):
    blob_service = get_blob_service()
    container_detail = blob_service.get_container_properties(container_name)
    return container_detail


def list_object_detail(container_name, blob_name):
    blob_service = get_blob_service()
    object_detail = blob_service. get_blob_properties(
        container_name=container_name,
        blob_name=blob_name)
    return object_detail


def container_create(container_name):
    blob_service = get_blob_service()
    blob_service.create_container(container_name=container_name,
                                  x_ms_blob_public_access='container')
    return True


def upload_object(container_name, blob_name, blob_file):
    blob_service = get_blob_service()
    try:
        blob_service.put_blob(container_name=container_name,
                              blob_name=blob_name,
                              blob=blob_file,
                              x_ms_blob_type='BlockBlob')
    except Exception:
        return False
    return True


def get_object(user, key, tenant_name, container_name, blob_name):
    blob_service = get_blob_service()
    try:
        objectheaderanddata = blob_service. get_blob(
            container_name=container_name,
            blob_name=blob_name)
    except Exception:
        raise Http404

    filename = blob_name
    response = HttpResponse()
    safe_name = filename.replace(",", "").encode('utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s' % safe_name
    response['Content-Type'] = 'application/octet-stream'
    response.write(objectheaderanddata[1])
    return response


def update_container(container_name):
    blob_service = get_blob_service()
    blob_service.set_container_metadata(container_name=container_name)
    return True


def create_container_subfolder(container_name, folder_name):
    try:
        blob_service = get_blob_service()
    except Exception:
        return False
    containername = ('%s%s%s' % (container_name, "-subfolder-", folder_name))
    blob_service.create_container(containername)
    return True
