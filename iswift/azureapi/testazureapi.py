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


def get_blob_service(username=None, key=None):
    blob_service = storage.BlobService(
        account_name='portalvhds566klfftsqsr7',
        account_key='xFwS67H28IWJUseqG5I9ZFSBcxNzBkdXgLFIALM9'
        '+0PVmBlw+GeO0dVo8j7rmfhasXyZtiPux5EYIu5mUnbuhg==.')
    return blob_service


def list_objects():
    blob_service = get_blob_service()
    blobs = blob_service.list_blobs('docpocket')
    for blob in blobs:
        print(blob.name)
        print(blob.url)
        print(blob)


list_objects()


def get_container_list():
    blob_service = get_blob_service()
    container_list = blob_service. list_containers()
    for blob in container_list:
        print(blob.name)
        print(blob.url)


def list_object_detail(container_name, blob_name):
    blob_service = get_blob_service()
    object_detail = blob_service.get_blob_properties(
        container_name=container_name, blob_name=blob_name)
    return object_detail


def list_container_objects(container_name):
    blob_service = get_blob_service()
    blobs = blob_service.list_blobs(container_name)
    return blobs


object_detail = list_container_objects('docpocket')


def list_container_detail(container_name):
    blob_service = get_blob_service()
    container_detail = blob_service.get_container_properties(container_name)
    return container_detail


def upload_object():
    blob_service = get_blob_service()
    myblob = open(r'azureapi.py', 'r').read()
    blob_service.put_blob('docpocket', 'azureapi.py',
                          myblob, x_ms_blob_type='BlockBlob')


def create_container_subfolder(container_name, folder_name):
    try:
        blob_service = get_blob_service()
    except Exception:
        return False
    containername = ('%s%s%s' % (container_name, "-subfolder-", folder_name))
    blob_service.create_container(containername)
    return True
