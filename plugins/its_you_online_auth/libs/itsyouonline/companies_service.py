# -*- coding: utf-8 -*-
# Copyright 2017 Green IT Globe NV
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

class CompaniesService:
    def __init__(self, client):
        self.client = client



    def GetCompanyList(self, headers=None, query_params=None):
        """
        Get companies. Authorization limits are applied to requesting user.
        It is method for GET /companies
        """
        uri = self.client.base_url + "/companies"
        return self.client.session.get(uri, headers=headers, params=query_params)


    def CreateCompany(self, data, headers=None, query_params=None):
        """
        Register a new company
        It is method for POST /companies
        """
        uri = self.client.base_url + "/companies"
        return self.client.post(uri, data, headers=headers, params=query_params)


    def GetCompany(self, globalId, headers=None, query_params=None):
        """
        Get organization info
        It is method for GET /companies/{globalId}
        """
        uri = self.client.base_url + "/companies/" + globalId
        return self.client.session.get(uri, headers=headers, params=query_params)


    def UpdateCompany(self, data, globalId, headers=None, query_params=None):
        """
        Update existing company. Updating ``globalId`` is not allowed.
        It is method for PUT /companies/{globalId}
        """
        uri = self.client.base_url + "/companies/" + globalId
        return self.client.put(uri, data, headers=headers, params=query_params)


    def GetCompanyContracts(self, globalId, headers=None, query_params=None):
        """
        Get the contracts where the organization is 1 of the parties. Order descending by date.
        It is method for GET /companies/{globalId}/contracts
        """
        uri = self.client.base_url + "/companies/" + globalId + "/contracts"
        return self.client.session.get(uri, headers=headers, params=query_params)


    def CreateCompanyContract(self, data, globalId, headers=None, query_params=None):
        """
        Create a new contract.
        It is method for POST /companies/{globalId}/contracts
        """
        uri = self.client.base_url + "/companies/" + globalId + "/contracts"
        return self.client.post(uri, data, headers=headers, params=query_params)


    def GetCompanyInfo(self, globalId, headers=None, query_params=None):
        """
        It is method for GET /companies/{globalId}/info
        """
        uri = self.client.base_url + "/companies/" + globalId + "/info"
        return self.client.session.get(uri, headers=headers, params=query_params)


    def companies_byGlobalId_validate_get(self, globalId, headers=None, query_params=None):
        """
        It is method for GET /companies/{globalId}/validate
        """
        uri = self.client.base_url + "/companies/" + globalId + "/validate"
        return self.client.session.get(uri, headers=headers, params=query_params)
