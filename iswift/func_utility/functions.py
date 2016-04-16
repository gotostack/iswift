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

from iswift.folderlist.models import company_tree
from iswift.folderlist.models import folder_tree


def isFileAlreadyIN(name, parentID, type, level, companyid):
    finder = folder_tree.objects.filter(
        name=name,
        parentID=parentID,
        isFile=type,
        level=level,
        companyid=companyid)
    if len(finder) > 0:
        return True
    return False


def getOpenstakTenantKey(companyid):
    company_token = company_tree.objects.filter(id=companyid)
    swift_user = company_token[0].keystone_user_id
    swift_key = company_token[0].keystone_passwd
    swift_tenant = company_token[0].keystone_tenant
    return (swift_user, swift_key, swift_tenant)
