# -*- coding: utf-8 -*-
# Copyright 2016 Mobicage NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @@license_version:1.1@@
import re

from plugins.its_you_online_auth.plugin_consts import Scopes

admin_re = re.compile('memberof:(.*?):admin')


def is_admin(session):
    """
    Args:
        session (models.Session)
    Returns:
        is_admin(bool)
    """
    return any(scope == Scopes.ADMIN for scope in session.scopes)


def get_admin_organization(session):
    """
    Args:
        session (models.Session)
    Returns:
        unicode
    """
    for scope in session.scopes:
        match = admin_re.match(scope)
        if match:
            return match.group(0)
