import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Organization } from '../index';
import { ItsYouOnlineConfig } from './its-you-online-config';

@Injectable()
export class OrganizationsService {

  constructor(private http: HttpClient) {
  }

  getOrganizations() {
    return this.http.get<Organization[]>(`${ItsYouOnlineConfig.API_URL}/organizations`);
  }

  getOrganization(id: string) {
    return this.http.get<Organization>(`${ItsYouOnlineConfig.API_URL}/organizations/${encodeURIComponent(id)}`);
  }

  createOrganization(organization: Organization) {
    return this.http.post<Organization>(`${ItsYouOnlineConfig.API_URL}/organizations`, organization);
  }

  updateOrganization(organization: Organization) {
    const url = `${ItsYouOnlineConfig.API_URL}/organizations/${encodeURIComponent(organization.id)}`;
    return this.http.put<Organization>(url, organization);
  }

  deleteOrganization(organization: Organization) {
    return this.http.delete(`${ItsYouOnlineConfig.API_URL}/organizations/${encodeURIComponent(organization.id)}`)
      .map(() => organization);
  }
}
