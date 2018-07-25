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

class OrganizationNotFoundException(Exception):
    def __init__(self, organization_id):
        self.organization_id = organization_id
        msg = 'Organization with id \'%s\' does not exists' % self.organization_id
        super(OrganizationNotFoundException, self).__init__(msg)


class OrganizationAlreadyExistsException(Exception):
    def __init__(self, organization_id):
        self.organization_id = organization_id
        msg = 'Organization with client id \'%s\' already exists' % self.organization_id
        super(OrganizationAlreadyExistsException, self).__init__(msg)
