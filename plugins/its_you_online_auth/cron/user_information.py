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

import webapp2

from framework.bizz.job import run_job
from framework.plugin_loader import get_config
from plugins.its_you_online_auth.bizz.profile import set_user_information
from plugins.its_you_online_auth.models import Profile
from plugins.its_you_online_auth.plugin_consts import NAMESPACE


class RefreshUserInformationHandler(webapp2.RequestHandler):
    def get(self):
        if get_config(NAMESPACE).fetch_information:
            run_job(_get_all_profiles, [], set_user_information, [], qry_transactional=False,
                    worker_queue='iyo-requests')


def _get_all_profiles():
    return Profile.query()
