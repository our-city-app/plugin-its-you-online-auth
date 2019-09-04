# -*- coding: utf-8 -*-
# Copyright 2019 Green Valley Belgium NV
# NOTICE: THIS FILE HAS BEEN MODIFIED BY GREEN VALLEY BELGIUM NV IN ACCORDANCE WITH THE APACHE LICENSE VERSION 2.0
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
# @@license_version:1.6@@

from google.appengine.ext import ndb

from framework.utils import chunks
from plugins.its_you_online_auth.models import Profile


def migrate(dry_run=False):
    profiles = Profile.query()
    to_put = []
    to_delete = []
    for profile in profiles:
        if profile.key.parent() and profile.key.parent().id():
            to_put.append(Profile(key=Profile.create_key(profile.username),
                                  organization_id=profile.organization_id,
                                  app_email=profile.app_email,
                                  language=profile.language))
            to_delete.append(profile.key)
    if dry_run:
        return to_put, to_delete
    for parts in chunks(to_put, 200):
        ndb.put_multi(parts)
    for parts in chunks(to_delete, 200):
        ndb.delete_multi(parts)
