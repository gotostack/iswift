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

from django.db import models


class folderlist(models.Model):
    name = models.CharField(max_length=128)
    parentname = models.CharField(max_length=128)
    sonname = models.CharField(max_length=60)
    isFile = models.BooleanField()


class folder_tree(models.Model):
    name = models.CharField(max_length=256)
    type = models.IntegerField(max_length=128)
    parentID = models.IntegerField(max_length=128)
    isFile = models.BooleanField()
    sizebyte = models.BigIntegerField(max_length=128)
    level = models.IntegerField(max_length=128)
    companyid = models.IntegerField(max_length=128)
    isContainer = models.BooleanField()
    competence = models.IntegerField(max_length=128)
    MD5string = models.CharField(max_length=256)
    SHA1string = models.CharField(max_length=256)
    CRC32string = models.CharField(max_length=256)
    FileLink = models.FloatField(max_length=128)
    isDeleted = models.IntegerField(max_length=128)


class company_tree(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    storage_size = models.BigIntegerField(max_length=128)
    used_size = models.BigIntegerField(max_length=128)
    employee_quantity = models.IntegerField(max_length=128)
    keystone_tenant = models.CharField(max_length=128)
    keystone_user_id = models.CharField(max_length=128)
    keystone_passwd = models.CharField(max_length=128)


class user_storage(models.Model):
    user_id = models.IntegerField(max_length=128)
    name = models.CharField(max_length=128)
    telephone = models.CharField(max_length=128)
    storage_size = models.IntegerField(max_length=128)
    used_size = models.IntegerField(max_length=128)
    companyid = models.IntegerField(max_length=128)
    competence = models.IntegerField(max_length=128)


class block_hashtable(models.Model):
    MD5string = models.CharField(max_length=256)
    SHA1string = models.CharField(max_length=256)
    CRC32string = models.CharField(max_length=256)
    next = models.IntegerField(max_length=128)
