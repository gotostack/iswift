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

import binascii
import hashlib
import os

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)


def StringMD5(string):
    return hashlib.md5(string).hexdigest().upper()


def StringSHA1(string):
    return hashlib.sha1(string).hexdigest().upper()


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest().upper()


def GetFileSHA1(filename):
    if not os.path.isfile(filename):
        return
    m = hashlib.sha1()
    f = file(filename, 'rb')
    while True:
        data = f.read(8096)
        if not data:
            break
        m.update(data)
    f.close()
    return m.hexdigest().upper()


def StringCRC32(v):
    return '0x%x' % (binascii.crc32(v) & 0xffffffff)
