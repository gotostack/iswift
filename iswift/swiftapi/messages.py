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

"""
Drop-in replacement for django.contrib.messages which handles Horizon's
messaging needs (e.g. AJAX communication, etc.).
"""

from django.contrib import messages as _messages
from django.contrib.messages import constants
from django.utils.encoding import force_unicode


def add_message(request, level, message, extra_tags='', fail_silently=False):
    """Attempts to add a message to the request using the 'messages' app."""
    if request.is_ajax():
        tag = constants.DEFAULT_TAGS[level]
        request.horizon['async_messages'].append([tag,
                                                  force_unicode(message)])
    else:
        return _messages.add_message(request, level, message,
                                     extra_tags, fail_silently)


def debug(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``DEBUG`` level."""
    add_message(request, constants.DEBUG, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def info(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``INFO`` level."""
    add_message(request, constants.INFO, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def success(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``SUCCESS`` level."""
    add_message(request, constants.SUCCESS, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def warning(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``WARNING`` level."""
    add_message(request, constants.WARNING, message, extra_tags=extra_tags,
                fail_silently=fail_silently)


def error(request, message, extra_tags='', fail_silently=False):
    """Adds a message with the ``ERROR`` level."""
    add_message(request, constants.ERROR, message, extra_tags=extra_tags,
                fail_silently=fail_silently)