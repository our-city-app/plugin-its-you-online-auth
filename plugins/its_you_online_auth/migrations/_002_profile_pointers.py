# -*- coding: utf-8 -*-
# Copyright 2018 Mobicage NV
# NOTICE: THIS FILE HAS BEEN MODIFIED BY MOBICAGE NV IN ACCORDANCE WITH THE APACHE LICENSE VERSION 2.0
# Copyright 2018 GIG Technology NV
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
# @@license_version:1.5@@

from google.appengine.ext import ndb

from framework.utils import chunks
from plugins.its_you_online_auth.models import Profile, ProfileAppEmailMapping


def migrate(dry_run=False):
    to_put = [ProfileAppEmailMapping(key=ProfileAppEmailMapping.create_key(p.app_email), username=p.username) for p in
              Profile.list_with_app_user()]
    if dry_run:
        return len(to_put), to_put
    for parts in chunks(to_put, 200):
        ndb.put_multi(parts)
