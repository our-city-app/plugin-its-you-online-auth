# -*- coding: utf-8 -*-
# Copyright 2017 GIG Technology NV
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
# @@license_version:1.3@@
import logging

import webapp2

from framework.bizz.job import run_job
from framework.models.session import Session
from plugins.its_you_online_auth.bizz.authentication import validate_session


class RefreshJwtsHandler(webapp2.RequestHandler):
    def get(self):
        run_job(_get_all_sessions, [], _refresh_jwt_if_needed, [], qry_transactional=False, worker_queue='iyo-requests')


def _get_all_sessions():
    return Session.query()


def _refresh_jwt_if_needed(session_key):
    session = session_key.get()
    if session:
        logging.info('Refreshing session %s for user %s', session.key, session.user_id)
        validate_session(session)
