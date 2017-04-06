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

class ContractsService:
    def __init__(self, client):
        self.client = client



    def GetContract(self, contractId, headers=None, query_params=None):
        """
        Get a contract
        It is method for GET /contracts/{contractId}
        """
        uri = self.client.base_url + "/contracts/" + contractId
        return self.client.session.get(uri, headers=headers, params=query_params)


    def SignContract(self, data, contractId, headers=None, query_params=None):
        """
        Sign a contract
        It is method for POST /contracts/{contractId}/signatures
        """
        uri = self.client.base_url + "/contracts/" + contractId + "/signatures"
        return self.client.post(uri, data, headers=headers, params=query_params)
