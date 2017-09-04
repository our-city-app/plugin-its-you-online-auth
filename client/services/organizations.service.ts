import { HttpClient } from '@angular/common/http';
// angular
import { Injectable } from '@angular/core';
// libs
// app
import { Analytics, AnalyticsService } from '../../../framework/client/analytics/index';
import { ITS_YOU_ONLINE_CATEGORY } from '../common/category.common';
// module
import { Organization } from '../index';
import { ItsYouOnlineConfig } from './its-you-online-config';

@Injectable()
export class OrganizationsService extends Analytics {

  constructor(public analytics: AnalyticsService, private http: HttpClient) {
    super(analytics);
    this.category = ITS_YOU_ONLINE_CATEGORY;
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
      .map(res => organization);
  }
}
